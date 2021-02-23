import os
import cv2 as cv
import time
from glob import glob
import concurrent.futures
import predict
import operator

model = predict.load_model('nsfw.299x299.h5')

image_directory = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/uploads'
# storing the frames from training videos
frames_directory_name = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/frames_from_videos'
# getting names of all videos
# check_videos = input('Enter "safe" to check safe videos and "unsafe" to check unsafe videos: ')
check_videos = 'unsafe'
videos_list = glob(f'C:\\Users\\Arjun Janamatti\\PycharmProjects\\jeeva_project\\video_and_image_classification\\upload_videos\\{check_videos}\\*')
video_filename_list = [((video.split("\\")[-1]).split("\\")[-1]).split('.')[0] for video in videos_list]
# print(video_filename_list)

sample_test_list = ["C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/upload_videos/unsafe\\#Open_desi_sexy_video\u200b sexy girl_Hindi sexy video pron video sex video sexy' Blu film xvideose_BF.mp4"]

print(videos_list)

for file in video_filename_list:
    print(file)

def remove_punctuations(string):
    # define punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    my_str = string

    # To take input from the user
    # my_str = input("Enter a string: ")

    # remove punctuation from the string
    no_punct = ""
    for char in my_str:
        if char not in punctuations:
            no_punct = no_punct + char

    # display the unpunctuated string
    return no_punct

def make_image_directory(video):
    vidObj = cv.VideoCapture(video)
    video_file_name = ((video.split("\\")[-1]).split("\\")[-1]).split('.')[0]
    video_file_name = remove_punctuations(video_file_name)
    try:
        os.mkdir(video_file_name)

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
                cv.imwrite("{}/{}_frame_{}.jpg".format(video_file_name, video_file_name, count), image)
                # print(video_file_name, count)
        except Exception as e:
            print(f'Exeception: {e}')
            pass


def video_process_updated(video):
    files = glob('{}/*'.format(video))
    # print(files)
    # for file in files:
    #     print(file)
    num_images_in_folder = len(files)
    result = predict.classify(model, '{}/'.format(video))
    count_unsafe = 0
    for key in result.keys():
        if (max(result[key].items(), key=operator.itemgetter(1))[0] == 'porn') or (
                max(result[key].items(), key=operator.itemgetter(1))[0] == 'sexy'):
            count_unsafe += 1
    percent_unsafe = round(count_unsafe / num_images_in_folder * 100, 2)
    print(video, percent_unsafe)
    if percent_unsafe > 50:
        print(f'{video} is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
    elif (percent_unsafe > 30) & (percent_unsafe <= 50):
        print(f'{video} is categorized as: "ADMIN HAS TO VERIFY", since percentage of unsafe images: {percent_unsafe}%')
    elif (percent_unsafe > 20) & (percent_unsafe <= 30):
        print(f'{video} is categorized as: "ADMIN CAN VERIFY or IGNORE", since percentage of unsafe images: {percent_unsafe}%')
    else:
        print(f'{video} is categorized as: "SAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
    pass

def video_process(video):
    percent_unsafe = 0
    vidObj = cv.VideoCapture(video)
    # print(f'Video: {video} ')
    video_file_name = ((video.split("/")[-1]).split("\\")[-1]).split('.')[0]
    count = 0
    success = 1
    fps = vidObj.get(cv.CAP_PROP_FPS)
    while success:
        try:
            success, image = vidObj.read()
            count += 1
            if count%(int(fps)*2)==0:
            # if count % 300 == 0:
            #     cv.imwrite("{}/{}_frame_{}.jpg".format(frames_directory_name,video_file_name, count), image)
                print(video_file_name, image.shape)
        except Exception as e:
            print(f'Exeception: {e}')
            pass
    # files = glob('{}/*'.format(frames_directory_name))
    # num_images_in_folder = len(files)
    # print(video_file_name, num_images_in_folder)
    # # result = predict.classify(model, '{}/'.format(frames_directory_name))
    # for file in files:
    #     os.remove(file)
    # count_unsafe = 0
    # for key in result.keys():
    #     if (max(result[key].items(), key=operator.itemgetter(1))[0] == 'porn') or (
    #             max(result[key].items(), key=operator.itemgetter(1))[0] == 'sexy'):
    #         count_unsafe += 1
    #
    #
    # # column_a.append(count_unsafe)
    # # column_b.append(num_images_in_folder)
    # percent_unsafe = round(count_unsafe / num_images_in_folder * 100, 2)
    # # print(video_file_name, percent_unsafe)
    # if percent_unsafe > 50:
    #     print(f'{video_file_name} is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
    # elif (percent_unsafe > 30) & (percent_unsafe <= 50):
    #     print(f'{video_file_name} is categorized as: "ADMIN HAS TO VERIFY", since percentage of unsafe images: {percent_unsafe}%')
    # elif (percent_unsafe > 20) & (percent_unsafe <= 30):
    #     print(f'{video_file_name} is categorized as: "ADMIN CAN VERIFY or IGNORE", since percentage of unsafe images: {percent_unsafe}%')
    # else:
    #     print(f'{video_file_name} is categorized as: "SAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')


def CheckConcurrent():
    start = time.perf_counter()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(video_process,videos_list[:2])

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(make_image_directory,videos_list)

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(video_process_updated,video_filename_list[:15])

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')

if __name__ == '__main__':
    # check_time()
    CheckConcurrent()


