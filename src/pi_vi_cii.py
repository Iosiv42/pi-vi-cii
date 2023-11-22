""" pi-vi-cii's main script. """

import argparse
import os
import subprocess
import shutil


def get_aspect_ratio(video_path: str) -> float:
    """ Get aspect ratio of video. """
    p1 = subprocess.Popen(
        ('mediainfo', '--Inform=Video;%Width%x%Height%', f'{video_path}'),
        stdout=subprocess.PIPE
    )
    
    comm = p1.communicate()
    print(comm)
    w, h = map(int, comm[0].decode("utf-8").strip('\n').split("x"))
    return w/h


def media_path(path):
    if os.path.isfile(path):
        return path

    raise argparse.ArgumentTypeError(
        f"readable_dir:{path} is not a valid path"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='pi-vi-cii',
        description='Play video in terminal',
        epilog='Hope it help helps you'
    )

    parser.add_argument("video_path", type=media_path)

    args = parser.parse_args()
    print(args)

    video_ratio = get_aspect_ratio(args.video_path)

    cols, lines = shutil.get_terminal_size((-1, -1))
    cols //= 2
    if cols == -1 and lines == -1:
        raise RuntimeError("Unable to get terminal dimensions.")

    terminal_ratio = cols/lines

    if video_ratio > terminal_ratio:
        width = cols
        height = int(width / video_ratio)
    else:
        height = lines
        width = int(video_ratio * height)

    print(cols, lines)

    os.system(
        f'ffmpeg -hide_banner -loglevel error -i "{args.video_path}" '
        f'-vf "fps=25,scale={width}:{height}" -f rawvideo -pix_fmt gray - | '
        f'python src/core.py --width {width} --height {height}'
    )
