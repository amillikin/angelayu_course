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
            self.read_text()
            self.parse_text("T")
            self.output_text()
        elif self.mode == "mt":
            self.read_text()
            self.parse_text("M")
            self.output_text()
        elif self.mode == "tw":
            self.parse_text("T")
            self.output_wave()
        elif self.mode == "wt":
            self.parse_wave()
            self.parse_text("M")
            self.output_text()
        else:
            print(f"Mode {self.mode} is invalid.")

    def read_text(self):
        try:
            with open(self.in_file, "r") as file:
                self.message_in = file.read().rstrip("\n")
        except FileNotFoundError:
            print(f"Unable to open file {self.in_file}")


    def parse_text(self, parse_mode):
        token_list = tokenizer(parse_mode, self.message_in)
        try: 
            converted_list = [decoder(parse_mode)[token] for token in token_list]
            self.message_out = joiner(parse_mode).join(converted_list)
        except KeyError:
            print("Invalid character or combination provided.\n"
                    "self.message_in could not be converted.")


    def parse_wave(self):
        try:
            with wave.open(self.in_file, "rb") as file:
                frequency = file.getframerate()
                number_of_frames = file.getnframes()
                data = file.readframes(number_of_frames)
        except FileNotFoundError:
            print(f"Unable to open file {self.in_file}")

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

        timing_segments = []
        for i in range(len(data_segments)-1):
            if data_segments[i][0] == "on":
                timing_segments.append(
                    ("on",data_segments[i+1][1]-data_segments[i][1])
                )
            elif data_segments[i][0] == "off":
                timing_segments.append(
                    ("off",data_segments[i+1][1]-data_segments[i][1])
                )
            else:
                pass

        timing_conversion = self.create_mapping(timing_segments)
        key_list = timing_conversion.keys()
        try:
            for seg in timing_segments:
                if seg[1] in key_list:
                    self.message_in += timing_conversion[seg[1]]
                else:
                    for i in range(-100,100):
                        if seg[1]+i in key_list:
                            self.message_in += timing_conversion[seg[1]+i]
        except KeyError:
            print("Potential bad data.\n"
                        f"No matching conversion found for {seg}")


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
                if symbol in (" ", "|"):
                    data_frames = self.create_frames(
                        duration=SIGNAL_CONVERSION[symbol],
                        volume=0
                    )
                else:
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


    def create_mapping(self, timings):
        unique_timings = list(set(timings))
        pause_intervals = [timing[1]
                           for timing in unique_timings 
                           if timing[0] == "off"]
        pause_intervals.sort()

        signal_intervals = [timing[1]
                           for timing in unique_timings 
                           if timing[0] == "on"]
        signal_intervals.sort()

        mapping = {
            signal_intervals[0]: ".",
            signal_intervals[1]: "-",
            pause_intervals[0]: "",
            pause_intervals[1]: " ",
            pause_intervals[2]: " | ",
        }

        return mapping
