import subprocess
import time
import numpy as np
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


MODEL_PATH = "deepspeech-0.9.3-models.pbmm"
SCORER_PATH = "deepspeech-0.9.3-models.scorer"
model = predict.load_model('nsfw.299x299.h5')
ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"

app = Flask(__name__)

class speech_to_text:
    def __init__(self, video_file):
        self.video_file = video_file
        self.video_file_name = self.video_file.split('.')[0]

    def VideoToText(self):

        video = self.video_file

        command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000", "-ar", "16000", "temp_output.wav"]
        video_to_audio = subprocess.check_output(command, shell=True)

        audio_filename = 'temp_output.wav'
        proc = subprocess.Popen(
            f"deepspeech --model {MODEL_PATH}  --audio " + audio_filename,
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
        word_list_df = self.ProfaneWordList()
        profane_words_list = []
        for words in word_list_df:
            if words in video_text:
                profane_words_list.append(words)
        return f'{self.video_file} has approximately {len(profane_words_list)} number of profane words and profane words in speech are {profane_words_list}!!!'
        pass

    def MakeImageDirectory(self):
        vidObj = cv.VideoCapture(self.video_file)
        self.video_file_name = self.video_file.split('.')[0]
        try:
            os.mkdir(self.video_file_name)

        except Exception as e:
            print(f'Execption in making directory: {e}')

        count = 0
        success = 1
        fps = vidObj.get(cv.CAP_PROP_FPS)
        while success:
            try:
                success, image = vidObj.read()
                count += 1
                if count % (int(fps) * 2) == 0:
                    # if count % 300 == 0:
                    cv.imwrite("{}\\{}_frame_{}.jpg".format(self.video_file_name, self.video_file_name, count), image)
            except Exception as e:
                print(f'Exeception: {e}')
                pass

    def VideoClassifyResult(self):
        self.MakeImageDirectory()
        self.video_file_name = self.video_file.split('.')[0]
        files = glob('{}/*'.format(self.video_file_name))
        num_images_in_folder = len(files)
        result = predict.classify(model, '{}/'.format(self.video_file_name))
        count_unsafe = 0
        for key in result.keys():
            if (max(result[key].items(), key=operator.itemgetter(1))[0] == 'porn') or (
                    max(result[key].items(), key=operator.itemgetter(1))[0] == 'sexy'):
                count_unsafe += 1
        percent_unsafe = round(count_unsafe / num_images_in_folder * 100, 2)
        if percent_unsafe > 50:
            return (f'{self.video_file} is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
        elif (percent_unsafe > 30) & (percent_unsafe <= 50):
            return (
                f'{self.video_file} is categorized as: "ADMIN HAS TO VERIFY", since percentage of unsafe images: {percent_unsafe}%')
        elif (percent_unsafe > 20) & (percent_unsafe <= 30):
            return (
                f'{self.video_file} is categorized as: "ADMIN CAN VERIFY or IGNORE", since percentage of unsafe images: {percent_unsafe}%')
        else:
            return (f'{self.video_file} is categorized as: "SAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
        pass

    def CompressVideo(self):
        command_10 = [f"{ffmpeg_location}",
                      "-i", f"{self.video_file}", "-vcodec", "libx264", "-crf", "30", "-preset", "fast",
                      f"{self.video_file_name}_compress.mp4"]
        compress_video = subprocess.check_output(command_10, shell=True)
        with open( f"{self.video_file_name}_compress.mp4", "rb") as videoFile:
            text = base64.b64encode(videoFile.read()).decode('utf-8')
        os.remove(f"{self.video_file_name}_compress.mp4")
        return text

    def TextAndClassity(self):
        start = time.perf_counter()
        text_result = self.TextResult()
        safe_image_result = self.VideoClassifyResult()
        compress_video_base64 = self.CompressVideo()
        # delete the directory created to store the frames
        shutil.rmtree(self.video_file_name)
        finish = time.perf_counter()
        print(f'Finished in {round(finish - start, 2)} seconds(s) ')
        return text_result, safe_image_result, compress_video_base64




@app.route('/video/upload', methods=['POST'])
def Main():
    if request.method == 'POST':
        file = request.files['file']
        print('Filename: ',file.filename)
        check = speech_to_text(file.filename)
        # print(check.TextResult())
        # check.MakeImageDirectory()
        text_result, safe_image_result, text_base64 = check.TextAndClassity()

        return {"Transcript_result": text_result,
                'Video content result': safe_image_result,
                "videoBase64": text_base64}




if __name__ == "__main__":
    app.run()
# filename = 'sample'
# print(f"{filename}_compress.mp4")