import re
from morse_utils import prompt, decoder, input_validator, tokenizer, joiner


class UserMode:


    def __init__(self):
        print("Welcome to Aaron's Morse Code Interpreter\nPlease select a mode.")
        self.active = True
        while self.active:
            self.convert_input()


    def convert_input(self):
        mode = ""
        while mode not in ("T","M","Q"):
            mode = input("(M)orse-to-Text\n"
                         "(T)ext-to-Morse\n"
                         "(Q)uit\n> ").upper()
        if mode == "Q":
            self.active = False
        else:
            message = input(prompt(mode)).strip().upper()
            while not re.match(input_validator(mode), message):
                message = input(prompt(mode)).strip().upper()
                print(f"{message}")
            token_list = tokenizer(mode, message)
            try: 
                converted_list = [decoder(mode)[token] for token in token_list]
                converted_message = joiner(mode).join(converted_list)
                print(f"{converted_message}")
            except KeyError:
                print("Invalid character or combination provided.\n"
                      "Message could not be converted.")
