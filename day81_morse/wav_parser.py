import wave
from morse_utils import decoder, input_validator

class WavParser:


    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
