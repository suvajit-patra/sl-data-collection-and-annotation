import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', required=True, help='enter name')
parser.add_argument('-d', '--dataset_dir', required=True, help='dataset directory')
args = parser.parse_args()

if len(args.name) > 0:
    try:
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'kinect'))
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'front'))
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'extras'))
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'perspective'))
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'sides'))
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'temp'))
        os.makedirs(os.path.join(args.dataset_dir, args.name, 'timestamps'))
    except:
        print('failed')