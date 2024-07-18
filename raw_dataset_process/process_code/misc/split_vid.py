import cv2
import numpy as np
import os
from tqdm.contrib.concurrent import process_map

def process_fn(data):
    vid_name = data[0]
    root_dir = data[1]
    out_path = data[2]

    upper_threshold = 200
    lower_threshold = 180

    video_file = os.path.join(root_dir, vid_name + '.mkv')

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(video_file, fps)
    counter = 1
    split_count = 0
    flag = False

    split_frame_list = []
    mid_pix = [980, 230]
    # mid_pix = [900, 300]

    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break

        if not flag:
            pixel = np.mean(frame[mid_pix[0]-4 : mid_pix[0]+5, mid_pix[1]-4 : mid_pix[1]+5], (0, 1))
            if pixel[1] >= upper_threshold and pixel[0] >= upper_threshold:
                flag = True
                # print(counter,'+')
                split_count += 1
                split_frame_list.append(str(counter)+'-')

        if flag:
            pixel = np.mean(frame[mid_pix[0]-4 : mid_pix[0]+5, mid_pix[1]-4 : mid_pix[1]+5], (0, 1))
            if pixel[1] < lower_threshold or pixel[0] < lower_threshold:
                flag = False
                # print(counter,'-')
                split_frame_list.append(str(counter)+',')

        counter += 1

    try:
        if split_frame_list[-1][-1] == ',':
            split_frame_list[-1] = split_frame_list[-1][:-1]
    except:
        pass

    print(vid_name+'Total Frames', counter)
    print(vid_name+'Total splits', split_count)
    print(vid_name, split_frame_list)

    try:
        os.makedirs(os.path.join(out_path, vid_name,'splits'))
    except:
        pass
    with open(os.path.join(out_path, vid_name, 'split_frame_list.txt'), 'w') as file:
        for i in split_frame_list:
            file.write(i)

if __name__ == "__main__":
    root_dir = "G:\\ARGISL\\data\\raw\\videos"
    out_path = "G:\\ARGISL\\data\\splits"
    vid_names = [name[:-4] for name in sorted(os.listdir(root_dir)) if name[-4:] == '.mkv']
    data = []
    for i in vid_names:
        data.append([i, root_dir, out_path])
    # data.append([vid_names[-1], root_dir, out_path])
    print(len(data))
    process_map(process_fn, data, max_workers=32)