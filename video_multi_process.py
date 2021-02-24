import os
import cv2 as cv
import time
from glob import glob
import concurrent.futures
import predict
import operator
import shutil

model = predict.load_model('nsfw.299x299.h5')
current_main_directory = 'C:/Users/Arjun Janamatti/PycharmProjects/video_classification/'

image_directory = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/uploads'
# storing the frames from training videos
frames_directory_name = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/frames_from_videos'
# getting names of all videos
# check_videos = input('Enter "safe" to check safe videos and "unsafe" to check unsafe videos: ')
check_videos = 'unsafe'
videos_main_directory = f'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/upload_videos/{check_videos}/'
videos_list = glob(f'C:\\Users\\Arjun Janamatti\\PycharmProjects\\jeeva_project\\video_and_image_classification\\upload_videos\\{check_videos}\\*')
video_filename_list = [((video.split("\\")[-1]).split("\\")[-1]).split('.')[0] for video in videos_list[:10]]
# print(video_filename_list)

sample_test_list = ["C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/upload_videos/unsafe\\#Open_desi_sexy_video\u200b sexy girl_Hindi sexy video pron video sex video sexy' Blu film xvideose_BF.mp4"]

# print(videos_list)
#
# for file in video_filename_list:
#     print(file)

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
                cv.imwrite("{}\\{}_frame_{}.jpg".format(video_file_name, video_file_name, count), image)
                # print(video_file_name, count)
        except Exception as e:
            print(f'Exeception: {e}')
            pass


def video_process_updated(video):
    video = remove_punctuations(video)
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

def check_and_update_empty_directory(videos_list, video_filename_list):
    no_jpg_dir_list = []
    for video in videos_list:
        vidObj = cv.VideoCapture(video)
        video_file_name = ((video.split("\\")[-1]).split("\\")[-1]).split('.')[0]
        video_file_name = remove_punctuations(video_file_name)
        video_file_name = video_file_name.strip()
        # if os.listdir(video_file_name):
        #     print()
        # else:
        #     print(f'{video_file_name} is empty')
        #     count = 0
        #     success = 1
        #     fps = vidObj.get(cv.CAP_PROP_FPS)
        #     while success:
        #         try:
        #             success, image = vidObj.read()
        #             count += 1
        #             if count % (int(fps) * 2) == 0:
        #                 # if count % 300 == 0:
        #                 cv.imwrite(f"{video_file_name}/{video_file_name}_frame_{count}.jpg", image)
        #                 # cv.imshow(winname='trial_image', mat=image)
        #                 # cv.waitKey(0)
        #                 # print("{}/{}_frame_{}.jpg".format(video_file_name, video_file_name, count))
        #         except Exception as e:
        #             print(f'Exception: {e}')
        if not os.listdir(video_file_name):
            no_jpg_dir_list.append(video)
            shutil.rmtree(video_file_name)

    return no_jpg_dir_list

def for_loop_use_result(no_jpg_dir_list):
    for video in no_jpg_dir_list:
        # print('Video path in for loop: ', videos_main_directory+video)
        vidObj = cv.VideoCapture(video)
        video_file_name = ((video.split("\\")[-1]).split("\\")[-1]).split('.')[0]
        video_file_name = remove_punctuations(video_file_name)
        video_file_name = video_file_name.strip()
        count = 0
        success = 1
        fps = vidObj.get(cv.CAP_PROP_FPS)
        while success:
            try:
                success, image = vidObj.read()
                count += 1
                if count % (int(fps) * 2) == 0:
                    # if count % 300 == 0:
                    cv.imwrite("{}/{}_frame_{}.jpg".format(frames_directory_name, video_file_name, count), image)
            except:
                pass

        files = glob('{}/*'.format(frames_directory_name))
        num_images_in_folder = len(files)
        result = predict.classify(model, '{}/'.format(frames_directory_name))
        for file in files:
            os.remove(file)
        count_unsafe = 0
        for key in result.keys():
            if (max(result[key].items(), key=operator.itemgetter(1))[0] == 'porn') or (
                    max(result[key].items(), key=operator.itemgetter(1))[0] == 'sexy'):
                count_unsafe += 1

        percent_unsafe = round(count_unsafe / num_images_in_folder * 100, 2)
        if percent_unsafe > 50:
            print(
                f'{video_file_name} is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
        elif (percent_unsafe > 30) & (percent_unsafe <= 50):
            print(
                f'{video_file_name} is categorized as: "ADMIN HAS TO VERIFY", since percentage of unsafe images: {percent_unsafe}%')
        elif (percent_unsafe > 20) & (percent_unsafe <= 30):
            print(
                f'{video_file_name} is categorized as: "ADMIN CAN VERIFY or IGNORE", since percentage of unsafe images: {percent_unsafe}%')
        else:
            print(
                f'{video_file_name} is categorized as: "SAFE VIDEO", since percentage of unsafe images: {percent_unsafe}%')
    pass

def delete_directories(video_filename_list):
    for folder_name in video_filename_list:
        video_file_name = remove_punctuations(folder_name)
        video_file_name = video_file_name.strip()
        shutil.rmtree(video_file_name)

    pass

def CheckConcurrent():
    start = time.perf_counter()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(video_process,videos_list[:2])

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(make_image_directory,videos_list[:10])
    no_jpg_dir_list = check_and_update_empty_directory(videos_list[:10], video_filename_list)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(video_process_updated,video_filename_list)
    for_loop_use_result(no_jpg_dir_list)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')

if __name__ == '__main__':
    # check_time()
    CheckConcurrent()
# check_and_update_empty_directory(videos_list, video_filename_list)


#BreastFeeding Hand Expression  Saving Milk for Baby    BreastFeeding Hand Expression Tips Method 86.67
# BreastFeeding Hand Expression  Saving Milk for Baby    BreastFeeding Hand Expression Tips Method is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: 86.67%
# Hot Romantic Video  Suhaag Raat  Sexy Video  Hot Web Series  Sex Video  Devar Bhabhi Ki Chudai 83.87
# Hot Romantic Video  Suhaag Raat  Sexy Video  Hot Web Series  Sex Video  Devar Bhabhi Ki Chudai is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: 83.87%
# Devar Hot Blue Sexy Blue Film Hot And Sexy Video 2021 Bhabhi Devar Hot Movie Hot Desi Indian 51.03
# Devar Hot Blue Sexy Blue Film Hot And Sexy Video 2021 Bhabhi Devar Hot Movie Hot Desi Indian is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: 51.03%
# Shilpa Shetty  Best Romantic Scenes  Hindi Movie SHILPA THE BIGGDON 720p HD 51.82
# Shilpa Shetty  Best Romantic Scenes  Hindi Movie SHILPA THE BIGGDON 720p HD is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: 51.82%
# Best New Teacher And Student Sex Scene Full Web Series 2020 52.48
# Best New Teacher And Student Sex Scene Full Web Series 2020 is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: 52.48%
# bangla hot video 2020 sex free video xx 2020 HD hot videobangla new xx videos 2020 Part 1 17.02
# bangla hot video 2020 sex free video xx 2020 HD hot videobangla new xx videos 2020 Part 1 is categorized as: "SAFE VIDEO", since percentage of unsafe images: 17.02%
# Best Ullu Web Series Romantic sex Scene  Hot Scene Full Hd Movie  Sexy Kiss Video 55.05
# Best Ullu Web Series Romantic sex Scene  Hot Scene Full Hd Movie  Sexy Kiss Video is categorized as: "UNSAFE VIDEO", since percentage of unsafe images: 55.05%
# #