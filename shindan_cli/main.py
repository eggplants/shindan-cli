"""Implements Shindan CLI as a main script."""

from __future__ import annotations

import argparse

from . import __version__, shindan


def _check_natural(v: str) -> int:
    if int(v) < 0:
        raise argparse.ArgumentTypeError("%s is an invalid natural int" % v)
    return int(v)


def _parse_args(*, test: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="shindan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="ShindanMaker (https://shindanmaker.com) CLI",
    )
    parser.add_argument("page_id", metavar="ID", type=_check_natural, help="shindan page id")
    parser.add_argument("shindan_name", metavar="NAME", type=str, help="shindan name")
    parser.add_argument("-w", "--wait", action="store_true", help="insert random wait")
    parser.add_argument("-H", "--hashtag", action="store_true", help="add hashtag `#shindanmaker`")
    parser.add_argument("-l", "--link", action="store_true", help="add link to last of output")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    if test is None:
        return parser.parse_args()
    return parser.parse_args(test)


def main(*, test: list[str] | None = None) -> None:
    """Run CLI."""
    args = _parse_args(test=test)
    result = shindan(args.page_id, args.shindan_name, wait=args.wait)
    print("\n".join(result["results"]))  # noqa: T201
    if args.hashtag:
        print(" ".join(result["hashtags"]))  # noqa: T201
    if args.link:
        print(result["shindan_url"])  # noqa: T201


if __name__ == "__main__":
    main()
