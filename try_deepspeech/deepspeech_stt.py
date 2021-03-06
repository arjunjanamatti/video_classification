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
audio_path = input('Enter the audio file path: ')

import numpy as np
from scipy.io import wavfile
from scipy import interpolate

NEW_SAMPLERATE = 16000

old_samplerate, old_audio = wavfile.read(audio_path)

print(f'Original sample rate: {old_samplerate}')

# if old_samplerate != NEW_SAMPLERATE:
#     duration = old_audio.shape[0] / old_samplerate
#
#     time_old  = np.linspace(0, duration, old_audio.shape[0])
#     time_new  = np.linspace(0, duration, int(old_audio.shape[0] * NEW_SAMPLERATE / old_samplerate))
#
#     interpolator = interpolate.interp1d(time_old, old_audio.T)
#     new_audio = interpolator(time_new).T
#
#     wavfile.write("out.wav", NEW_SAMPLERATE, np.round(new_audio).astype(old_audio.dtype))

new_samplerate, new_audio = wavfile.read("out.wav")

print(f'Changed sample rate: {new_samplerate}')

model = deepspeech.Model(MODEL_PATH)
# configure scorer
model.enableExternalScorer(SCORER_PATH)
lm_alpha = 0.75
lm_beta = 1.85
# model.enableDecoderWithLM(lm_file_path, trie_file_path, lm_alpha, lm_beta)
print(model.sampleRate())
filename = 'out.wav'
w = wave.open(filename, 'rb')
rate = w.getframerate()
frames = w.getnframes()
buffer = w.readframes(frames)
data16 = np.frombuffer(buffer, dtype=np.int16)
text = model.stt(data16)
print(text)
# np.frombuffer()

# def convert_samplerate(audio_path, desired_sample_rate):
#     sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(
#         quote(audio_path), desired_sample_rate)
#     try:
#         output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
#     except subprocess.CalledProcessError as e:
#         raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
#     except OSError as e:
#         raise OSError(e.errno,
#                       'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))
#
#     return desired_sample_rate, np.frombuffer(output, np.int16)
#
#
# def main(audio_path):
#     # parser = argparse.ArgumentParser(description='Speech to text using deepspeech')
#     # parser.add_argument('--audio', required=True, help='Path to the audio file to run (WAV format)')
#     # args = parser.parse_args()
#     # audio_path = args.audio
#     # # initialise model
#     model = deepspeech.Model(MODEL_PATH)
#     # configure scorer
#     model.enableExternalScorer(SCORER_PATH)
#     fin = wave.open(audio_path, 'rb')
#     fs_orig = fin.getframerate()
#     desired_sample_rate = model.sampleRate()
#     fs_new, audio = convert_samplerate(audio_path, desired_sample_rate)
#     audio_length = fin.getnframes() * (1 / fs_orig)
#     print("audio-length {}".format(str(audio_length)))
#     print("Audio: ", audio)
#     output_text = model.stt(audio)
#     print(output_text)
#     file_name = "{}_text_{}.txt".format(audio_path.split("/")[-1], str(time.time()))
#     output_text_file = open(file_name, "a")
#     output_text_file.write(output_text)
#     output_text_file.close()
#
#
# if __name__ == '__main__':
#     main(audio_path)