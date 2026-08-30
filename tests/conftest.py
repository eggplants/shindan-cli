"""Shared helpers for the tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from shindan_cli import ShindanError

if TYPE_CHECKING:
    from collections.abc import Generator

FORBIDDEN = 403


def skip_if_blocked(error: ShindanError) -> None:
    """Skip the running test if the request was blocked by Cloudflare.

    <https://shindanmaker.com> is fronted by Cloudflare, which answers requests
    from data center addresses (GitHub Actions runners, for one) with a `403`
    instead of the page. Nothing can be tested against the site from there, so
    those runs are skipped rather than reported as failures.

    Args:
        error (ShindanError): error raised while fetching a shindan

    """
    if error.args[:1] == (FORBIDDEN,):
        pytest.skip("blocked by Cloudflare: cannot reach shindanmaker.com from here")


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None]:  # noqa: ARG001
    """Turn a Cloudflare block into a skipped test instead of a failure."""
    try:
        return (yield)
    except ShindanError as error:
        skip_if_blocked(error)
        raise
