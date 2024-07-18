import argparse, os, subprocess, shutil
from datetime import datetime
import csv
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm
from multiprocessing import Pool

def process_fn(data):
    in_file = data[0]
    out_file = data[1]

    # print(word, in_file, out_file)

    # if not os.path.isfile(out_file) or os.path.getsize(out_file) < 1024.0:
    subprocess.call("ffmpeg -y -hide_banner -loglevel error -i \"" + in_file + "\" -b 5120k -an \"" + out_file + "\"", shell=True)


if __name__ == "__main__":
    print(datetime.now())

    data_roots = ['/data3/dataset', '/data4/dataset', '/data5/dataset']
    
    data_out_dirs = ['/data3/dataset_compressed', '/data4/dataset_compressed', '/data5/dataset_compressed']

    data = []

    for idx, data_root in enumerate(data_roots):
        for (root,dirs,files) in os.walk(data_root, topdown=True):
            for file in files:
                in_dir = root
                out_dir = root.replace(data_root, data_out_dirs[idx])
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                # print(in_dir, out_dir)
                if '.mkv' in file and 'sides' in in_dir :
                    data.append([os.path.join(in_dir, file), os.path.join(out_dir, file)])
                else:
                    if not os.path.isfile(os.path.join(out_dir, file)) or os.path.getsize(os.path.join(out_dir, file)) < 10.0:
                        shutil.copy(os.path.join(in_dir, file), os.path.join(out_dir, file))
    
    # process_map(process_fn, data, max_workers=32, chunksize=1)
    process_map(process_fn, data, chunksize=1)
    # with Pool(64) as pool:
    #     results = tqdm(pool.imap_unordered(process_fn, data), total=len(data), desc='Videos')
    print(datetime.now())
