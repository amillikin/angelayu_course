import argparse
import sys
from file_parser import FileParser
from user_mode import UserMode


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-i",
    "--interactive",
    help="User interactive mode. Input morse/plaintext outputs reverse",
    action="store_true"
)
group.add_argument(
    "-f",
    "--file",
    nargs=2,
    type=str,
    help=
    """
    File to convert. |
    Mode argument determines operation. |
    tm: text to morse |
    mt: morse to text |
    tw: text to wav |
    wt: wav to text |
    e.g. python main.py -f message.txt tw
    """,
)

args = parser.parse_args()
if args.interactive:
    UserMode()
elif args.file:
    FileParser(args.file[0], args.file[1])
else:
    print(parser.parse_args(["-h"]))
