import cv2 as cv
import os
from glob import glob

def MakeImageDirectory(video_file):
    vidObj = cv.VideoCapture(video_file)
    video_file_name = video_file.split('.')[0]
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
        except Exception as e:
            print(f'Exeception: {e}')
            pass

    try:
        os.mkdir('sample/faces')
    except Exception as e:
        pass
    pass

def ExtractFaces(image,neighbors=3):
    img = cv.imread(filename=image)
    image_filename = image.split('\\')[-1]
    video_filename = image.split('\\')[0]
    # convert to grayscale image
    gray_image = cv.cvtColor(src=img,code=cv.COLOR_BGR2GRAY)
    # call the har cascade xml file
    har_cas = cv.CascadeClassifier('har_face.xml')
    # detect faces
    face_detect = har_cas.detectMultiScale(image=gray_image,scaleFactor=1.1,minNeighbors=neighbors)
    for (x, y, w, h) in face_detect:
        cv.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), thickness=2, color=(0, 255, 0))
        roi_color = img[y:y + h, x:x + w]
        print(str(video_filename)+"\\faces\\"+str(image_filename) + str(x) + str(w) + str(h) + '_faces.jpg')
        cv.imwrite(str(video_filename)+"\\faces\\"+str(image_filename) + str(x) + str(w) + str(h) + '_faces.jpg', roi_color)


def detect_face_try(image_location,neighbors=3):
    img = cv.imread(filename=image_location)
    # convert to grayscale image
    gray_image = cv.cvtColor(src=img,code=cv.COLOR_BGR2GRAY)
    # call the har cascade xml file
    har_cas = cv.CascadeClassifier('har_face.xml')
    # detect faces
    face_detect = har_cas.detectMultiScale(image=gray_image,scaleFactor=1.1,minNeighbors=neighbors)
    print(f'Number of faces detected in image is: {len(face_detect)}')
    if len(face_detect) == 1:
        for (x,y,w,h) in face_detect:
            cv.rectangle(img=img,pt1=(x,y),pt2=(x+w,y+h),thickness=2,color=(0,255,0))
            roi_color = img[y:y + h, x:x + w]
            print("[INFO] Object found. Saving locally.")
            # print(str(x)+ str(w) + str(h) + '_faces.jpg')
            cv.imshow(winname='Face detection', mat=img)
            cv.waitKey(0)
            cv.imwrite(str(x)+ str(w) + str(h) + '_faces.jpg', roi_color)
            cv.imshow(winname='Only face', mat=roi_color)
            cv.waitKey(0)
    else:
        for (x, y, w, h) in face_detect:
            cv.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), thickness=2, color=(0, 255, 0))
            roi_color = img[y:y + h, x:x + w]
            print("[INFO] Object found. Saving locally.")
            # print(str(x)+ str(w) + str(h) + '_faces.jpg')
        cv.imshow(winname='Face detection', mat=img)
        cv.waitKey(0)
    # cv.imshow(winname='Face detection',mat=img)
    # cv.imshow(winname='Only face', mat=img)
    # cv.waitKey(0)
# single_image = 'C:/Users/Arjun Janamatti/Documents/image_classification/nude_sexy_safe_v1_x320/testing/safe/0B16C26F-2C07-4F75-B8BC-F7A50E3D5EFE.jpg'
# group_img = 'C:/Users/Arjun Janamatti/Documents/image_classification/nude_sexy_safe_v1_x320/training/sexy/GantMan_0A21E234-F4FF-49A7-B6AC-98C69F5C6EF2.jpg'
# detect_face_try(single_image)
# detect_face_try(group_img)

# MakeImageDirectory('sample.mp4')



images_list = glob('sample/*.jpg')
print(images_list)
for image in images_list:
    ExtractFaces(image)

