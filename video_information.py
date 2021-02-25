import cv2 as cv
from glob import glob

check_videos = 'unsafe'
videos_list = glob(f'C:\\Users\\Arjun Janamatti\\PycharmProjects\\jeeva_project\\video_and_image_classification\\upload_videos\\{check_videos}\\*')
for video in videos_list:
    # # v=cv.VideoCapture(video)
    # # print(f'Video: {video} is of length: {v.get(cv.CAP_PROP_POS_MSEC)} seconds')
    vidObj = cv.VideoCapture(video)
    # seconds_duration = vidObj.get(cv.CAP_PROP_POS_MSEC)
    # print(seconds_duration)
    # fps = vidObj.get(cv.CAP_PROP_FPS)
    # print(fps)
    width = vidObj.get(cv.CAP_PROP_FRAME_WIDTH)
    height = vidObj.get(cv.CAP_PROP_FRAME_HEIGHT)
    fps = vidObj.get(cv.CAP_PROP_FPS) #bitrate
    totalNoFrames = vidObj.get(cv.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)
    print(f'width: {width}, height: {height}')
    print(f"bitrate: {fps}")
    print(f"durationInSeconds: {round(durationInSeconds, 2)} seconds")