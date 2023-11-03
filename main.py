import cv2
import time
import sys
import signal
import os
import nibabel as nib
import numpy as np


def main_function():
    video_device_id_frontal: int = 2
    video_device_id_lateral: int = 3

    cam_frontal = cv2.VideoCapture(video_device_id_frontal)
    cam_frontal.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam_frontal.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
    cam_frontal.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    cam_lateral = cv2.VideoCapture(video_device_id_lateral)
    cam_lateral.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam_lateral.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
    cam_lateral.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    images_frontal: list = []
    images_lateral: list = []

    def save_data_to_nifti(*args):
        path = os.getcwd() + "/Recordings/" + time.strftime("%Y%m%d-%H%M%S") + "/"
        print("")
        print("Saving Images to " + path)
        os.mkdir(path)
        nib.save(nib.Nifti1Image(np.array(images_frontal), np.eye(4)), path + "recording_frontal.nii.gz")
        nib.save(nib.Nifti1Image(np.array(images_lateral), np.eye(4)), path + "recording_lateral.nii.gz")
        sys.exit()

    print("Cams initialized, press Enter to start")
    while True:
        if input() == '':
            break
    print("Start Recording, stop with CTR+C or stop button")

    signal.signal(signal.SIGINT, save_data_to_nifti)
    while True:
        ret_frontal, frame_frontal_tmp = cam_frontal.read()
        frame_frontal = cv2.cvtColor(frame_frontal_tmp, cv2.COLOR_BGR2GRAY)
        ret_lateral, frame_lateral_tmp = cam_lateral.read()
        frame_lateral = cv2.cvtColor(frame_lateral_tmp, cv2.COLOR_BGR2GRAY)
        images_frontal.append(frame_frontal)
        images_lateral.append(frame_lateral)
        print("Frames Recorded: " + str(len(images_frontal)))
        time.sleep(0.2)


if __name__ == '__main__':
    path = os.getcwd() + "/Recordings/"
    if not os.path.exists(path):
        os.mkdir(path)
    main_function()
