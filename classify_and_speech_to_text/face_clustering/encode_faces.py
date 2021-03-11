# USAGE
	# python encode_faces.py --dataset dataset --encodings encodings.pickle

# import the necessary packages
from imutils import paths
# face_recognition library by @ageitgey
import face_recognition
# argument parser
import argparse
# pickle to save the encodings
import pickle
# openCV
import cv2
# operating system
import os
from constants import ENCODINGS_PATH