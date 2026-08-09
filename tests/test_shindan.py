from __future__ import annotations

import pytest

from shindan_cli import ShindanError, shindan

test_data: list[tuple[int, int]] = [
    (1036646, 3),  # general
    (962461, 2),  # with image
    (1195323, 1),  # with graph
]


@pytest.mark.parametrize(("page_id", "lines"), test_data)
def test_site_download(page_id: int, lines: int) -> None:
    res = shindan(page_id, "hoge")
    assert len(res["results"]) == lines, "invalid length of results"
    assert "#shindanmaker" in res["hashtags"], "invalid hashtags"
    assert res["shindan_url"] == f"https://shindanmaker.com/{page_id}", "invalid shindan url"


def test_invalid_id() -> None:
    with pytest.raises(ShindanError) as e:
        shindan(0, "hoge")
    assert e.value.args == (404,), "expected error is not raised."


def test_name() -> None:
    res = shindan(1224370, "hoge")
    assert any("hoge" in result for result in res["results"]), "name is not working."


def test_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    waits = 0

    def count_wait() -> None:
        nonlocal waits
        waits += 1

    monkeypatch.setattr("shindan_cli._http.random_wait", count_wait)

    shindan(1036646, "hoge", wait=False)
    assert waits == 0, "waiting is not skipped."

    shindan(1036646, "hoge", wait=True)
    assert waits == 1, "waiting is not working."
