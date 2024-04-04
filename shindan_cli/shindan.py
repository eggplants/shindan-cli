"""Implements the function to get the shindan result from <https://shindanmaker.com>."""

from __future__ import annotations

import random
import re
import time
from typing import TypedDict, Union

from bs4 import BeautifulSoup, Tag
from requests import Session, codes


class ShindanResult(TypedDict):
    """TypedDict Class for result of shindan."""

    results: list[str]
    hashtags: list[str]
    shindan_url: str


class ShindanError(Exception):
    """Error class for shindan-cli."""


Params = dict[str, Union[str, list[str], None]]

TARGET_KEYS_BY_TYPE = {
    "ai": ("_token", "shindanName", "type", "shindan_token"),
    "branch": ("_token", "shindanName", "hiddenName", "type", "shindan_token", "rbr"),
    "check": ("_token", "shindanName", "hiddenName", "type", "shindan_token"),
    "name": ("_token", "shindanName", "hiddenName", "type", "shindan_token"),
}

BASE_URL = "https://shindanmaker.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
}


class UserInput(TypedDict):
    q: str
    a: str | None


UserInputs = dict[str, UserInput]


def get_user_inputs(source: BeautifulSoup) -> UserInputs:
    user_inputs: dict[str, UserInput] = {}
    form_labels = source.select("form#shindanForm > div.px-3 > div > span")
    for idx, question in enumerate([*form_labels, *range(10 - len(form_labels))]):
        if isinstance(question, int):
            user_inputs[f"user_input_{idx + 1}"] = {"q": "", "a": None}
            continue
        question_text = question.text
        answer_text = None
        while not answer_text:
            answer_text = input(f"[{question_text}]: ").strip()
        user_inputs["user_input_{idx + 1}"] = {"q": question_text, "a": answer_text}
    return user_inputs


class QuestionBranchChoice(TypedDict):
    label: str
    next_branch_id: str


class QuestionBranch(TypedDict):
    question: str
    choices: list[QuestionBranchChoice]


def get_rbr(source: BeautifulSoup) -> str:
    question_branches: dict[str, QuestionBranch] = {}
    for branch in source.select("div[id^='shindan_branch_'][data-kind='0']"):
        branch_id = branch.get("id")
        question = branch.select_one("p.shindan_branch_question")
        if not isinstance(branch_id, str) or not question:
            continue
        question_branches[branch_id.replace("shindan_branch_", "")] = {
            "question": question.text.strip(),
            "choices": [
                {
                    "label": choice.text,
                    "next_branch_id": next_branch_id,
                }
                for choice in branch.select("button")
                if isinstance(next_branch_id := choice.get("data-next_branch"), str)
            ],
        }

    goal_branches: dict[str, str] = {}
    for branch in source.select("div[id^='shindan_branch_'][data-kind='1']"):
        branch_id = branch.get("id")
        rbr = branch.get("data-rbr")
        if not isinstance(branch_id, str) or not isinstance(rbr, str):
            continue
        goal_branches[branch_id.replace("shindan_branch_", "")] = rbr

    current_branch_id = "1"
    while current_branch_id not in goal_branches:
        current_branch = question_branches[current_branch_id]
        choices = current_branch["choices"]

        print("[Q.", current_branch["question"], "]")  # noqa: T201
        for idx, choice in enumerate(choices):
            print(f"> {idx}:", choice["label"])  # noqa: T201

        inputed_text = input(">>> ").strip()
        if not inputed_text:
            continue
        selected_id = int(inputed_text)
        if 0 <= selected_id < len(choices):
            current_branch_id = choices[selected_id]["next_branch_id"]

    return goal_branches[current_branch_id]


class QuestionChoiceChoice(TypedDict):
    label: str
    choice_id: str


class QuestionChoice(TypedDict):
    question: str
    choices: list[QuestionChoiceChoice]


def get_choices(source: BeautifulSoup) -> dict[int, str]:
    question_choices: dict[int, QuestionChoice] = {}
    for question in source.select("div.check-username-target"):
        order_id = question.get("data-order")
        question_text = question.select_one("div > p > span")
        if not isinstance(order_id, str) or not question_text:
            continue
        question_choices[int(order_id)] = {
            "question": question_text.text.strip(),
            "choices": [
                {"label": choice.text.strip(), "choice_id": choice_key}
                for choice in question.select("button.list-group-item")
                if isinstance(choice_key := choice.get("data-choice_key"), str)
            ],
        }
    current_question_id = 1
    total_questions = len(question_choices)
    answers: dict[int, str] = {}
    while len(answers) < total_questions:
        current_question = question_choices[current_question_id]
        choices = current_question["choices"]
        print(  # noqa: T201
            f"= {current_question_id}/{total_questions} =\n",
            current_question["question"],
            "\n===",
        )
        for idx, choice in enumerate(choices):
            print(f"> {idx}:", choice["label"])  # noqa: T201

        inputed_text = input(">>> ").strip()
        if not inputed_text:
            continue
        selected_id = int(inputed_text)
        if 0 <= selected_id < len(choices):
            answers[current_question_id] = choices[selected_id]["choice_id"]
            current_question_id += 1
    return answers


