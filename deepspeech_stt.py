#!/usr/bin/env python3
"""
This script will use deepspeech and convert the audio file to text
author: sachin2001g@gmail.com
"""
import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave
import json
import time
import deepspeech

from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

MODEL_PATH = "deepspeech-0.9.3-models.pbmm"
SCORER_PATH = "deepspeech-0.9.3-models.scorer"


def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(
        quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno,
                      'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)


def main():
    parser = argparse.ArgumentParser(description='Speech to text using deepspeech')
    parser.add_argument('--audio', required=True, help='Path to the audio file to run (WAV format)')
    args = parser.parse_args()
    audio_path = args.audio
    # initialise model
    model = deepspeech.Model(MODEL_PATH)
    # configure scorer
    model.enableExternalScorer(SCORER_PATH)
    fin = wave.open(audio_path, 'rb')
    fs_orig = fin.getframerate()
    desired_sample_rate = model.sampleRate()
    fs_new, audio = convert_samplerate(audio_path, desired_sample_rate)
    audio_length = fin.getnframes() * (1 / fs_orig)
    print("audio-length {}".format(str(audio_length)))
    output_text = model.stt(audio)
    print(output_text)
    file_name = "{}_text_{}.txt".format(audio_path.split("/")[-1], str(time.time()))
    output_text_file = open(file_name, "a")
    output_text_file.write(output_text)
    output_text_file.close()


if __name__ == '__main__':
    main()