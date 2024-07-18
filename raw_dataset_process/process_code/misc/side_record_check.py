import argparse
import cv2
from datetime import datetime
import numpy as np
import os

change_filename = True
reject_duration = 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--in_path", required=True, help = "input folder")
    args = parser.parse_args()

    dirs = os.listdir(args.in_path)
    for dir in dirs:
        files = os.listdir(os.path.join(args.in_path, dir))
        vidcap1 = cv2.VideoCapture(os.path.join(args.in_path, dir, files[0]))
        vidcap2 = cv2.VideoCapture(os.path.join(args.in_path, dir, files[1]))
        success1, image1 = vidcap1.read()
        success2, image2 = vidcap2.read()
        diff = np.sum(cv2.subtract(image1, image2))
        print(diff)
        if diff < 0.5:
            print('wrong: ', os.path.join(args.in_path, dir))

if __name__ == '__main__':
    main()