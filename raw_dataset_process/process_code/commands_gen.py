import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', required=True, help='enter name')
parser.add_argument('-id', '--id', required=True, help='enter id')
parser.add_argument('-in', '--in_path', required=True, help='enter in_path')
parser.add_argument('-out', '--out_path', required=True, help='enter out_path')
args = parser.parse_args()

if len(args.name) > 0:
    try:
        with open(os.path.join('commands_archive', 'commands_'+args.name+'.txt'), 'w') as file:
            file.write('python full_split.py -in ' + args.in_path + args.name + ' -out ' + args.out_path + args.id + ' -m front\n')
            file.write('python name_split.py -in ' + args.in_path + args.name + ' -out ' + args.out_path + args.id + ' -m front\n')
            file.write('python full_split.py -in ' + args.in_path + args.name + ' -out ' + args.out_path + args.id + ' -m sides\n')
            file.write('python name_split.py -in ' + args.in_path + args.name + ' -out ' + args.out_path + args.id + ' -m sides\n')
            # file.write('python crop_splits.py -sp D:\ISL_project\dataset\\' + args.name + '_p\\front -out D:\ISL_project\dataset\\' + args.name + '_p\cropped')
    except Exception as e:
        print('failed', e)