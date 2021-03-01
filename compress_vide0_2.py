from flask import Flask, request, jsonify
import cv2
import base64
import os
import subprocess
from werkzeug.utils import secure_filename


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


assure_path_exists("video_uploads/")

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "video_uploads"

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