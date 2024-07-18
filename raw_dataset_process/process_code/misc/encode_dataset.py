import os, csv, shutil
from pathlib import Path
from tqdm import tqdm


words_file = '../datasheet_v11.csv'
id_file = '../dataset_subject_ids.csv'
data_root = '/data2/data'
out_folder = '/data2/data_encoded'
file_ext = '.mp4'

if __name__ == "__main__":
    prefix_abbr = {'front':'_f_', 'left':'_l_', 'right':'_r_'}

    word_id = {}
    with open(words_file, 'r') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)

        for line in csvFile:
            word_id[line[1]] = line[2]

    subject_id = {}
    with open(id_file, 'r') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)

        for line in csvFile:
            subject_id[line[0]] = line[1]

    
    for (root,dirs,files) in os.walk(data_root, topdown=True):
        subject = Path(root).parts[-2]
        loop = tqdm(files, desc=f'Processing videos -> {subject} {Path(root).parts[-1]}') if subject in subject_id else files
        for file in loop:
            if file_ext in file:
                word = file[:-4]
                word_clean = word.replace(' or ', '/')
                out_file = subject_id[subject] + prefix_abbr[Path(root).parts[-1]] + word_id[word_clean] + file_ext
                out_dir = root.replace(data_root, out_folder).replace(subject, subject_id[subject])
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                # print(os.path.join(root, file), os.path.join(out_dir, out_file))
                shutil.copy(os.path.join(root, file), os.path.join(out_dir, out_file))
                # exit()
