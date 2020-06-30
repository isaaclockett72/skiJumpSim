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


def dashed_line(n=32, colour=yellow):
    """Create a dashed line of a prespecified colour."""
    return colour + (n * "-") + white
