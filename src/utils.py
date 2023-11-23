""" Utils for pi-vi-cii. """

import time
import curses
import bisect
from typing import Callable

from globals import W_DENS, W_DENS_KEYS


class PeriodicActor():
    """ Act some function with some periodicity. """

    def __init__(self, period: float, func: Callable, *func_args):
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
    """ Converts white density to char and
        returns char and curses attribute.
    """

    attr = curses.A_NORMAL
    if w_den > 0.66:
        w_den = 1 - w_den
        attr = curses.A_REVERSE

    idx = bisect.bisect_left(W_DENS_KEYS, w_den)
    char = W_DENS[W_DENS_KEYS[idx if idx == 0 else idx - 1]]

    return char, attr
