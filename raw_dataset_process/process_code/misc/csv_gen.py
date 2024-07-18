import csv
import os


# split[7:1:2]
# train = ['s0002', 's0003', 's0005', 's0007', 's0008', 's0009', 's0010', 's0011', 's0012', 's0013', 's0015', 's0017', 's0019', 's0021']
# val = ['s0006', 's0014']
# test = ['s0004', 's0016', 's0018', 's0020']


# split[5:1:4]
train = ['s0014', 's0003', 's0002', 's0013', 's0009', 's0008', 's0012', 's0006', 's0019', 's0010']
val = ['s0016', 's0004']
test = ['s0018', 's0017', 's0020', 's0005', 's0015','s0011', 's0007', 's0021']

dir = '/data1/data/'


words = {}
with open('../word_tags.csv', 'r') as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        words[line[1]] = line[0]


with open('/data1/data/metadata.csv', 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)
    header = ['subject_id', 'video_dir', 'video_name', 'word', 'split']
    csvwriter.writerow(header)
    for (root,dirs,files) in os.walk(dir, topdown=True):
        for file in files:
            if file[-3:] == 'mp4':
                sub_name = file.split('_')[0]
                split = None
                if sub_name in train:
                    split = 'train'
                if sub_name in test:
                    split = 'test'
                if sub_name in val:
                    split = 'val'
                row = [file.split('_')[0], os.path.join('data', file.split('_')[0], 'front'), file, words[file.split('_')[2][:-4]], split]
                # writing the data rows
                csvwriter.writerow(row)