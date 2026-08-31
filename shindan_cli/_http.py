"""HTTP helpers to cope with bot detection and rate limiting on <https://shindanmaker.com>."""

from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING, Any

from curl_cffi import requests

from .constants import BASE_URL, HEADERS, IMPERSONATE

if TYPE_CHECKING:
    from curl_cffi.requests import HttpMethod, Response, Session

TOO_MANY_REQUESTS = 429

MAX_RETRIES = 5
INITIAL_WAIT = 2.0
BACKOFF_FACTOR = 2.0

WAIT_RANGE = (2.0, 5.0)


def create_session() -> Session:
    """Open a session that Cloudflare takes for a browser.

    `curl_cffi` replays Chrome's TLS and HTTP/2 handshake, which is what keeps
    the site from answering with a `403` bot challenge. An ordinary HTTP client
    is recognised by that handshake alone, whatever headers it sends.

    Returns:
        Session: session impersonating a browser

    """
    return requests.Session(impersonate=IMPERSONATE)


def form_headers(referer: str) -> dict[str, str]:
    """Get the headers a browser sends when submitting a form on a shindan page.

    Args:
        referer (str): url of the page holding the form

    Returns:
        dict[str, str]: headers to send alongside the impersonated ones

    """
    return {
        **HEADERS,
        "Origin": BASE_URL,
        "Referer": referer,
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-User": "?1",
    }


def xhr_headers(referer: str) -> dict[str, str]:
    """Get the headers a browser sends for the background requests a shindan page makes.

    Args:
        referer (str): url of the page making the request

    Returns:
        dict[str, str]: headers to send alongside the impersonated ones

    """
    return {
        **HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Origin": BASE_URL,
        "Referer": referer,
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
    }


def random_wait() -> None:
    """Sleep for a random while, to fetch at a less machine-like pace."""
    time.sleep(random.uniform(*WAIT_RANGE))  # noqa: S311


def backoff_wait(attempt: int) -> float:
    """Get how long to wait before the given retry attempt.

    Args:
        attempt (int): 0-based index of the retry about to be made

    Returns:
        float: seconds to sleep

    """
    return INITIAL_WAIT * BACKOFF_FACTOR**attempt


def request_with_retry(
    session: Session,
    method: HttpMethod,
    url: str,
    **kwargs: Any,  # noqa: ANN401
) -> Response:
    """Send a request, retrying with a backoff while the site rate limits us.

    The site is fronted by Cloudflare, which answers bursts of requests with a
    `429` challenge page instead of the result. Those responses are transient,
    so they are retried rather than reported to the caller.

    Args:
        session (Session): session object
        method (HttpMethod): HTTP method
        url (str): url to request
        **kwargs (Any): extra arguments passed to `Session.request`

    Returns:
        Response: the last response received

    """
    response = session.request(method, url, **kwargs)
    for attempt in range(MAX_RETRIES - 1):
        if response.status_code != TOO_MANY_REQUESTS:
            break
        time.sleep(backoff_wait(attempt))
        response = session.request(method, url, **kwargs)
    return response


__all__ = (
    "BACKOFF_FACTOR",
    "INITIAL_WAIT",
    "MAX_RETRIES",
    "TOO_MANY_REQUESTS",
    "WAIT_RANGE",
    "backoff_wait",
    "create_session",
    "form_headers",
    "random_wait",
    "request_with_retry",
    "xhr_headers",
)
