import argparse

from . import __version__, shindan


def check_natural(v: str) -> int:
    if int(v) < 0:
        raise argparse.ArgumentTypeError("%s is an invalid natural int" % v)
    else:
        return int(v)


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog="shindan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="ShindanMaker (https://shindanmaker.com) CLI",
    )
    parser.add_argument(
        "page_id", metavar="ID", type=check_natural, help="shindan page id"
    )
    parser.add_argument("shindan_name", metavar="NAME", type=str, help="shindan name")
    parser.add_argument("-w", "--wait", action="store_true", help="insert random wait")
    parser.add_argument(
        "-H", "--hashtag", action="store_true", help="add hashtag `#shindanmaker`"
    )
    parser.add_argument(
        "-l", "--link", action="store_true", help="add link to last of output"
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = shindan.shindan(args.page_id, args.shindan_name, wait=args.wait)
    print("\n".join(result["results"]))
    if args.hashtag:
        print(" ".join(result["hashtags"]))
    if args.link:
        print(result["shindan_url"])


if __name__ == "__main__":
    main()
