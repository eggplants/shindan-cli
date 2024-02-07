"""Implements the function to get the shindan result from <https://shindanmaker.com>."""

from __future__ import annotations

import random
import time
from typing import TypedDict

import requests
from bs4 import BeautifulSoup, Tag


class ShindanResult(TypedDict):
    """TypedDict Class for result of shindan."""

    results: list[str]
    hashtags: list[str]
    shindan_url: str


class ShindanError(Exception):
    """Error class for shindan-cli."""


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
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/96.0.4664.45 Safari/537.36"
        ),
    }

    if not isinstance(page_id, int) or page_id < 0:
        msg = f"invalid page id: {page_id}"
        raise ShindanError(msg)

    url = f"https://shindanmaker.com/{page_id}"

    session = requests.session()
    s = session.get(url, headers=headers)
    if s.status_code != requests.codes.ok:
        raise ShindanError(s.status_code)

    source = BeautifulSoup(s.text, features="lxml")

    # q, _token, shindanName, hiddenName, type, shindan_token, q
    params = {i["name"]: i["value"] for i in source.find_all("input")[1:5]}

    # overwrite shindanName
    params["shindanName"] = shindan_name

    login = session.post(url, data=params, headers=headers)
    if wait:
        time.sleep(random.uniform(2, 5))  # noqa: S311

    soup = BeautifulSoup(login.text, features="lxml")
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


__all__ = ("ShindanResult", "shindan")
