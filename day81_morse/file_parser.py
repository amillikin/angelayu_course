from morse_utils import decoder, input_validator, joiner, tokenizer, prompt
import re

class FileParser:


    def __init__(self, in_file, mode):
        self.in_file = in_file
        self.mode = mode
        self.message_in = ""
        self.message_out = ""
        self.convert_input()

    def convert_input(self):
        if self.mode == "tm":
            self.parse_text("T")
        elif self.mode == "mt":
            self.parse_text("M")
        elif self.mode == "wt":
            self.parse_wave()
        elif self.mode == "ww":
            self.parse_wave()
        else:
            print(f"Mode {self.mode} is invalid.")

    def parse_text(self, parse_mode):
        try:
            with open(self.in_file, "r") as file:
                self.message_in = file.read().rstrip("\n")
                token_list = tokenizer(parse_mode, self.message_in)
                print(f"{token_list}")
                try: 
                    converted_list = [decoder(parse_mode)[token] for token in token_list]
                    self.message_out = joiner(parse_mode).join(converted_list)
                    print(f"{self.message_out}")
                except KeyError:
                    print("Invalid character or combination provided.\n"
                            "self.message_in could not be converted.")
        except FileNotFoundError:
            print(f"Unable to open file {self.in_file}")


    def parse_wave(self):
        pass
