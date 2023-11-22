""" Core module to cast video frames to terminal. """

import curses
import bisect
import time
import sys
import argparse
import threading
from typing import Callable

import numpy as np

from globals import W_DENS, W_DENS_KEYS


class PeriodicActor(threading.Thread):
    """ Act some function with some periodicity. """

    def __init__(self, period: float, func: Callable, *func_args):
        super().__init__()

        self.func = func
        self.func_args = func_args
        self.period = period
        self.running = True

    def run(self):
        """ Start actor. """

        next_call = time.time()
        while self.running:
            self.running = self.func(*self.func_args)

            next_call += self.period
            delta = next_call - time.time()
            time.sleep(delta * (delta >= 0))


def w_den_to_char(w_den: float) -> tuple[str, int]:
    """ Converts white density ot char and
        returns char and curses attribute.
    """

    attr = curses.A_NORMAL
    if w_den > 0.66:
        w_den = 1 - w_den
        attr = curses.A_REVERSE

    idx = bisect.bisect_left(W_DENS_KEYS, w_den)
    ch = W_DENS[W_DENS_KEYS[idx if idx == 0 else idx - 1]]

    return ch, attr


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


def draw(stdscr, frame_area: int, width: int) -> bool:
    """ Draw frame from stdin. """

    stdscr.move(0, 0)

    pix_data = np.frombuffer(sys.stdin.buffer.read(frame_area), np.uint8)
    x = 0
    for pix in pix_data:
        if x == width:
            stdscr.addch("\n")
            x = 0

        ch, attr = w_den_to_char(pix / 255)
        stdscr.addstr(2*ch, attr)
        x += 1

    stdscr.redrawwin()
    stdscr.refresh()

    return True


def play_video(stdscr, frame_area: int, width: int):
    """ Play video from stdin (piped from ffmpeg) to terminal. """

    stdscr.erase()
    curses.curs_set(False)

    p_actor = PeriodicActor(0.04, draw, stdscr, frame_area, width)
    p_actor.run()


if __name__ == "__main__":
    width, height = parse_dims()
    curses.wrapper(play_video, width*height, width)
