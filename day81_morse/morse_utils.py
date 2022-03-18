import re

# Morse Code Durations:
# Length of a dot is one unit (dit)
# Length of a dash is three unit (dah)
# Space between each part of the one character is one unit
# Space between letters is three units
# Space between words is seven units
ALLOWED_MORSE = re.compile(r'^(?:[.-]{1,5})(?:\s+(?:[.-]{1,5}|\|))*$')
ALLOWED_TEXT = re.compile(r'[A-Za-z0-9\s]*')

UNIT_LEN = 100 #milliseconds
DOT = 1 * UNIT_LEN # dit
DASH = 3 * UNIT_LEN # dah
I_PAUSE = 1 * UNIT_LEN # inner pause
L_PAUSE = 3 * UNIT_LEN # letter pause
W_PAUSE = 7 * UNIT_LEN # word pause

TEXT_TO_MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    " ": "|"
}

MORSE_TO_TEXT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "|": " "
}

def prompt(mode: str):
    """
    Accepts mode (M)orse-to-Text or (T)ext-to-Morse
    Returns respective prompt 
    """
    if mode == "M":
        return (
            "Please provide morse code using '-' and '.'.\n"
            "You may separate words with '|'\n"
            "(e.g) -. --- .-- | .. | -.- -. --- .--\n> "
            )
    elif mode == "T":
        return "Please provide text to be converted to morse code.\n> "


def decoder(mode: str):
    """
    Accepts mode (M)orse-to-Text or (T)ext-to-Morse
    Returns respective decoder dictionary
    """
    if mode == "M":
        return MORSE_TO_TEXT
    elif mode == "T":
        return TEXT_TO_MORSE


def input_validator(mode: str):
    """
    Accepts mode (M)orse-to-Text or (T)ext-to-Morse
    Returns respective input regex validator
    """
    if mode == "M":
        return ALLOWED_MORSE
    elif mode == "T":
        return ALLOWED_TEXT


def tokenizer(mode: str, message: str):
    """
    Accepts mode (M)orse-to-Text or (T)ext-to-Morse and string to split
    Returns respective tokenized message
    """
    if mode == "M":
        return message.split()
    elif mode == "T":
        return list(message)


def joiner(mode: str):
    """
    Accepts mode (M)orse-to-Text or (T)ext-to-Morse
    Returns respective joiner for converted input
    """
    if mode == "M":
        return ""
    elif mode == "T":
        return " "
