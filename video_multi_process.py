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