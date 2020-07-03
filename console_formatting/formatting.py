#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:53:34 2020

@author: ikelockett
"""

from console_formatting.ansi_colours import light_cyan, light_green, light_red, light_white, yellow


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
             symbol=False, return_text=False):
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
    print_str = f"{k_colour}{(k_val+':'):{key_width}}{v_colour}{v_val}{suffix}"
    if return_text:
        return print_str
    else:
        print(print_str)


def line_break(n=1):
    """Print n blank lines."""
    print("" + (n-1) * "\n")

