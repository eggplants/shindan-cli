from __future__ import annotations

from time import time

import pytest

from shindan_cli import ShindanError
from shindan_cli.main import main


def test_no_args(capfd: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main(test=[])
    captured = capfd.readouterr()
    assert not captured.out
    assert captured.err == "\n".join(
        [
            "usage: shindan [-h] [-w] [-H] [-l] [-V] ID NAME",
            "shindan: error: the following arguments are required: ID, NAME",
            "",
        ],
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
    assert captured.err == "\n".join(
        [
            "usage: shindan [-h] [-w] [-H] [-l] [-V] ID NAME",
            "shindan: error: the following arguments are required: NAME",
            "",
        ],
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
