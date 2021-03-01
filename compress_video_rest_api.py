from flask import Flask, request, jsonify
import cv2
import base64
import os
import subprocess
from werkzeug.utils import secure_filename
import shutil


def assure_path_exists(upload_path, output_path):
    dir_upload = os.path.dirname(upload_path)
    if not os.path.exists(dir_upload):
        os.makedirs(dir_upload)
    dir_output = os.path.dirname(output_path)
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)


assure_path_exists("compress_video_upload/", "compress_video_output/")

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "compress_video_upload"

ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"


@app.route('/video/upload', methods=['POST'])
def Classification():
    if request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        file_path = 'video_uploads'+ secure_filename(file.filename)
        file.save(file_path)

        # start = time.perf_counter()
        command = [ffmpeg_location, "-i", f"{file_path}", "-vcodec", "libx264", "-crf", "45", "temp_output.mp4"]
        compress_video = subprocess.check_output(command, shell=True)
        # finish = time.perf_counter()
        # print(f'Finished in {round(finish-start, 2)} seconds(s) ')
        with open("temp_output.mp4", "rb") as videoFile:
            text = base64.b64encode(videoFile.read()).decode('utf-8')
            print(text)

        return {"videoBase64": text}


if __name__ == "__main__":
    app.run()