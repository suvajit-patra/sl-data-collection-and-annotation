#                         w   h   x  y
# for perspective 1 use 1200:950:350:0
# for perspective 3 use 1200:950:425:0
import os
import csv
import subprocess

mode = 'front'
front_cs = {'1' : '1200:950:350:0', '2' : '1200:950:350:0', '3' : '1200:950:425:0'}

data_folders = ["/data1/", "/data2/", "/data3/", "/data4/", "/data5/"]

out_folder = "/data1/data/"
try:
    os.makedirs(out_folder)
except:
    pass

subject_per = {}

with open('../input/subject_ids_mapping.csv', mode ='r')as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        subject_per[line[1]] = line[4]

for data_folder in data_folders:
    subjects = os.listdir(os.path.join(data_folder, 'dataset'))
    for subject in subjects:
        if mode == 'front':
            try:
                os.makedirs(os.path.join(out_folder, subject, 'front'))
            except:
                pass
            file_prefix = subject+'_f_'
            subprocess.call("python crop_splits.py -sp " + os.path.join(data_folder, 'dataset', subject, 'front') + " -out " + os.path.join(out_folder, subject, 'front') + " -wf ../input/word_tags.csv -fp " + file_prefix + " -cs " + front_cs[subject_per[subject]], shell=True)


    