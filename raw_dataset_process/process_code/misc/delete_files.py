import os 
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, help = "input folder")
    parser.add_argument("-ex", "--extension", required=True, help = "extension of the files")
    parser.add_argument("-sub", "--substring", required=True, default='', help = "substring to check in absolute path")
    parser.add_argument("-v", "--verbose", required=False, help = "verbose")
    parser.add_argument("-t", "--test", required=True, help = "test")
    args = parser.parse_args()

    path = args.path
    extension = args.extension
    substring = args.substring
    verbose = args.verbose
    test = args.test

    print('Are you sure your want to delete all the ' + extension + ' files in the folder ' + path + ' having path substring ' + substring + ' (y/n)')
    confirmation = input()

    if not confirmation == 'y':
        return 

    for (root,dirs,files) in os.walk(path, topdown=True):
        for file in files:
            file_path = os.path.join(root, file)
            if file[-3:] == extension and substring in file_path:
                if verbose:
                    print('removing ', file_path)
                if test == 'no':
                    os.remove(file_path)

if __name__ == '__main__':
    main()
