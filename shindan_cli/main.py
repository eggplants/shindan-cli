import argparse
from . import shindan
from . import __version__

# type: (Any) -> int
def check_natural(v):
    if type(v) is int and int(v) < 0:
        raise argparse.ArgumentTypeError("%s is an invalid natural int" % v)
    return v

# type: None -> argparse.Namespace
def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog="shindan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="ShindanMaker (https://shindanmaker.com) CLI",
    )
    parser.add_argument(
        'page_id', metavar='ID', type=check_natural, help="shindan page id"
    )
    parser.add_argument(
        'shindan_name',
        metavar='NAME',
        type=str,
        help="shindan name"
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    return parser.parse_args()

def main():
    args = parse_args()
    print(shindan.shindan(args.page_id, args.shindan_name))


if __name__ == '__main__':
    main()
