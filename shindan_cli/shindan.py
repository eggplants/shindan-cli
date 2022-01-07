import random
import time
from typing import List, Optional, TypedDict
from urllib import parse

import requests
from bs4 import BeautifulSoup as BS


class ShindanResult(TypedDict):
    results: List[str]
    hashtags: List[str]
    shindan_url: str


def shindan(
    page_id: int, shindan_name: str, wait: Optional[bool] = False
) -> ShindanResult:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/96.0.4664.45 Safari/537.36"
        )
    }
    if type(page_id) is int and page_id < 0:
        raise ValueError("invalid page id: %d" % page_id)
    url = "https://shindanmaker.com/%d" % page_id
    session = requests.session()
    s = session.get(url, headers=headers)
    if s.status_code != 200:
        raise FileNotFoundError(s.status_code)
    source = BS(s.text, features="lxml")
    params = {i["name"]: i["value"] for i in source.find_all("input")[1:4]}
    params["shindanName"] = shindan_name
    login = session.post(url, data=params, headers=headers)
    if wait:
        time.sleep(random.uniform(2, 5))
    soup = BS(login.text, features="lxml")
    parsed_url = parse.urlparse(soup.find(class_="flex-fill")["href"])  # type: ignore
    *val, hashtag, url = parse.unquote(
        parse.parse_qs(parsed_url.query)["text"][0]
    ).split("\n")
    hashtag = hashtag.split(" ")  # type: ignore
    return {"results": val, "hashtags": hashtag, "shindan_url": url}  # type: ignore
