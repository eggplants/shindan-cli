"""Module contains functions to get the result from <https://shindanmaker.com>."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Union

from bs4 import BeautifulSoup, Tag

from .constants import BASE_URL, HEADERS

if TYPE_CHECKING:
    from requests import Session

    from .models import ShindanResult, UserInputs

Params = dict[str, Union[str, list[str], None]]


def __get_result(
    session: Session,
    params: Params,
    *,
    is_renewal: bool = False,
    shindan_url: str,
) -> ShindanResult:
    result_page = session.post(
        shindan_url + ("/r" if is_renewal else ""),
        data=params,
        headers=HEADERS,
    )
    soup = BeautifulSoup(result_page.text, features="lxml")
    result_tag = soup.find(id="share-copytext-shindanresult-textarea")

    if not isinstance(result_tag, Tag) or not result_tag.text:
        msg = f"Could not find a tag contains the result, returns: {result_tag}"
        raise TypeError(msg)

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
    """Get result by AI type shindan.

    Args:
        session (Session): session object
        params (Params): input parameters fetched from shindan page
        user_inputs (UserInputs): user inputs
        hashtag (str | None): hashtag
        shindan_url (str): shindan url

    Returns:
        ShindanResult: the returned result from <https://shindanmaker.com>

    """
    res = session.post(
        shindan_url,
        data=params,
        headers=HEADERS,
    )
    meta = BeautifulSoup(
        res.text,
        features="lxml",
    ).select_one('meta[name="csrf-token"]')
    if not res.ok or not meta or not isinstance(csrf_token := meta.get("content"), str):
        msg = f"Failed to get the csrf token. ({res.status_code})"
        raise ValueError(msg)
    HEADERS.update({"x-csrf-token": csrf_token})
    if not res.ok:
        res = session.post(
            f"{BASE_URL}/ai_life_update",
            data={"ai_life": 3},
            headers=HEADERS,
        )
        if not res.ok:
            msg = f"Failed to update AI life. ({res.status_code})"
            raise ValueError(msg)

    result_sse = session.post(
        f"{shindan_url}/ai_result",
        json={
            "form_values": user_inputs,
            "shindan_token": params["_token"],
            "ai_result_request_times": 0,
        },
        headers=HEADERS,
    )
    gpt_results = "".join(
        re.findall(r'"content":"([^"]+)', result_sse.text),
    ).split("\n")
    return {
        "results": gpt_results,
        "hashtags": [hashtag, "#shindanmaker"] if hashtag else ["#shindanmaker"],
        "shindan_url": shindan_url,
    }


def get_result_by_branch(
    session: Session,
    params: Params,
    *,
    shindan_url: str,
) -> ShindanResult:
    """Get result by branch type shindan.

    Args:
        session (Session): session object
        params (Params): input parameters fetched from shindan page
        shindan_url (str): shindan url

    Returns:
        ShindanResult: the returned result from <https://shindanmaker.com>

    """
    return __get_result(session, params, is_renewal=True, shindan_url=shindan_url)


def get_result_by_check(
    session: Session,
    params: Params,
    *,
    user_choices: dict[int, str],
    shindan_url: str,
) -> ShindanResult:
    """Get result by check type shindan.

    Args:
        session (Session): session object
        params (Params): input parameters fetched from shindan page
        user_choices (dict[int, str]): choices inputted by user on terminal
        shindan_url (str): shindan url

    Returns:
        ShindanResult: the returned result from <https://shindanmaker.com>

    """
    for choice_id, answer_id in user_choices.items():
        params[f"input-check-choice[{choice_id}]"] = answer_id

    return __get_result(session, params, is_renewal=True, shindan_url=shindan_url)


def get_result_by_name(
    session: Session,
    params: Params,
    *,
    shindan_url: str,
) -> ShindanResult:
    """Get result by name type shindan.

    Args:
        session (Session): session object
        params (Params): input parameters fetched from shindan page
        shindan_url (str): shindan url

    Returns:
        ShindanResult: the returned result from <https://shindanmaker.com>

    """
    return __get_result(session, params, shindan_url=shindan_url)


__all__ = (
    "get_result_by_ai",
    "get_result_by_branch",
    "get_result_by_check",
    "get_result_by_name",
)
