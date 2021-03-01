import subprocess
import time
import base64
import cv2
from pathlib import Path

ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"

def compress_without_base_64(video):
    start = time.perf_counter()
    command = [ffmpeg_location, "-i", f"{video}", "-vcodec", "libx264", "-crf", "45", "temp_output.mp4"]
    compress_video = subprocess.check_output(command, shell=True)
    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')
    pass

def compress_wit_base_64(video):
    start = time.perf_counter()
    command = [ffmpeg_location, "-i", f"{video}", "-vcodec", "libx264", "-crf", "45", "temp_output.mp4"]
    compress_video = subprocess.check_output(command, shell=True)

    with open("temp_output.mp4", "rb") as videoFile:
        # CONVERT VIDEO TO BASE64
        text = base64.b64encode(videoFile.read())
        print(text)
        file = open("temp_output.txt", "wb")
        file.write(text)
        file.close()

        # CONVERT BASE64 TO VIDEO
        fh = open("video.mp4", "wb")
        fh.write(base64.b64decode(text))
        fh.close()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')
    pass

video = 'sample.mp4'
file = video
file_size = Path(file).stat().st_size
v = cv2.VideoCapture(file)
fps = v.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
duration_seconds = frame_count/fps
# duration_seconds = v.get(cv2.CAP_PROP_POS_MSEC)
actual_bitrate = file_size / duration_seconds
compressed_file_size = 0.1 * file_size
assigned_bitrate = compressed_file_size / duration_seconds
print(actual_bitrate, assigned_bitrate)
# compress_wit_base_64(video)