import argparse
import sys
from pdfminer.high_level import extract_text
from gtts import gTTS


def convert_pdf(file):
    text = extract_text(pdf_file=file,
                          maxpages=2)
    tts = gTTS(text)
    tts.save("test.mp3")


parser = argparse.ArgumentParser()

parser.add_argument(
    "-f",
    "--file",
    type=str,
    help=
    """
    File to convert.
    e.g. python main.py -f book.pdf
    """,
)

args = parser.parse_args()
if args.file:
    convert_pdf(args.file)
else:
    print(parser.parse_args(["-h"]))
