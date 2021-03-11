import subprocess
import time
import pandas as pd
import pickle
import os
import cv2 as cv
from glob import glob
import predict
import operator
import shutil
from flask import Flask, request
import base64


# MODEL_PATH = "deepspeech-0.9.3-models.pbmm"
# SCORER_PATH = "deepspeech-0.9.3-models.scorer"
# model = predict.load_model('nsfw.299x299.h5')
# ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"
#
# app = Flask(__name__)
#
# class speech_to_text:
#     def __init__(self, video_file):
#         self.video_file = video_file
#         self.video_file_name = self.video_file.split('.')[0]
#
#     def VideoToText(self):
#
#         video = self.video_file
#         print(video)
#         command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000", "-ar", "16000", "temp_output.wav"]
#         video_to_audio = subprocess.check_output(command, shell=True)
#
#         audio_filename = 'temp_output.wav'
#         proc = subprocess.Popen(
#             f"deepspeech --model {MODEL_PATH}  --audio " + audio_filename,
#             shell=True, stdout=subprocess.PIPE, )
#         output = proc.communicate()[0]
#         # os.remove("temp_output.wav")
#
#         return output
#
#     def ProfaneWordList(self):
#         try:
#             with open(file='data.pickle', mode='rb') as file:
#                 word_list_df = pickle.load(file)
#         except:
#             df = pd.read_csv('profane_word_list.txt', header=None)
#             word_list_df = [words for words in df.iloc[:, -1]]
#
#             with open('data.pickle', mode='wb') as file:
#                 pickle.dump(word_list_df, file)
#
#         return word_list_df
#
#     def TextResult(self):
#         video_text = self.VideoToText()
#         video_text = video_text.decode('utf-8')
#         word_list_df = self.ProfaneWordList()
#         profane_words_list = []
#         for words in word_list_df:
#             if words in video_text:
#                 profane_words_list.append(words)
#         return f'{self.video_file} has approximately {len(profane_words_list)} number of profane words and profane words in speech are {profane_words_list}!!!'
#         pass
#
#
# start = time.perf_counter()
# a = speech_to_text('obama.mp4')
# a.TextResult()
# finish = time.perf_counter()
# print(f'Finished in {round(finish - start, 2)} seconds(s) ')

# !deepspeech --model deepspeech-0.6.1-models/output_graph.pbmm --lm deepspeech-0.6.1-models/lm.binary --trie deepspeech-0.6.1-models/trie --audio test.wav
MODEL_PATH = "deepspeech-0.6.1-models/output_graph.pbmm"
LM_PATH = "deepspeech-0.6.1-models/lm.binary"
TRIE_PATH = "deepspeech-0.6.1-models/trie"
ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"


class speech_to_text:
    def __init__(self, video_file):
        self.video_file = video_file
        self.video_file_name = self.video_file.split('.')[0]

    def VideoToText(self):

        video = self.video_file
        print(video)
        command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000", "-ar", "16000", "temp_output.wav"]
        video_to_audio = subprocess.check_output(command, shell=True)

        audio_filename = 'temp_output.wav'
        # deepspeech_command = f"deepspeech --model {MODEL_PATH}  --audio " + audio_filename
        deepspeech_command = f"deepspeech --model {MODEL_PATH} --lm {LM_PATH}  --trie {TRIE_PATH} --audio " + audio_filename
        proc = subprocess.Popen(
            deepspeech_command,
            shell=True, stdout=subprocess.PIPE, )
        output = proc.communicate()[0]
        os.remove("temp_output.wav")

        return output

    def ProfaneWordList(self):
        try:
            with open(file='data.pickle', mode='rb') as file:
                word_list_df = pickle.load(file)
        except:
            df = pd.read_csv('profane_word_list.txt', header=None)
            word_list_df = [words for words in df.iloc[:, -1]]

            with open('data.pickle', mode='wb') as file:
                pickle.dump(word_list_df, file)

        return word_list_df

    def TextResult(self):
        video_text = self.VideoToText()
        video_text = video_text.decode('utf-8')
        print(video_text)
        # word_list_df = self.ProfaneWordList()
        # profane_words_list = []
        # for words in word_list_df:
        #     if words in video_text:
        #         profane_words_list.append(words)
        # return f'{self.video_file} has approximately {len(profane_words_list)} number of profane words and profane words in speech are {profane_words_list}!!!'
        # pass


if __name__ == "__main__":
    start = time.perf_counter()
    a = speech_to_text('obama.mp4')
    a.TextResult()
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} seconds(s) ')