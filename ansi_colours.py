#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:53:34 2020

@author: ikelockett
"""

cyan = "\033[36;1m"
green = "\033[32;1m"
red = "\033[31;1m"
white = "\033[0m"
yellow = "\033[33;1m"


def dashed_line(print_out=False, n=32, colour=yellow):
    """Create a dashed line of a prespecified colour."""
    if print_out:
        print(f"{colour}{n * '-'}{white}")
    else:
        return colour + (n * "-") + white


def kv_print(k, v, suffix="", key_width=32):
    """Print a kv pair cleanly and colourfully."""
    if isinstance(k, tuple):
        if len(k) != 2:
            raise IndexError("Enter the key in the format: (k, colour)")
        k_colour = k[1]
        k = k[0]
    else:
        k_colour = cyan
    if isinstance(v, tuple):
        if len(v) != 2:
            raise IndexError("Enter the value in the format: (v, colour)")
        v_colour = v[1]
        v = v[0]
    else:
        v_colour = white
    print(f"{k_colour}{(k+':'):{key_width}}{v_colour}{v}{suffix}")


def line_break(n=1):
    """Print n blank lines."""
    print("" + (n-1) * "\n")
