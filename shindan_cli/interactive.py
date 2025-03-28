"""Interactive functions for the shindan CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

    from .models import QuestionBranch, QuestionChoice, UserInput, UserInputs


def get_user_inputs(
    source: BeautifulSoup,
    shindan_name: str,
) -> UserInputs:
    """Get user inputs from the shindan source.

    Args:
        source (BeautifulSoup): The source of the shindan page.
        shindan_name (str): The name of the shindan.

    Returns:
        UserInputs: The user inputs.

    """
    user_inputs: dict[str, UserInput] = {}
    form_labels = source.select("form#shindanForm > div.px-3 > div > span")
    for idx, question in enumerate([*form_labels, *range(10 - len(form_labels))]):
        if isinstance(question, int):
            user_inputs[f"user_input_{idx + 1}"] = {"q": "", "a": None}
            continue
        question_text = question.text
        if question_text == "あなたの名前":
            user_inputs[f"user_input_{idx + 1}"] = {
                "q": question_text,
                "a": shindan_name,
            }
            continue
        answer_text = None
        while not answer_text:
            answer_text = input(f"[{question_text}]: ").strip()
        user_inputs["user_input_{idx + 1}"] = {"q": question_text, "a": answer_text}
    return user_inputs


def get_rbr(source: BeautifulSoup) -> str:
    """Get the result of the shindan from the source.

    Args:
        source (BeautifulSoup): The source of the shindan page.

    Returns:
        str: The result of the shindan.

    """
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

        inputted_text = input(">>> ").strip()
        if not inputted_text:
            continue
        selected_id = int(inputted_text)
        if 0 <= selected_id < len(choices):
            current_branch_id = choices[selected_id]["next_branch_id"]

    return goal_branches[current_branch_id]


def get_choices(source: BeautifulSoup) -> dict[int, str]:
    """Get the choices from the shindan source.

    Args:
        source (BeautifulSoup): The source of the shindan page.

    Returns:
        dict[int, str]: The choices.

    """
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
            f"= {current_question_id}/{total_questions} =",
            current_question["question"].strip(),
            "===",
            sep="\n",
        )
        for idx, choice in enumerate(choices):
            print(f"> {idx}:", choice["label"])  # noqa: T201

        inputted_text = input(">>> ").strip()
        if not inputted_text:
            continue
        selected_id = int(inputted_text)
        if 0 <= selected_id < len(choices):
            answers[current_question_id] = choices[selected_id]["choice_id"]
            current_question_id += 1
    return answers


__all__ = (
    "get_choices",
    "get_rbr",
    "get_user_inputs",
)
