#!/usr/bin/env python3

import argparse as ap
import itertools as it
import re
import sys

import colorful as cf
from colour import Color


def parse_args():
    p = ap.ArgumentParser()

    p.add_argument("-c", "--column", type=int, default=1, help="column to colorize, default: 1")

    p.add_argument(
        "-H", "--skip-header", default=False, action="store_true", help="skip colorizing header row",
    )

    p.add_argument("--mid", type=float, default=None, help="midpoint value, default: (min + max)/2")

    p.add_argument(
        "-f", "--field-separator", default=r"\s+", type=str, help="field separator regexp, default: '\\s+'",
    )

    return p.parse_args()


def parse_input(inp, separator_re):
    for line in inp:
        yield [str.strip(t) for t in re.split(separator_re, line)]


def select_column(data, i, default=None):
    for row in data:
        try:
            yield row[i]
        except IndexError:
            yield default


def to_float(s, default=0.0):
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


class ColorScaler:
    MIN_COLOR = "lime"
    MID_COLOR = "yellow"
    MAX_COLOR = "red"
    GRADIENT_STEPS = 256

    def __init__(self, min, mid, max):
        self.min = min
        self.max = max
        self.mid = self._normalize(min, mid, max)

        self.min_to_mid = list(self._gradient(self.MIN_COLOR, self.MID_COLOR, self.GRADIENT_STEPS))
        self.mid_to_max = list(self._gradient(self.MID_COLOR, self.MAX_COLOR, self.GRADIENT_STEPS))

    @staticmethod
    def _normalize(_min, x, _max):
        # bring x into range [min, max]
        x = max(x, _min)
        x = min(x, _max)
        return x

    @staticmethod
    def _gradient(start, end, steps):
        colors = Color(start).range_to(Color(end), steps)
        palette = {}
        for c in colors:
            h = c.hex_l.lstrip("#")
            name = "hex" + h
            palette[name] = "#" + h
            yield name
        cf.update_palette(palette)

    def scale(self, x):
        x = self._normalize(self.min, x, self.max)

        if x < self.mid:
            idx = (len(self.min_to_mid) - 1) * (x - self.min) / (self.mid - self.min)
            return self.min_to_mid[int(idx)]

        elif x == self.mid:
            return self.mid_to_max[0]

        else:
            assert x >= self.mid
            idx = (len(self.mid_to_max) - 1) * (x - self.mid) / (self.max - self.mid)
            return self.mid_to_max[int(idx)]


def cprint(color, *args, **kwargs):
    c = getattr(cf, color)
    return print(c(kwargs.get("sep", " ").join(args)), **kwargs)


# visually check if terminal colors work as expected if you are seeing bands of
# color instead of a smooth gradient the terminal might be not working in the
# "true color" mode
def test_color_scaler():
    cf.use_true_colors()
    cs = ColorScaler(0, 1, 2)
    for i, color in enumerate(it.chain(cs.min_to_mid, cs.mid_to_max)):
        text = color[len("hex") :]
        end = " " if (i + 1) % 8 else "\n"
        cprint(color, text, end=end)


def main():
    args = parse_args()
    cf.use_true_colors()

    inp = [line.rstrip("\n") for line in sys.stdin.readlines()]

    if args.skip_header:
        header, inp = inp[0], inp[1:]

    data = list(parse_input(inp, args.field_separator))
    col = list(select_column(data, args.column - 1))

    col_float = list(to_float(x) for x in col)
    col_min = min(col_float)
    col_max = max(col_float)

    mid = (col_min + col_max) / 2.0
    if args.mid is not None:
        mid = args.mid

    cs = ColorScaler(col_min, mid, col_max)

    if args.skip_header:
        print(header)

    for row, val in zip(inp, col_float):
        color = cs.scale(val)
        cprint(color, row)
