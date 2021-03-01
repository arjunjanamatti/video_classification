from flask import Flask, request, jsonify
import cv2
import base64
import os
import subprocess
from werkzeug.utils import secure_filename
import shutil
from pathlib import Path


def assure_path_exists(upload_path, output_path):
    dir_upload = os.path.dirname(upload_path)
    if not os.path.exists(dir_upload):
        os.makedirs(dir_upload)
    dir_output = os.path.dirname(output_path)
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)

def get_bitrate(file):
    file_size = Path(file).stat().st_size
    v = cv2.VideoCapture(file)
    duration_seconds = v.get(cv2.CAP_PROP_POS_MSEC)
    actual_bitrate = file_size/duration_seconds
    compressed_file_size = 0.1 * file_size
    assigned_bitrate = compressed_file_size/duration_seconds


assure_path_exists("compress_video_upload/", "compress_video_output/")

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "compress_video_upload/"

ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"


@app.route('/video/upload', methods=['POST'])
def Classification():
    if request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        upload_file_path = 'compress_video_upload/'+ secure_filename(file.filename)
        file.save(upload_file_path)

        # start = time.perf_counter()
        command = [ffmpeg_location, "-i", f"{upload_file_path}", "-vcodec", "libx264", "-crf", "45", "compress_video_output/temp_output.mp4"]

        # ffmpeg -y -i in.mp4 -codec:v libx264 -crf 23 -preset medium -codec:a libfdk_aac -vbr 4 -vf scale=-1:640,format=yuv420p out.mp4
        command_1 = [ffmpeg_location, "-y" ,"-i", f"{upload_file_path}", "-codec:v", "libx264", "-crf", "23",
                    "-preset", "medium", "-codec:a", "libfdk_aac","-vbr","4","-vf","scale=-1:640,format=yuv420p","compress_video_output/temp_output.mp4"]

        # ffmpeg -i input.mp4 -vf scale=320:240,setsar=1:1 output.mp4
        command_2 = [ffmpeg_location, "-i", f"{upload_file_path}", "-vf", "scale=320:240,setsar=1:1",
                   "compress_video_output/temp_output.mp4"]

        # ffmpeg -i data/video.mp4 -vcodec h264 -b:v 1000k -acodec mp2 data/output.mp4
        command_3 = [ffmpeg_location, "-i", f"{upload_file_path}", "-vcodec", "h264","-b:v", "20k","-acodec", "mp2",
                   "compress_video_output/temp_output.mp4"]

        # ffmpeg -i input.mp4 -vcodec h264 -acodec mp2 output.mp4
        command_4 = [ffmpeg_location, "-i", f"{upload_file_path}", "-vcodec", "h264","-acodec", "mp2",
                   "compress_video_output/temp_output.mp4"]
        compress_video = subprocess.check_output(command, shell=True)
        # finish = time.perf_counter()
        # print(f'Finished in {round(finish-start, 2)} seconds(s) ')
        with open("compress_video_output/temp_output.mp4", "rb") as videoFile:
            text = base64.b64encode(videoFile.read()).decode('utf-8')
            print(text)
        print(f'Size of output file {Path("compress_video_output/temp_output.mp4").stat().st_size}')
        shutil.rmtree("compress_video_upload")
        # shutil.rmtree("compress_video_output")

        return {"videoBase64": text}


if __name__ == "__main__":
    app.run()