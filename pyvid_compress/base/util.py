from math import log10, sqrt
import numpy as np
import cv2
import os


def file_to_tensor(file):
    vidcap = cv2.VideoCapture(file)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()
    count = 0
    frames = []
    while success:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frames.append(image)
        count += 1
        success, image = vidcap.read()

    frames = np.stack(frames, axis=0).astype(float)
    return frames, fps


def claculate_compression_ratio(original_file, compressed_file):
    original_file_size = float(os.stat(original_file).st_size)
    compressed_file_size = float(os.stat(compressed_file).st_size)
    return original_file_size/compressed_file_size


def calculate_psnr(original_file, compressed_file):
    original, ofps = file_to_tensor(original_file)
    compressed, cfps = file_to_tensor(compressed_file)
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0 * 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr
