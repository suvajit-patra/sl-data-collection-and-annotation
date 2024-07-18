import csv
import os

words = []
with open('../300_atomic_words.csv', 'r') as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        words.append(line[0].strip())

entries = []
with open('/data1/data/metadata.csv', 'r') as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        entries.append(line)

with open('/data1/data/metadata_300.csv', 'w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    header = ['subject_id', 'video_dir', 'video_name', 'word', 'split']
    csvwriter.writerow(header)
    for entry in entries:
        if entry[3] in words and entry[0] != 's0001':
            csvwriter.writerow(entry)
            
            