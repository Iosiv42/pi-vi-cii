#!/usr/bin/env python3

""" pi-vi-cii's main script. """

import argparse
import os
import subprocess
import shutil


def get_aspect_ratio(video_path: str) -> float:
    """ Get aspect ratio of video. """
    pipe = subprocess.Popen(
        ('mediainfo', '--Inform=Video;%Width%x%Height%', f'{video_path}'),
        stdout=subprocess.PIPE
    )

    comm = pipe.communicate()
    w, h = map(int, comm[0].decode("utf-8").strip('\n').split("x"))
    return w/h


def parse_args():
    """ Argparse video path. """

    parser = argparse.ArgumentParser(
        prog='pi-vi-cii',
        description='Play video in terminal',
        epilog='Hope it help helps you'
    )

    parser.add_argument("video_path")

    return parser.parse_args()


def start_shell_scripts(args, width, height) -> None:
    os.system(
        f'ffplay -hide_banner -loglevel error -i "{args.video_path}" '
        '-af pan="stereo|c0=c0|c1=c1" -nodisp &'
    )
    os.system(
        f'ffmpeg -hide_banner -loglevel error -i "{args.video_path}" '
        f'-vf "fps=25,scale={width}:{height}" -f rawvideo -pix_fmt gray - | '
        f'python src/core.py --width {width} --height {height}'
    )


if __name__ == "__main__":
    args = parse_args()

    cols, lines = shutil.get_terminal_size((-1, -1))
    cols //= 2
    if cols == -1 and lines == -1:
        raise RuntimeError("Unable to get terminal dimensions.")

    terminal_ratio = cols/lines
    video_ratio = get_aspect_ratio(args.video_path)

    if video_ratio > terminal_ratio:
        width = cols
        height = int(width / video_ratio)
    else:
        height = lines
        width = int(video_ratio * height)

    start_shell_scripts(args, width, height)
