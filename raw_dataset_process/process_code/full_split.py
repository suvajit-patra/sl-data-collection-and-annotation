import os
import cv2
import numpy as np
from pathlib import Path
import subprocess
from tqdm.contrib.concurrent import process_map
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--in_path", required=True, help = "input folder")
    parser.add_argument("-out", "--out_path", required=True, help = "output folder")
    parser.add_argument("-v", "--verbose", required=False, help = "verbose")
    parser.add_argument("-m", "--mode", required=True, help = "which mode front or sides or kinect")
    args = parser.parse_args()

    if args.in_path.strip() == args.out_path.strip():
        print('change output dir')
        return

    mode = args.mode
    in_path = args.in_path
    out_path = args.out_path
    verbose = args.verbose

    try:
        os.makedirs(os.path.join(out_path, 'temp'))
    except:
        pass

    if splitPath(in_path) and splitPath(out_path):
        subject_name = splitPath(in_path)[-1]
        # subject_name_p = splitPath(out_path)[-1]
    else:
        print("error")
        return 1

    input_files = sorted(os.listdir(os.path.join(args.in_path, mode)))
    if mode in ['front', 'kinect']:
        input_files = [file[:-4] for file in input_files]
    elif mode == 'sides':
        input_files1 = sorted(os.listdir(os.path.join(in_path, 'temp', 'Corel MultiCam Capture X', 'Records')))
        input_files2 = sorted(os.listdir(os.path.join(in_path, 'sides')))
        if len(input_files1) > len(input_files2):
            input_files = input_files1
        else:
            input_files = input_files2

    data = []
    for file in input_files:
        data.append([file, in_path, out_path, mode])

    process_map(processFn, data, max_workers=32)

def splitPath(path):
    if len(path.split('\\')) > 1:
        return path.split('\\')
    elif len(path.split('/')) > 1:
        return path.split('/')
    else:
        return None

def processFn(data):
    video_name = data[0]
    in_path = data[1]
    out_path = data[2]
    mode = data[3]

    split_path = os.path.join(out_path, mode)

    if not mode == 'kinect':
        if mode == 'front':
            in_video_file = os.path.join(in_path, mode, video_name) + '.mp4'
            t_mkv_file = os.path.join(out_path, 'temp', mode, video_name) + ".mkv"
        elif mode == 'sides':
            try:
                sides_folder = os.path.join(in_path, 'temp', 'Corel MultiCam Capture X', 'Records', video_name)
                files = os.listdir(sides_folder)
                # print(files)
                if 'Camera 1' in files[0]:
                    r_file = files[0]
                    l_file = files[1]
                else:
                    r_file = files[1]
                    l_file = files[0]
                in_video_file = os.path.join(sides_folder, r_file)
                in_video_file_l = os.path.join(sides_folder, l_file)
            except:
                in_video_file = os.path.join(in_path, mode, video_name, 'right.mov')
                in_video_file_l = os.path.join(in_path, mode, video_name, 'left.mov')
            t_mkv_file = os.path.join(out_path, 'temp', mode, video_name, 'right.mkv')
            t_mkv_file_l = os.path.join(out_path, 'temp', mode, video_name, 'left.mkv')

        try:
            os.makedirs(t_mkv_file.rstrip(splitPath(t_mkv_file)[-1]))
        except Exception as e:
            pass

        makeMkv(in_video_file, t_mkv_file)
        if mode == 'sides':
            makeMkv(in_video_file_l, t_mkv_file_l)

        split_count = splitReader(t_mkv_file, video_name, mode, split_path)
        
        if mode == 'sides':
            splitVideo(t_mkv_file, video_name, mode, split_path, split_count, t_mkv_file_l)
        else:
            splitVideo(t_mkv_file, video_name, mode, split_path, split_count)
    else:
        split_count = splitReader(os.path.join(in_path, mode, video_name) + '.mkv', video_name, mode, split_path)
        
        splitVideo(os.path.join(in_path, mode, video_name) + '.mkv', video_name, mode, split_path, split_count)
    
def makeMkv(in_path, out_path):
    if not os.path.isfile(out_path) or os.path.getsize(out_path) < 1024.0:
        subprocess.call("ffmpeg -i \"" + in_path + "\" -vcodec copy -an \"" + out_path + "\"", shell=True)


