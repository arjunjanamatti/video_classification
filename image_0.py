import os
import cv2 as cv
import time
from glob import glob
import concurrent.futures
import predict
import operator

image_directory = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/uploads'
images_list = glob(f'{image_directory}/*')
print(images_list)

model = predict.load_model('nsfw.299x299.h5')

def process_image(image):
    result = predict.classify(model, image)
    # img = cv.imread(filename=image)
    # gray_image = cv.cvtColor(src=img,code=cv.COLOR_BGR2GRAY)
    for key in result.keys():
        image_name = (key.split("\\")[-1]).split(".")[0]
        if (max(result[key].items(), key=operator.itemgetter(1))[0] == 'porn') or (
                max(result[key].items(), key=operator.itemgetter(1))[0] == 'sexy'):
            print(f' {image_name} image has high chance of UNSAFE content !!!')
        else:
            print(f' {image_name} image has high chance of SAFE content !!!')


def CheckConcurrent():
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image,images_list)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')

if __name__ == '__main__':
    # check_time()
    CheckConcurrent()