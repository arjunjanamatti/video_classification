import subprocess
import time
import numpy as np
import pandas as pd
import pickle

MODEL_PATH = "deepspeech-0.9.3-models.pbmm"
SCORER_PATH = "deepspeech-0.9.3-models.scorer"
def generate(filename):
    'ffmpeg -i trial_copy.mp4 -ac 1 -ab 16000 -ar 16000 output.wav'
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
    print(output)
    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} seconds(s) ')
    return output



# post("static/img/chunk278.wav")

def generate_their(filename):
    proc = subprocess.Popen(
        "deepspeech --model models/output_graph.pbmm   --lm /home/udaram/Desktop/TCS_Internship/try-Kenlm/combined_corpus.binary --trie /home/udaram/Desktop/TCS_Internship/DeepspeechModel/trie --audio " + filename,
        shell=True, stdout=subprocess.PIPE, )
    output = proc.communicate()[0]
    print(output)

    return output
# filename = 'sample_video.mp4'
# generate(filename)

# word_list = np.loadtxt('profane_word_list.txt')
# print(word_list)
word_list = []
with open('profane_word_list.txt') as file:
    word_list.append(file.read())

print(word_list)
word_list_df = []
df = pd.read_csv('profane_word_list.txt', header = None)
print(df)
word_list_df = [words for words in df.iloc[:,-1]]
print(word_list_df)

# filename = 'sample_video.mp4'
# generate(filename)


# 'ffmpeg -i trial_copy.mp4 -ac 1 -ab 16000 -ar 16000 output.wav'
# ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"
#
# video = 'med_video.mp4'
# start = time.perf_counter()
# command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000","-ar", "16000","temp_output.wav"]
# compress_video = subprocess.check_output(command, shell=True)
# finish = time.perf_counter()
#
# print(f'Finished in {round(finish-start, 2)} seconds(s) ')