def __get_result(session: Session, params: Params, *, is_renewal: bool = False, shindan_url: str) -> ShindanResult:
    result_page = session.post(
        shindan_url + ("/r" if is_renewal else ""),
        data=params,
        headers=HEADERS,
    )
    soup = BeautifulSoup(result_page.text, features="lxml")
    result_tag = soup.find(id="share-copytext-shindanresult-textarea")

    if not isinstance(result_tag, Tag) or not result_tag.text:
        msg = f"Could not find a tag contains the result, returns: {result_tag}"
        raise ShindanError(msg)

    *results, hashtag, shindan_url, _ = result_tag.text.split("\n")

    if not results[-1]:
        results.pop(-1)

    return {
        "results": results,
        "hashtags": hashtag.split("\xa0"),
        "shindan_url": shindan_url,
    }


def get_result_by_ai(
    session: Session,
    params: Params,
    *,
    user_inputs: UserInputs,
    hashtag: str | None,
    shindan_url: str,
) -> ShindanResult:
    session.post(
        f"{shindan_url}/ai_life_update",
        data={"ai_life": 3},
        headers=HEADERS,
    )
    result_sse = session.post(
        f"{shindan_url}/ai_result",
        json={
            "form_values": user_inputs,
            "shindan_token": params["shindan_token"],
            "ai_result_request_times": 0,
        },
        headers=HEADERS,
    )
    gpt_results = "".join(
        re.findall(r'^\s+"content": "(.*)"$', result_sse.text),
    ).split("\n")
    return {
        "results": gpt_results,
        "hashtags": [hashtag, "#shindanmaker"] if hashtag else ["#shindanmaker"],
        "shindan_url": shindan_url,
    }


def get_result_by_branch(session: Session, params: Params, *, shindan_url: str) -> ShindanResult:
    return __get_result(session, params, is_renewal=True, shindan_url=shindan_url)


def get_result_by_check(
    session: Session,
    params: Params,
    *,
    user_choices: dict[int, str],
    shindan_url: str,
) -> ShindanResult:
    for choice_id, answer_id in user_choices.items():
        params[f"input-check-choice[{choice_id}]"] = answer_id

    return __get_result(session, params, is_renewal=True, shindan_url=shindan_url)


def get_result_by_name(session: Session, params: Params, *, shindan_url: str) -> ShindanResult:
    return __get_result(session, params, shindan_url=shindan_url)


def shindan(page_id: int, shindan_name: str, *, wait: bool | None = False) -> ShindanResult:
    """Get the shindan result from <https://shindanmaker.com>.

    Parameters
    ----------
    page_id : int
        shindan page id (e.g. `1036646`)
    shindan_name : str
        shindan name (e.g. your name)
    wait : bool | None, optional
        enable random waits while fetching shindan data, by default False

    Returns
    -------
    ShindanResult
        the returned result from <https://shindanmaker.com>

    Raises
    ------
    ShindanError

    """
    if not isinstance(page_id, int) or page_id < 0:
        msg = f"invalid page id: {page_id}"
        raise ShindanError(msg)
    shindan_url = f"{BASE_URL}/{page_id}"

    session = Session()

    shindan_page = session.get(shindan_url, headers=HEADERS)
    if shindan_page.status_code != codes.ok:
        raise ShindanError(shindan_page.status_code)

    source = BeautifulSoup(shindan_page.text, features="lxml")

    shindan_type_input = source.select_one('input[name="type"]')
    if not shindan_type_input or not shindan_type_input.get("value"):
        msg = "Cannot detect shindan type!"
        raise ValueError(msg)
    shindan_type = str(shindan_type_input.get("value"))
    params = {
        key: key_input.get("value")
        for key in TARGET_KEYS_BY_TYPE[shindan_type]
        if (key_input := source.select_one(f'input[name="{key}"]'))
    }
    # overwrite shindanName
    if "shindanName" in params:
        params["shindanName"] = shindan_name

    # overwrite rbr
    if "rbr" in params:
        params["rbr"] = get_rbr(source)

    if wait:
        time.sleep(random.uniform(2, 5))  # noqa: S311

    if shindan_type == "ai":
        raise NotImplementedError(shindan_type)

        hashtag_title = source.select_one("h1#shindanTitle")
        if not hashtag_title or not isinstance(hashtag := hashtag_title.get("data-shindan_hashtag"), str):
            hashtag = None
        return get_result_by_ai(
            session,
            params,
            user_inputs=get_user_inputs(source),
            hashtag=hashtag,
            shindan_url=shindan_url,
        )
    if shindan_type == "branch":
        return get_result_by_branch(
            session,
            params,
            shindan_url=shindan_url,
        )
    if shindan_type == "check":
        return get_result_by_check(
            session,
            params,
            user_choices=get_choices(source),
            shindan_url=shindan_url,
        )
    if shindan_type == "name":
        return get_result_by_name(
            session,
            params,
            shindan_url=shindan_url,
        )
    raise NotImplementedError(shindan_type)


__all__ = ("ShindanResult", "shindan")
