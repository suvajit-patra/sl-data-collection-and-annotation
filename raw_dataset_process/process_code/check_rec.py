import argparse
from datetime import datetime
import os

change_filename = True
reject_duration = 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--in_path", required=True, help = "input folder")
    parser.add_argument("-v", "--verbose", required=False, help = "verbose")
    args = parser.parse_args()

    verbose = args.verbose
    timeline_folder = os.path.join(args.in_path, 'timestamps')
    
    timeline_files = sorted(os.listdir(timeline_folder))
    
    events = []
    words = []
    
    for index in range(len(timeline_files)):
        timeline_file = os.path.join(timeline_folder, timeline_files[index])
        words_count = {}

        with open(timeline_file, 'r') as file:
            events = file.readlines()

        try:
            for i in range(len(events)):
                if 'start_record' in events[i] and 'stop_record' in events[i + 1]:
                    if (datetime.strptime(events[i+1][:26], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(events[i][:26], "%Y-%m-%d %H:%M:%S.%f")).total_seconds() > (reject_duration+0.1):
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
        
    print('total words count: ', len(words))
    print('unique words count: ', len(set(words)))

    
if __name__ == '__main__':
    main()