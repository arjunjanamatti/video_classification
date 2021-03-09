import subprocess
import time
import numpy as np
import pandas as pd
import pickle

MODEL_PATH = "deepspeech-0.9.3-models.pbmm"
SCORER_PATH = "deepspeech-0.9.3-models.scorer"
def generate(filename):
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

    print(f'Finished in {round(finish - start, 2)} seconds(s) ')
    return output


# # filename = 'sample_video.mp4'
# # generate(filename)
#
# # word_list = np.loadtxt('profane_word_list.txt')
# # print(word_list)
# word_list = []
# with open('profane_word_list.txt') as file:
#     word_list.append(file.read())
#
# print(word_list)

df = pd.read_csv('profane_word_list.txt', header = None)
print(df)
word_list_df = [words for words in df.iloc[:,-1]]
print(word_list_df)

# filename = 'sample.mp4'
# video_text = generate(filename)
# video_text = video_text.decode('utf-8')
# print(video_text)
video_text = "allow everybody who i con do tory second cily dot com the easiest and the finest way to get your jobs suf light allo i am unclta and i 'm going to tell you some simple dilint to make your widiou cvy to reat so woine of a one is you have to well foms you have to look con firent and copession to no more about bomwers please seck ur bloo for an eveto was you have to take care of your lucation blease toos and noise free lookation they care of your bacglong it hould be ready need in dice poin but three years to leave min dela good boy woster stands trave look onfident look right into the gamblor that obviously leads to poind of aport at wou have to make a good ey condact with a gan please wol get a cam with up and not to the cream point bo bivis pleas tak care of your voice bit i'm don't lease don bet too loud tal arman olies we and ter the aspect wer thespees thes temply thrust me all yu need ot e good tory seconds stop on with your with e polite greating tell your name about your cario trustpacts tarbolli e case in tacround talavod yon lo cas in your colen jop pasison and trust me fer a fresh our don to warit not that difficult e can talk about you intone sip your education what do you loane in collegitet itcepra don wony it caraby simple okay the last is that if half to smile through watoveryou trust me mile luly heads it come you confidence okay sa a smiling of ir you is a very positive tood so let go to the quickly cap you have to wears nice formood thak care of your back round think in of your boy poster i con tack with the camoa your voice don'twon anfit please smile dowards the end dis he stor n thorty second se we thot gome and get going al the best"

for words in word_list_df:
    if words in video_text:
        print(words)

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