#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:53:34 2020

@author: ikelockett
"""

from ansi_colours import light_cyan, light_green, light_red, white, yellow

def dashed_line(print_out=True, n=50, colour=yellow):
    """Create a dashed line of a prespecified colour."""
    if print_out:
        print(f"{colour}{n * '-'}{white}")
    else:
        return colour + (n * "-") + white


def kv_print(k, v, suffix="", key_width=32, colour_map=False,
             symbol=False):
    """Print a kv pair cleanly and colourfully."""
    if isinstance(k, tuple):
        if len(k) != 2:
            raise IndexError("Enter the key in the format: (k, colour)")
        k_colour = k[1]
        k = k[0]
    else:
        k_colour = light_cyan
    if isinstance(v, tuple):
        if len(v) != 2:
            raise IndexError("Enter the value in the format: (v, colour)")
        v_colour = v[1]
        v = v[0]
    elif colour_map:
        v_colour = colour_map_1_to_10(v)
    else:
        v_colour = white
    if symbol and isinstance(v, int):
        v = v * symbol
    print(f"{k_colour}{(k+':'):{key_width}}{v_colour}{v}{suffix}")


def line_break(n=1):
    """Print n blank lines."""
    print("" + (n-1) * "\n")

def colour_map_1_to_10(x):
    """Map the numbers 1-10 to a colour."""
    colour_map = {
        0: light_red,
        1: light_red,
        2: light_red,
        3: yellow,
        4: yellow,
        5: white,
        6: white,
        7: white,
        8: light_green,
        9: light_green,
        10: light_green
        }
    return colour_map[x]