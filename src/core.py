""" Core module to cast video frames to terminal. """

import curses
import sys
import argparse

import numpy as np

from utils import PeriodicActor, w_den_to_char


def parse_dims() -> tuple[int]:
    """ Argparse video dimensions. """
    parser = argparse.ArgumentParser(
        prog='pi-vi-cii core module',
        description='Casts video from stdin to terminal',
        epilog='auxilary script'
    )

    parser.add_argument("--width")
    parser.add_argument("--height")

    args = parser.parse_args()
    return int(args.width), int(args.height)


def draw(stdscr, width: int, height) -> bool:
    """ Draw frame from stdin. """

    stdscr.move(0, 0)

    frame_area = width * height
    pix_data = np.frombuffer(sys.stdin.buffer.read(frame_area), np.uint8)
    x = y = 0
    for pix in pix_data:
        if x == width:
            y = (y + 1) % height
            stdscr.move(y, 0)
            x = 0

        char, attr = w_den_to_char(pix / 255)
        stdscr.addstr(2*char, attr)
        x += 1

    stdscr.redrawwin()
    stdscr.refresh()

    return True


def play_video(stdscr, width: int, height: int) -> None:
    """ Play video from stdin (piped from ffmpeg) to terminal. """

    stdscr.erase()
    curses.curs_set(False)

    p_actor = PeriodicActor(0.04, draw, stdscr, width, height)
    p_actor.run()


if __name__ == "__main__":
    width, height = parse_dims()
    curses.wrapper(play_video, width, height)
