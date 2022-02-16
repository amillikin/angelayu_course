import argparse
from inputmanager import InputManager
from pricechecker import PriceChecker

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--interactive",
    help="Interactive input mode. Add Users & Items to Watch",
    action="store_true"
)
parser.add_argument(
    "-c",
    "--checkprices",
    help=
    """
        Check price mode.\n
        Looks up all items in the DB, 
        and notifies user when price falls under threshold.
    """,
    action="store_true"
)

args = parser.parse_args()

if args.interactive:
    InputManager()
elif args.checkprices:
    PriceChecker()
else:
    print(parser.parse_args(["-h"]))
