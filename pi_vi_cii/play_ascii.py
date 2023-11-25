#!/usr/bin/env python3

""" pi-vi-cii's main script. """

import sys
import os
import subprocess as sp
import shutil

import ffmpeg

from .core import play_from_pipe


def __get_aspect_ratio(video_path: str) -> float:
    """ Get aspect ratio of video. """

    probe = ffmpeg.probe(video_path)
    video_streams = [
        stream for stream in probe["streams"] if stream["codec_type"] == "video"
    ]

    return int.__truediv__(
        *map(int, video_streams[0]['display_aspect_ratio'].split(":"))
    )


def play_ascii(video_path: str) -> None:
    """ Play video to terminal using ascii symbols. """

    cols, lines = shutil.get_terminal_size((-1, -1))
    cols //= 2
    if cols == -1 and lines == -1:
        raise RuntimeError("Unable to get terminal dimensions.")

    terminal_ratio = cols/lines
    video_ratio = __get_aspect_ratio(video_path)

    if video_ratio > terminal_ratio:
        width = cols
        height = int(width / video_ratio)
    else:
        height = lines
        width = int(video_ratio * height)

    os.system(
        f'ffplay -hide_banner -loglevel error -i "{video_path}" '
        '-af pan="stereo|c0=c0|c1=c1" -nodisp &'
    )

    pipe: sp.Popen = (
        ffmpeg
        .input(video_path)
        .output(
            "pipe:",
            format="rawvideo",
            pix_fmt="gray",
            vf=f"fps=25,scale={width}:{height}",
            loglevel="quiet",
        )
        .run_async(pipe_stdout=True)
    )

    play_from_pipe(pipe, width, height)
    pipe.terminate()
