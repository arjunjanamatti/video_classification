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
import random


# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection_method "cnn"
command = ['python','encode_faces.py']
a = subprocess.run(command, shell=True)

app = Flask(__name__)

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

    def MakeFaceDirectory(self):
        self.MakeImageDirectory()
        os.mkdir(f'{self.video_file_name}/faces')
        images_list = glob(f'{self.video_file_name}/*.jpg')
        print(images_list)
        for image in images_list:
            self.ExtractFaces(image)
        pass

    def UseFaceCluster(self):
        start = time.perf_counter()
        self.MakeFaceDirectory()
        command_encode_faces = ['python', 'encode_faces.py', '--dataset', f'{self.video_file_name}/faces', '--encodings', f'{self.video_file_name}.pickle', '--detection_method', 'hog']
        encode_f = subprocess.run(command_encode_faces, shell=True)
        command_cluster_faces = ['python', 'cluster_faces.py', '--encodings', f'{self.video_file_name}.pickle', '--jobs', '-1']
        encode_cl = subprocess.run(command_cluster_faces, shell=True)
        finish = time.perf_counter()
        print(f'Finished in {round(finish - start, 2)} seconds(s) ')

    def GetUniqueFacesDirectory(self):
        # get the names of all folders in directory
        my_dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
        # get the names of folders which have label in their names
        req_dirs = [dir for dir in my_dirs if 'label' in dir]
        try:
            # create a directory with label unique faces
            os.mkdir(f'unique_faces_{self.video_file.split(".")[0]}')
        except Exception as e:
            pass
        base_encoded_list = []
        for image in req_dirs:
            files = os.listdir(image)
            random_file = random.choice(files)
            shutil.move(image+'/'+random_file,f'unique_faces_{self.video_file.split(".")[0]}/')
            os.rename(f'unique_faces_{self.video_file.split(".")[0]}/{random_file}',f'unique_faces_{self.video_file.split(".")[0]}/unique_face_{image.split("_")[-1]}_{random_file}')
            with open(f'unique_faces_{self.video_file.split(".")[0]}/unique_face_{image.split("_")[-1]}_{random_file}', "rb") as imageFile:
                text = base64.b64encode(imageFile.read()).decode('utf-8')
            base_encoded_list.append(text)
        return  base_encoded_list


    def AllUniqueFaces(self):
        self.UseFaceCluster()
        base_encoded_list = self.GetUniqueFacesDirectory()
        # get the names of all folders in directory
        my_dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
        # get the names of folders which have label in their names
        req_dirs = [dir for dir in my_dirs if 'label' in dir]
        for dir in req_dirs:
            shutil.rmtree(dir)
        shutil.rmtree(f'{self.video_file.split(".")[0]}')
        os.remove(f'{self.video_file.split(".")[0]}.pickle')
        return base_encoded_list


@app.route('/video/upload', methods=['POST'])
def Main():
    if request.method == 'POST':
        file = request.files['file']
        print('Filename: ',file.filename)
        check = speech_to_text(file.filename)
        base_encoded_list = check.AllUniqueFaces()

        return {"imageBase64": base_encoded_list}




if __name__ == "__main__":
    app.run()


# a = speech_to_text('Pant.mp4')
# a.AllUniqueFaces()

