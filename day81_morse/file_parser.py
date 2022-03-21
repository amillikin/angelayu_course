from morse_utils import *
import re
import wave
import math
import struct

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
            self.output_text()
        elif self.mode == "mt":
            self.parse_text("M")
            self.output_text()
        elif self.mode == "tw":
            self.parse_text("T")
            self.output_wave()
        elif self.mode == "wt":
            self.parse_wave()
        else:
            print(f"Mode {self.mode} is invalid.")

    def parse_text(self, parse_mode):
        try:
            with open(self.in_file, "r") as file:
                self.message_in = file.read().rstrip("\n")
                token_list = tokenizer(parse_mode, self.message_in)
                try: 
                    converted_list = [decoder(parse_mode)[token] for token in token_list]
                    self.message_out = joiner(parse_mode).join(converted_list)
                except KeyError:
                    print("Invalid character or combination provided.\n"
                            "self.message_in could not be converted.")
        except FileNotFoundError:
            print(f"Unable to open file {self.in_file}")


    def parse_wave(self):
        # TODO: how to read and interpret wave.
        # Read header info.
        # Set a threshold
        # Check frame when threshold passed and when it falls again.
        # Calculate the duration of those intervals
        # Determine roughly how many different intervals we have
        # Use those to appropriately categorize each interval
        # Turn that into morse symbols, then to text
        pass


    def output_text(self):
        with open("./output.txt", "w") as file:
            file.write(self.message_out)


    def output_wave(self):
        with wave.open("./output.wav", "wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(SAMPLE_RATE)
            all_frames = []
            for symbol in self.message_out:
                data_frames = self.create_frames(
                    duration=SIGNAL_CONVERSION[symbol],
                    volume=VOLUME
                )
                all_frames.extend(data_frames)
                
                pause_frames = self.create_frames(
                    duration=I_PAUSE,
                    volume=0
                )
                all_frames.extend(pause_frames)
            file.writeframes(b''.join(all_frames))


    def create_frames(self, duration, volume):
        data_frames = []
        for i in range(int(duration**2 * SAMPLE_RATE)):
            frame = int(
                volume * math.sin(FREQUENCY * math.pi * float(i) / float(SAMPLE_RATE))
            )
            data_frames.append(struct.pack("<h", frame))
        return data_frames
