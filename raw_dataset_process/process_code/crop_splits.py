import argparse
import os
import subprocess
from tqdm.contrib.concurrent import process_map
from datetime import datetime
import csv

crop_string = ''

def process_fn(data):
    word = data[0]
    in_dir = data[1]
    out_dir = data[2]

    # print(word, in_dir, out_dir)

    if not os.path.isfile(out_dir) or os.path.getsize(out_dir) < 1024.0:
        # subprocess.call("ffmpeg -i \"" + in_dir + "\" -filter:v \"crop=702:864:620:56\" -an \"" + out_dir + "\"")
        # subprocess.call("ffmpeg -i \"" + in_dir + "\" -filter:v \"crop=1280:1080:331:0\" -an \"" + out_dir + "\"", shell=True)
        subprocess.call("ffmpeg -i \"" + in_dir + "\" -filter:v \"crop="+crop_string+"\" -an \"" + out_dir + "\"", shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sr", "--splits_root", required=True, help = "input root")
    parser.add_argument("-sp", "--splits_path", required=True, help = "input folder of videos")
    parser.add_argument("-out", "--out_path", required=True, help = "output folder")
    parser.add_argument("-wf", "--word_file", required=True, help = "word file")
    parser.add_argument("-fp", "--file_prefix", required=True, help = "file prefix")
    parser.add_argument("-cs", "--crop_str", required=True, help = "crop string")
    parser.add_argument("-v", "--verbose", required=False, help = "verbose")
    parser.add_argument("-t", "--test", required=False, help = "test")
    args = parser.parse_args()
    
    splits_root = args.splits_root
    splits_folder = args.splits_path
    output_folder = args.out_path
    verbose = args.verbose
    test = args.test
    words_file = args.word_file
    crop_string = args.crop_str
    file_prefix = args.file_prefix

    try:
        os.makedirs(output_folder)
    except:
        pass

    words = {}
    with open(words_file, 'r') as file:
        header = next(file)
        csvFile = csv.reader(file)

        for line in csvFile:
            words[line[0]] = line[1]
    
    # print(len(words))

    all_folders = os.listdir(splits_root)
    video_dir = {}
    for folder in all_folders:
        temp_words = []
        temp_files = os.listdir(os.path.join(splits_root, folder))
        # print(temp_files)
        for file in temp_files:
            if file[-4:] == '.txt' and not file == 'split_frame_list.txt':
                # print("*")
                with open(os.path.join(splits_root, folder, file), 'r') as file:
                    temp_words = file.readlines()
                temp_words = [i.rstrip('\n') for i in temp_words]
        
        for word in temp_words:
            video_dir[word] = os.path.join(splits_root, folder, splits_folder, word.replace('/', ' or ')+".mkv")
    
    data = []
    for word in words.keys():
        try:
            # data.append([word, video_dir[word], os.path.join(output_folder, word.replace('/', ' or ')+".mp4")])
            data.append([word, video_dir[word], os.path.join(output_folder, file_prefix + words[word]+".mp4")])
        except Exception as e:
            print(e)

    
    # print(video_dir.keys())
    # print(data)

    process_map(process_fn, data, max_workers=40, chunksize=1)
    print(datetime.now())

