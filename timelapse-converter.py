import argparse
import os
from pathlib import Path

import cv2
from colorama import Fore, Style, init
from tqdm import tqdm


def start_up():
    parser = argparse.ArgumentParser(description="Create a timelapse video from a directory of images.")
    parser.add_argument("-f", metavar='fps', type=int, default=24, help="Frames per second for the output video (default: 24)")
    parser.add_argument("-d", metavar='input_directory', required=True, help="Input image directory")
    parser.add_argument("-o", metavar='output', required=True, help="Output video file path")
    args = parser.parse_args()

    fps = args.f
    out = f"{args.o}.mp4"    
    try:
        dir = Path(args.d)
        if not dir.is_dir():
            print(f"path to images must be a directory. ({dir})")
            raise AttributeError
    except:
        print("usage: timelapse-converter.py [-h] [-f fps] -d input_directory -o output")
        exit(1)
    
    if Path(out).exists():
        out = handle_exist(args.o)
    return (dir,out,fps)


def handle_exist(name):
    i = input(f"{name}.mp4 already exists. overwrite it? (y/n)")
    if i.lower() != "y":
        ext = 1
        while(Path(f"{name}{ext}.mp4").exists()):
            ext += 1
        name = name + str(ext)
    return f"{name}.mp4"


def get_shape(imgs: list[Path]):
    first_img = cv2.imread(os.path.join(imgs[0]))
    height, width, _ = first_img.shape
    return (height, width)


def build_video(video, imgs: list, fps):
    init()
    for img_file in tqdm(imgs, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Style.RESET_ALL)):
        img = cv2.imread(os.path.join(img_file))
        video.write(img)
    for i in range(fps):
        video.write(cv2.imread(os.path.join(imgs[-1])))
    return video


def main():
    dir, out, fps = start_up()    
    print(f"converting images in {dir} with {fps} FPS to {out}")
    imgs = list(x for x in dir.iterdir() if x.is_file() and (x.name.lower().endswith(".jpg") or  x.name.lower().endswith(".png")))
    height, width = get_shape(imgs)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(out, fourcc, fps, (width, height))
    video = build_video(video, imgs, fps)
    video.release()

if __name__=="__main__":
    main()
