"""HTTP helpers to cope with rate limiting on <https://shindanmaker.com>."""

from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from requests import Response, Session

TOO_MANY_REQUESTS = 429

MAX_RETRIES = 5
INITIAL_WAIT = 2.0
BACKOFF_FACTOR = 2.0

WAIT_RANGE = (2.0, 5.0)


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
    method: str,
    url: str,
    **kwargs: Any,  # noqa: ANN401
) -> Response:
    """Send a request, retrying with a backoff while the site rate limits us.

    The site is fronted by Cloudflare, which answers bursts of requests with a
    `429` challenge page instead of the result. Those responses are transient,
    so they are retried rather than reported to the caller.

    Args:
        session (Session): session object
        method (str): HTTP method
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
    "random_wait",
    "request_with_retry",
)
