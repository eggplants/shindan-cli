from __future__ import annotations

from textwrap import dedent
from time import time

import pytest

from shindan_cli import ShindanError
from shindan_cli.main import main


def test_no_args(capfd: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main(test=[])
    captured = capfd.readouterr()
    assert not captured.out
    assert (
        captured.err
        == "usage: shindan [-h] [-w] [-H] [-l] [-V] ID NAME\nshindan: error: the following arguments are required: ID, NAME\n"  # noqa: E501
    )
    assert e.value.args == (2,)


def test_invalid_id() -> None:
    with pytest.raises(ShindanError) as e:
        main(test=["000", "hoge"])
    assert e.value.args == (404,)


def test_no_name(capfd: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main(test=["1036646"])
    captured = capfd.readouterr()
    assert not captured.out
    assert (
        captured.err
        == "usage: shindan [-h] [-w] [-H] [-l] [-V] ID NAME\nshindan: error: the following arguments are required: NAME\n"  # noqa: E501
    )
    assert e.value.args == (2,)


def test_args_without_options(capfd: pytest.CaptureFixture[str]) -> None:
    main(test=["1036646", "hoge"])
    captured = capfd.readouterr()
    assert "ねこって、むしだ。" in captured.out
    assert not captured.err


def test_args_with_link(capfd: pytest.CaptureFixture[str]) -> None:
    main(test=["1036646", "hoge", "-l"])
    captured = capfd.readouterr()
    assert "ねこって、むしだ。" in captured.out
    assert "https://shindanmaker.com/1036646" in captured.out
    assert "#shindanmaker" not in captured.out
    assert not captured.err


def test_args_with_hashtags(capfd: pytest.CaptureFixture[str]) -> None:
    main(test=["1036646", "hoge", "-H"])
    captured = capfd.readouterr()
    assert "ねこって、むしだ。" in captured.out
    assert "https://shindanmaker.com/1036646" not in captured.out
    assert "#shindanmaker" in captured.out
    assert not captured.err


def test_args_with_link_and_hashtags(capfd: pytest.CaptureFixture[str]) -> None:
    main(test=["1036646", "hoge", "-l", "-H"])
    captured = capfd.readouterr()
    assert "ねこって、むしだ。" in captured.out
    assert "https://shindanmaker.com/1036646" in captured.out
    assert "#shindanmaker" in captured.out
    assert not captured.err


def test_wait() -> None:
    t1 = time()
    main(test=["1036646", "hoge"])
    t2 = time()
    main(test=["1036646", "hoge", "-w"])
    t3 = time()
    assert t3 - t2 > t2 - t1, "waiting is not working."


def test_ai(
    capfd: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    i = ["適当"]
    monkeypatch.setattr("builtins.input", lambda _: i.pop())
    main(test=["1202021", "hoge"])
    captured = capfd.readouterr()
    assert len(captured.out.strip()) > 0
    assert not captured.err


def test_branch(
    capfd: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    i = ["0"]
    monkeypatch.setattr("builtins.input", lambda _: i.pop())
    main(test=["1201948", "hoge"])
    captured = capfd.readouterr()
    assert (
        captured.out
        == dedent(
            """
        [Q. 可愛いのが異常なくらい大好き ]
        > 0: はい
        > 1: いいえ
        ［あなたは…「ゆめかわ女子」］
        ・おっちょこちょい系
        ・こだわりが強い
        ・嘘は苦手
        """,  # noqa: RUF001
        ).lstrip()
    )
    assert not captured.err


def test_check(
    capfd: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    i = ["0"]
    monkeypatch.setattr("builtins.input", lambda _: i.pop())
    main(test=["1201960", "hoge"])
    captured = capfd.readouterr()
    assert (
        captured.out
        == dedent(
            """
        = 1/1 =
        obahann
        ===
        > 0: はい
        > 1: いいえ
        1/1点
        [obahann]
        obahan
        """,
        ).lstrip()
    )
    assert not captured.err
