import argparse
from datetime import datetime
import numpy as np
import os

change_filename = True
reject_duration = 2 #previously it was 3 for the first person

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
    verbose = args.verbose
    timeline_folder = os.path.join(args.in_path, 'timestamps')
    splits_folder = os.path.join(args.out_path, mode)
    
    timeline_files = sorted(os.listdir(timeline_folder))

    split_video_filename = sorted(os.listdir(splits_folder))
    
    for index in range(len(timeline_files)):
        timeline_file = os.path.join(timeline_folder, timeline_files[index])
        video_name = split_video_filename[index]
        events = []
        words = []
        words_count = {}

        if mode == 'sides':
            splits_dir = os.path.join(splits_folder, video_name, "right_splits")
            splits_dir_left = os.path.join(splits_folder, video_name, "left_splits")
        else:
            splits_dir = os.path.join(splits_folder, video_name, "splits")

        split_count = 0

        with open(timeline_file, 'r') as file:
            events = file.readlines()

        try:
            for i in range(len(events)):
                if 'start_record' in events[i] and 'stop_record' in events[i + 1]:
                    if (datetime.strptime(events[i+1][:26], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(events[i][:26], "%Y-%m-%d %H:%M:%S.%f")).total_seconds() > (reject_duration+0.1):
                        split_count += 1
                        word = events[i].split('start_record')[1][1:].split('[')[0][:-1]
                        words.append(word)
                        try:
                            words_count[word] += 1
                        except:
                            words_count[word] = 0
                        
        except Exception as e:
            print('Events file corrapted', e)
            return

        if verbose:
            print(words)

        # print(events)
        # print(words)
        # print(words_count)
        
        with open(os.path.join(splits_folder, video_name, timeline_files[index]), 'w') as logfile:
            skip = False
            videos_list = sorted(os.listdir(splits_dir))
            if mode == 'sides':
                videos_list_l = sorted(os.listdir(splits_dir_left))
            if len(videos_list) < 1 or not videos_list[0][-5].isdigit():
                if mode == 'sides' and len(videos_list) > 1 and 'right' in videos_list[0]:
                    pass
                else:
                    print(video_name, 'skipped')
                    skip = True

            if not(len(videos_list) == split_count):
                print(splits_dir, 'splits are wrong', len(videos_list), split_count)
                logfile.close()
                return

            if mode == 'sides' and not(len(videos_list_l) == split_count):
                print(splits_dir_left, 'splits are wrong', len(videos_list_l), split_count)
                logfile.close()
                return
            
            for i in range(len(words)):
                if words_count[words[i]] > 0:
                    if change_filename and not skip:
                        os.rename(os.path.join(splits_dir, videos_list[i]), os.path.join(splits_dir, words[i].replace('/', ' or ')+'_'+str(words_count[words[i]])+'.mkv'))
                        if mode == 'sides':
                            os.rename(os.path.join(splits_dir_left, videos_list_l[i]), os.path.join(splits_dir_left, words[i].replace('/', ' or ')+'_'+str(words_count[words[i]])+'.mkv'))
                    logfile.write(words[i]+'_'+str(words_count[words[i]])+'\n')
                    words_count[words[i]] -= 1
                else:
                    if change_filename and not skip:
                        os.rename(os.path.join(splits_dir, videos_list[i]), os.path.join(splits_dir, words[i].replace('/', ' or ')+'.mkv'))
                        if mode == 'sides':
                            os.rename(os.path.join(splits_dir_left, videos_list_l[i]), os.path.join(splits_dir_left, words[i].replace('/', ' or ')+'.mkv'))
                    logfile.write(words[i]+'\n')
        

if __name__ == '__main__':
    main()