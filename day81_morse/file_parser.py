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
        # Calculate the duration of those intervals
        # Determine roughly how many different intervals we have
        # Use those to appropriately categorize each interval
        # Turn that into morse symbols, then to text
        try:
            with wave.open(self.in_file, "rb") as file:
                frequency = file.getframerate()
                number_of_frames = file.getnframes()
                data = file.readframes(number_of_frames)
                data_segments = []
                frame_number = 0
                last_frame = (-1,-1) # (data_value, frame_pos)
                
                for frame in struct.iter_unpack("<h", data):
                    if data_segments == []:
                        data_segments.append(("on", frame_number))
                    elif (data_segments[len(data_segments)-1][0] == "on" and
                         last_frame[0] == 0 and
                         frame[0] == 0):
                            data_segments.append(("off", last_frame[1]))
                    elif (data_segments[len(data_segments)-1][0] == "off" and
                         frame[0] != 0):
                            data_segments.append(("on", frame_number+1))
                    else:
                        pass
                    frame_number += 1
                    last_frame = (frame[0], frame_number)

                tokens = []
                for i in range(len(data_segments)-1):
                    if data_segments[i][0] == "on":
                        tokens.append(
                            ("on",data_segments[i+1][1]-data_segments[i][1])
                        )
                    elif data_segments[i][0] == "off":
                        tokens.append(
                            ("off",data_segments[i+1][1]-data_segments[i][1])
                        )
                    else:
                        pass
                with open("test.txt", "w") as file:
                    for token in tokens:
                        file.write(f"{token}\n")
                
        except FileNotFoundError:
            print(f"Unable to open file {self.in_file}")


    def output_text(self):
        with open("./output.txt", "w") as file:
            file.write(self.message_out)


#   UNIT_LEN = .27 #seconds
#   DOT = 1 * UNIT_LEN # dit
#   DASH = 3 * UNIT_LEN # dah
#   I_PAUSE = 1 * UNIT_LEN # inner pause
#   L_PAUSE = 2 * UNIT_LEN # letter pause: followed by I_PAUSE, so 2+1=3
#   W_PAUSE = 0 * UNIT_LEN # word pause: 
#                          # surrounded by L_PAUSE, followed by I_PAUSE
#                          # so 3+1+3=7u, don't technically need a frame here 
#   
#   SIGNAL_CONVERSION = {
#       ".": DOT,
#       "-": DASH,
#       " ": L_PAUSE,
#       "|": W_PAUSE, 
#   }

    def output_wave(self):
        with wave.open("./output.wav", "wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(SAMPLE_RATE)
            all_frames = []
            for symbol in self.message_out:
                print(f"'{symbol}'")
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
