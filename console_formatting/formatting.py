#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:53:34 2020

@author: ikelockett
"""

import re
import time
from console_formatting.ansi_colours import light_cyan, light_green, light_red, light_white, yellow
import sys

def colour_map_1_to_10(x):
    """Map the numbers 1-10 to a colour."""
    colour_map = {
        0: light_red,
        1: light_red,
        2: light_red,
        3: yellow,
        4: yellow,
        5: light_white,
        6: light_white,
        7: light_white,
        8: light_green,
        9: light_green,
        10: light_green
        }
    return colour_map[x]


def dashed_line(print_out=True, n=50, colour=yellow):
    """Create a dashed line of a prespecified colour."""
    if print_out:
        print(f"{colour}{n * '-'}{light_white}")
    else:
        return colour + (n * "-") + light_white


def kv_print(k, v, suffix="", key_width=32, colour_map=False,
             symbol=False, return_text=False, signed=False,
             typing_effect=True, typing_delay=0.05):
    """Print a kv pair cleanly and colourfully."""
    if isinstance(k, tuple):
        k_val, k_colour = k
    else:
        k_val = k
        k_colour = light_cyan
    if isinstance(v, tuple):
        v_val, v_colour = v
    else:
        v_val = v
        v_colour = light_white

    if colour_map:
        v_colour = colour_map_1_to_10(v)
    if symbol and isinstance(v_val, int):
        v_val = v_val * symbol
    if signed:
        v_colour = light_green if v_val >= 0 else light_red
        print_str = f"{k_colour}{(k_val+':'):{key_width}}{v_colour}{v_val:+}{suffix}"
    else:
        print_str = f"{k_colour}{(k_val+':'):{key_width}}{v_colour}{v_val}{suffix}"
    if return_text:
        return print_str
    elif typing_effect:
        type_out(print_str)
    else:
        print(print_str)


def type_out(input_string, typing_delay=0.04):
    """Type out a string like a typewriter."""
    buffer = False
    buffer_str = ""
    for char in input_string:
        if char == "\033":
            buffer = True
        if buffer:
            buffer_str += char
            if char == "m":
                sys.stdout.write(buffer_str)
                sys.stdout.flush()
                buffer_str = ""
                buffer = False
                continue
            else:
                continue
        else:
            if re.match("[\S\-]", char):
                time.sleep(typing_delay)
            sys.stdout.write(char)
            sys.stdout.flush()
    sys.stdout.write("\n")

def line_break(n=1):
    """Print n blank lines."""
    print("" + (n-1) * "\n")

