import predict
import operator
import cv2 as cv
from glob import glob
import os
import time


model = predict.load_model('nsfw.299x299.h5')

# storing the frames from training videos
frames_directory_name = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/frames_from_videos'
# getting names of all videos
# check_videos = input('Enter "safe" to check safe videos and "unsafe" to check unsafe videos: ')
# videos_list = glob('C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/upload_videos/{}/*'.format(check_videos))

check_videos = 'unsafe'
videos_list = glob(f'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/upload_videos/{check_videos}/*')


result_statement = []
column_a, column_b = [], []

start = time.perf_counter()
for index, video in enumerate(videos_list[:15]):
    vidObj = cv.VideoCapture(video)
    video_file_name = (videos_list[index].split('\\')[-1]).split('.')[0]
    count = 0
    success = 1
    fps = vidObj.get(cv.CAP_PROP_FPS)
    while success:
        try:
            success, image = vidObj.read()
            count += 1
            if count%(int(fps)*2)==0:
            # if count % 300 == 0:
              cv.imwrite("{}/{}_frame_{}.jpg".format(frames_directory_name,video_file_name, count), image)
        except:
          pass

    files = glob('{}/*'.format(frames_directory_name))
    num_images_in_folder = len(files)
    print(video_file_name, num_images_in_folder)
    result = predict.classify(model, '{}/'.format(frames_directory_name))
    for file in files:
        os.remove(file)
    count_unsafe = 0
    for key in result.keys():
        if (max(result[key].items(), key=operator.itemgetter(1))[0] == 'porn') or (
                max(result[key].items(), key=operator.itemgetter(1))[0] == 'sexy'):
            count_unsafe += 1


    column_a.append(count_unsafe)
    column_b.append(num_images_in_folder)
    percent_unsafe = round(count_unsafe / num_images_in_folder * 100, 2)
    if percent_unsafe > 50:
        print(f'{video_file_name} is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
    elif (percent_unsafe > 30) & (percent_unsafe <= 50):
        print(f'{video_file_name} is categorized as: "ADMIN HAS TO VERIFY", since percentage of unsafe images: {percent_unsafe}%')
    elif (percent_unsafe > 20) & (percent_unsafe <= 30):
        print(f'{video_file_name} is categorized as: "ADMIN CAN VERIFY or IGNORE", since percentage of unsafe images: {percent_unsafe}%')
    else:
        print(f'{video_file_name} is categorized as: "SAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds(s) ')

