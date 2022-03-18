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
    "-t",
    "--textfile",
    help=
    """
    
    """,
    action="store_true"
)
group.add_argument(
    "-w",
    "--wavfile",
    help=
    """
    Accepts a wav file, outputs a plaintext file of the same name
    or if specified as the second positional argument.
    """,
    action="store_true"
)

group.add_argument("in_file",
                   nargs="?",
                   type=argparse.FileType('r'),
                   default=sys.stdin,
                   help="input file")
group.add_argument("out_file",
                   nargs="?",
                   type=argparse.FileType('w'),
                   default=sys.stdout,
                   help="output file")


args = parser.parse_args()

#if not args.out_file:
#    out_file = 

if args.interactive:
    UserMode()
# elif args.textfile:
#     TextParser(args.in_file, args.files[1])
# elif args.wavfile:
#     WavParser(args.in_file, args.files[1])
else:
    print(parser.parse_args(["-h"]))
