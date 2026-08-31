"""Module contains functions to get the result from <https://shindanmaker.com>."""

from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING, cast

from bs4 import BeautifulSoup, Tag

from ._http import MAX_RETRIES, backoff_wait, form_headers, request_with_retry, xhr_headers
from .constants import AIParams, BranchParams, CheckParams, NameParams

if TYPE_CHECKING:
    from curl_cffi.requests import Session

    from .models import ShindanResult, UserInputs

Params = AIParams | BranchParams | CheckParams | NameParams


def __get_result(
    session: Session,
    params: Params,
    *,
    is_renewal: bool = False,
    shindan_url: str,
) -> ShindanResult:
    result_tag: Tag | None = None
    status_code = None

    for attempt in range(MAX_RETRIES):
        if attempt > 0:
            time.sleep(backoff_wait(attempt - 1))
        result_page = request_with_retry(
            session,
            "POST",
            shindan_url + ("/r" if is_renewal else ""),
            data=params,
            headers=form_headers(shindan_url),
        )
        status_code = result_page.status_code
        soup = BeautifulSoup(result_page.text, features="lxml")
        found = soup.find(id="share-copytext-shindanresult-textarea")
        if isinstance(found, Tag) and found.text:
            result_tag = found
            break

    if result_tag is None:
        msg = f"Could not find a tag contains the result, last status code: {status_code}"
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
    params: AIParams,
    *,
    user_inputs: UserInputs,
    hashtag: str | None,
    csrf_token: str,
    shindan_url: str,
) -> ShindanResult:
    """Get result by AI type shindan.

    Args:
        session (Session): session object
        params (Params): input parameters fetched from shindan page
        user_inputs (UserInputs): user inputs
        hashtag (str | None): hashtag
        csrf_token (str): CSRF token extracted from the shindan page
        shindan_url (str): shindan url

    Returns:
        ShindanResult: the returned result from <https://shindanmaker.com>

    """
    ai_headers = {**xhr_headers(shindan_url), "x-csrf-token": csrf_token}

    result_sse = request_with_retry(
        session,
        "POST",
        f"{shindan_url}/ai_result",
        json={
            "form_values": user_inputs,
            "shindan_token": params["_token"],
            "ai_result_request_times": 0,
            "encrypted_exec_key": params["encrypted_exec_key"],
        },
        headers=ai_headers,
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
    params: BranchParams,
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
    params: CheckParams,
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
    check_params = cast("dict[str, str]", params)
    for choice_id, answer_id in user_choices.items():
        check_params[f"input-check-choice[{choice_id}]"] = answer_id

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
