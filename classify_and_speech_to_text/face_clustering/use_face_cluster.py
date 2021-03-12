import subprocess
import time
import pandas as pd
import pickle
import os
import cv2 as cv
from glob import glob
import predict
import operator
import shutil
from flask import Flask, request
import base64


# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection_method "cnn"
command = ['python','encode_faces.py']
a = subprocess.run(command, shell=True)

class speech_to_text:
    def __init__(self, video_file):
        self.video_file = video_file
        self.video_file_name = self.video_file.split('.')[0]

    def MakeImageDirectory(self):
        vidObj = cv.VideoCapture(self.video_file)
        self.video_file_name = self.video_file.split('.')[0]
        try:
            os.mkdir(self.video_file_name)

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
                    cv.imwrite("{}\\{}_frame_{}.jpg".format(self.video_file_name, self.video_file_name, count), image)
            except Exception as e:
                print(f'Exeception: {e}')
                pass

    def ExtractFaces(self, image, neighbors=3):
        img = cv.imread(filename=image)
        image_filename = image.split('\\')[-1]
        video_filename = image.split('\\')[0]
        # convert to grayscale image
        gray_image = cv.cvtColor(src=img, code=cv.COLOR_BGR2GRAY)
        # call the har cascade xml file
        har_cas = cv.CascadeClassifier('har_face.xml')
        # detect faces
        face_detect = har_cas.detectMultiScale(image=gray_image, scaleFactor=1.1, minNeighbors=neighbors)
        for (x, y, w, h) in face_detect:
            cv.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), thickness=2, color=(0, 255, 0))
            roi_color = img[y:y + h, x:x + w]
            print(str(video_filename) + "\\faces\\" + str(image_filename) + str(x) + str(w) + str(h) + '_faces.jpg')
            cv.imwrite(
                str(video_filename) + "\\faces\\" + str(image_filename) + str(x) + str(w) + str(h) + '_faces.jpg',
                roi_color)

    def Check(self):
        # self.MakeImageDirectory()
        os.mkdir(f'{self.video_file_name}/faces')
        images_list = glob(f'{self.video_file_name}/*.jpg')
        print(images_list)
        for image in images_list:
            self.ExtractFaces(image)
        pass

    def UseFaceCluster(self):
        self.MakeImageDirectory()
        command = ['python', 'encode_faces.py', '--dataset', f'{self.video_file_name}', '--encodings', f'{self.video_file_name}.pickle', '--detection_method', 'hog']
        a = subprocess.run(command, shell=True)
        pass



a = speech_to_text('sample.mp4')
a.Check()

