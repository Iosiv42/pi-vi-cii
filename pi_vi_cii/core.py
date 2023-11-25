""" Core module to cast video frames to terminal. """

import curses
import subprocess as sp
import time

import numpy as np

from .utils import PeriodicActor, w_den_to_char


def __draw(stdscr, pipe: sp.Popen, width: int, height: int) -> bool:
    """ Draw frame from stdin. """

    stdscr.move(0, 0)

    frame_area = width * height
    pix_data = np.frombuffer(pipe.stdout.read(frame_area), np.uint8)
    x = y = 0
    for pix in pix_data:
        if x == width:
            y = (y + 1) % height
            stdscr.move(y, 0)
            x = 0

        char, attr = w_den_to_char(pix)
        stdscr.addstr(2*char, attr)
        x += 1

    stdscr.redrawwin()
    stdscr.refresh()


def __curses_aux(stdscr, pipe: sp.Popen, width: int, height: int) -> None:
    """ Play video from pipe to terminal. """

    stdscr.clear()
    curses.curs_set(False)

    next_call = time.time()
    frame_area = width * height
    while True:
        stdscr.move(0, 0)

        pix_data = np.frombuffer(pipe.stdout.read(frame_area), np.uint8)
        x = y = 0
        for pix in pix_data:
            if x == width:
                y = (y + 1) % height
                stdscr.move(y, 0)
                x = 0

            char, attr = w_den_to_char(pix)
            stdscr.addstr(2*char, attr)
            x += 1

        stdscr.redrawwin()
        stdscr.refresh()

        next_call += 0.04
        delta = next_call - time.time()
        time.sleep(delta * (delta >= 0))


def play_from_pipe(pipe: sp.Popen, width: int, height: int) -> None:
    """ Play video from pipe to terminal. """
    try:
        curses.wrapper(__curses_aux, pipe, width, height)
    except KeyboardInterrupt:
        curses.endwin()
        pipe.kill()
