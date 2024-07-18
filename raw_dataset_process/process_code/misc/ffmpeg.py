import os
import subprocess
from tqdm.contrib.concurrent import process_map

def process_fn(data):
    in_dir = data[0]
    out_dir = data[1]

    if not os.path.isfile(out_dir) or os.path.getsize(out_dir) < 1024.0:
        subprocess.call("ffmpeg -i \"" + in_dir + "\" -filter:v \"setpts=PTS/3\" -an \"" + out_dir + "\"")
        # subprocess.call("ffmpeg -i \"" + in_dir + "\" -filter:v \"fps=30\" -an \"" + out_dir + "\"")
        # subprocess.call("ffmpeg -i \"" + in_dir + "\" -vcodec copy -an \"" + out_dir + "\"")


if __name__ == "__main__":
    input_folder = "C:\\Users\\admin\\Desktop\\ARGISL_work\\apps\\wvtm\\assets\\videos_or"
    output_folder = "C:\\Users\\admin\\Desktop\\ARGISL_work\\apps\\wvtm\\assets\\videos"

    input_files = os.listdir(input_folder)
    data = []
    for file in input_files:
        out_dir = os.path.join(output_folder, file)
        out_dir = out_dir[:-4] + ".mp4"
        data.append([os.path.join(input_folder, file), out_dir])

    process_map(process_fn, data, max_workers=32)