def splitReader(mkv_file, vid_name, mode, out_path):
    cap = cv2.VideoCapture(mkv_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(mkv_file, fps)
    counter = 1
    split_count = 0
    flag = False

    split_frame_list = []

    if (os.path.exists(os.path.join(out_path, vid_name, 'split_frame_list.txt')) and 
        os.path.getsize(os.path.join(out_path, vid_name, 'split_frame_list.txt')) > 8.0):
        with open(os.path.join(out_path, vid_name, 'split_frame_list.txt'), 'r') as file:
            temp = file.readline()
        split_count = temp.count('-')
        return split_count

    if mode == 'kinect':
        mid_pix = [900, 380]
        upper_threshold = 140
        lower_threshold = 120
    elif mode == 'front':
        mid_pix = [900, 260]
        upper_threshold = 180
        lower_threshold = 150
    elif mode == 'sides':
        mid_pix = [920, 380]
        upper_threshold = 120
        lower_threshold = 100

    split_start = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            counter += 1
            # looking forward some frames in case of frame drops
            for i in range(5):
                is_read, frame = cap.read()
                if is_read:
                    break
                counter += 1
        if not is_read:
            # break out of the loop if there are no frames to read
            break

        if not flag:
            pixel = np.mean(frame[mid_pix[0]-9 : mid_pix[0]+10, mid_pix[1]-9 : mid_pix[1]+10], (0, 1))
            # print(pixel)
            if pixel[2] >= upper_threshold and pixel[0] >= upper_threshold:
                flag = True
                # print(counter,'+')
                split_start = counter

        if flag:
            pixel = np.mean(frame[mid_pix[0]-9 : mid_pix[0]+10, mid_pix[1]-9 : mid_pix[1]+10], (0, 1))
            if pixel[2] < lower_threshold or pixel[0] < lower_threshold:
                flag = False
                # print(counter,'-')
                if counter - split_start >= 1:
                    split_count += 1
                    print(mkv_file, ' # splits -> ', split_count)
                    split_frame_list.append(str(split_start)+'-')
                    split_frame_list.append(str(counter)+',')

        counter += 1
        if counter % 1000 == 0:
            print(mkv_file, ' frames processed -> ', counter)

    try:
        if split_frame_list[-1][-1] == ',':
            split_frame_list[-1] = split_frame_list[-1][:-1]
    except:
        pass

    print(vid_name+' Total Frames', counter)
    print(vid_name+' Total splits', split_count)
    print(vid_name, split_frame_list)

    try:
        if mode == "sides":
            os.makedirs(os.path.join(out_path, vid_name,'right_splits'))
            os.makedirs(os.path.join(out_path, vid_name,'left_splits'))
        else:
            os.makedirs(os.path.join(out_path, vid_name,'splits'))
    except:
        pass
    with open(os.path.join(out_path, vid_name, 'split_frame_list.txt'), 'w') as file:
        for i in split_frame_list:
            file.write(i)
    
    return split_count
    

def splitVideo(mkv_file, vid_name, mode, out_path, split_count, mkv_file_l=None):
    splits = None
    with open(os.path.join(out_path, vid_name, 'split_frame_list.txt'), 'r') as file:
        splits = file.readline()

    if mode == 'sides':
        if (len(os.listdir(os.path.join(out_path, vid_name,'right_splits'))) == split_count or
                len(os.listdir(os.path.join(out_path, vid_name,'left_splits'))) == split_count):
            return
        out_file = os.path.join(out_path, vid_name,'right_splits', 'right.mkv')
        out_file_l = os.path.join(out_path, vid_name,'left_splits', 'left.mkv')
        subprocess.call('mkvmerge -o \"'+out_file+'\" --split parts-frames:'+splits+' \"'+mkv_file+'\"', shell=True)
        subprocess.call('mkvmerge -o \"'+out_file_l+'\" --split parts-frames:'+splits+' \"'+mkv_file_l+'\"', shell=True)
    else:
        if len(os.listdir(os.path.join(out_path, vid_name,'splits'))) == split_count:
            return
        out_file = os.path.join(out_path, vid_name,'splits', vid_name + '.mkv')
        subprocess.call('mkvmerge -o \"'+out_file+'\" --split parts-frames:'+splits+' \"'+mkv_file+'\"', shell=True)

    

if __name__ == "__main__":
    main()