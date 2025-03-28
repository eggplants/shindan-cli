"""Implements the function to get the shindan result from <https://shindanmaker.com>."""

from __future__ import annotations

import random
import time

import cloudscraper  # type: ignore[unused-ignore,import-not-found,import-untyped]
from bs4 import BeautifulSoup
from requests import codes

from .constants import BASE_URL, HEADERS, TARGET_KEYS_BY_TYPE
from .get_results import (
    get_result_by_ai,
    get_result_by_branch,
    get_result_by_check,
    get_result_by_name,
)
from .interactive import get_choices, get_rbr, get_user_inputs
from .models import ShindanResult


class ShindanError(Exception):
    """Error class for shindan-cli."""


def shindan(
    page_id: int,
    shindan_name: str,
    *,
    wait: bool | None = False,
) -> ShindanResult:
    """Get the shindan result from <https://shindanmaker.com>.

    Args:
        page_id : int
            shindan page id (e.g. `1036646`)
        shindan_name : str
            shindan name (e.g. your name)
        wait : bool | None, optional
            enable random waits while fetching shindan data, by default False

    Returns:
        ShindanResult: the returned result from <https://shindanmaker.com>

    Raises:
        ShindanError

    """
    if not isinstance(page_id, int) or page_id < 0:
        msg = f"invalid page id: {page_id}"
        raise ShindanError(msg)
    shindan_url = f"{BASE_URL}/{page_id}"

    session = cloudscraper.create_scraper()

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
    # overwrite randname (old: shindanName)
    params["randname"] = shindan_name

    if wait:
        time.sleep(random.uniform(2, 5))  # noqa: S311

    if shindan_type == "ai":
        hashtag_title = source.select_one("h1#shindanTitle")
        if not hashtag_title or not isinstance(
            hashtag := hashtag_title.get("data-shindan_hashtag"),
            str,
        ):
            hashtag = None
        return get_result_by_ai(
            session,
            params,
            user_inputs=get_user_inputs(source, shindan_name),
            hashtag=hashtag,
            shindan_url=shindan_url,
        )
    if shindan_type == "branch":
        params["rbr"] = get_rbr(source)
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
