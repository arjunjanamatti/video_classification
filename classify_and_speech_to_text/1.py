import subprocess
import time
import numpy as np
import pandas as pd
import pickle
import os
from nltk.tokenize import sent_tokenize

MODEL_PATH = "deepspeech-0.9.3-models.pbmm"
SCORER_PATH = "deepspeech-0.9.3-models.scorer"


class speech_to_text:
    def __init__(self, video_file):
        self.video_file = video_file

    def VideoToText(self):
        ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"

        video = self.video_file
        start = time.perf_counter()
        command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000", "-ar", "16000", "temp_output.wav"]
        video_to_audio = subprocess.check_output(command, shell=True)

        audio_filename = 'temp_output.wav'
        proc = subprocess.Popen(
            f"deepspeech --model {MODEL_PATH}  --audio " + audio_filename,
            shell=True, stdout=subprocess.PIPE, )
        output = proc.communicate()[0]
        finish = time.perf_counter()
        os.remove("temp_output.wav")
        print(f'Finished in {round(finish - start, 2)} seconds(s) ')
        return output

    pass

def VideoToText(filename):
    ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"

    video = filename
    start = time.perf_counter()
    command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000","-ar", "16000","temp_output.wav"]
    compress_video = subprocess.check_output(command, shell=True)

    audio_filename = 'temp_output.wav'
    proc = subprocess.Popen(
        f"deepspeech --model {MODEL_PATH}  --audio " + audio_filename,
        shell=True, stdout=subprocess.PIPE, )
    output = proc.communicate()[0]
    finish = time.perf_counter()
    os.remove("temp_output.wav")
    print(f'Finished in {round(finish - start, 2)} seconds(s) ')
    return output

try:
    with open(file='data.pickle', mode='rb') as file:
        word_list_df = pickle.load(file)
except:
    df = pd.read_csv('profane_word_list.txt', header = None)
    print(df)
    word_list_df = [words for words in df.iloc[:,-1]]
    print(word_list_df)

    with open('data.pickle', mode='wb') as file:
        pickle.dump(word_list_df, file)


filename = 'sample.mp4'
video_text = VideoToText(filename)
video_text = video_text.decode('utf-8')
print(video_text)
print(len(video_text))
for words in word_list_df:
    if words in video_text:
        print(words)
