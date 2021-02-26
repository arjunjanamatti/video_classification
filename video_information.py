import cv2 as cv
from glob import glob
import subprocess

def get_bitrate(video):
    command = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", f"{video}", "-hide_banner"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    line_list = []
    for line in process.stdout:
        line_list.append(line)
    for line in line_list:
        if 'Duration' in line:
            __, _, bitrate = line.split(',')
            key_bitrate, value_bitrate = bitrate.split(':')
    return value_bitrate


check_videos = 'unsafe'
videos_list = glob(f'C:\\Users\\Arjun Janamatti\\PycharmProjects\\jeeva_project\\video_and_image_classification\\upload_videos\\{check_videos}\\*')
for video in videos_list:
    try:
        vidObj = cv.VideoCapture(video)
        width = vidObj.get(cv.CAP_PROP_FRAME_WIDTH)
        height = vidObj.get(cv.CAP_PROP_FRAME_HEIGHT)
        fps = vidObj.get(cv.CAP_PROP_FPS) #bitrate
        bitrate = get_bitrate(video)
        totalNoFrames = vidObj.get(cv.CAP_PROP_FRAME_COUNT)
        durationInSeconds = float(totalNoFrames) / float(fps)
        print(f'width: {width}, height: {height}')
        print(f"fps: {fps}")
        print(f'bitrate: {bitrate}' )
        print(f"durationInSeconds: {round(durationInSeconds, 2)} seconds")
    except:
        pass