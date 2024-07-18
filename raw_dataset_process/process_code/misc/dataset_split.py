import csv
import os
import shutil
from tqdm import tqdm

root = '/data1'
dest_dir = 'data_300'

entries = []
with open('/data1/data/metadata_300.csv', 'r') as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        entries.append(line)
    
    entries = entries[1:]

    for entry in tqdm(entries):
        # print(os.path.join(root, entry[1].replace('data', 'data_300'), entry[2]))
        try:
            os.makedirs(os.path.join(root, entry[1].replace('data', 'data_300')))
        except:
            pass
        shutil.copyfile(os.path.join(root, entry[1], entry[2]), os.path.join(root, entry[1].replace('data', 'data_300'), entry[2]))
        # break
            
            