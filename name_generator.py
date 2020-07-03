#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:56:15 2020

@author: ikelockett
"""

import pandas as pd
from pandas import DataFrame, Series
import random
import string
from itertools import product


def init():
    """Initialise the name generation."""
    try:
        pairs_df = pd.read_pickle("pairs.pkl")
    except FileNotFoundError:
        pairs_of_letters = list(
            product(string.ascii_lowercase, string.ascii_lowercase))
        random.shuffle(pairs_of_letters)
        pairs_df = DataFrame(pairs_of_letters)

        pairs_df.to_pickle("pairs.pkl")
    return pairs_df


def initialise_columns(pairs_df):
    """Initialise the columns of the df."""
    if "accepted" not in pairs_df.columns:
        pairs_df["accepted"] = ""

    if "beginning" not in pairs_df.columns:
        pairs_df["beginning"] = ""
        pairs_df.loc[pairs_df["accepted"] == 0, "beginning"] = 0

    if "non_beginning" not in pairs_df.columns:
        pairs_df["non_beginning"] = ""
        pairs_df.loc[pairs_df["accepted"] == 0, "non_beginning"] = 0

    if "rating" not in pairs_df.columns:
        pairs_df["rating"] = ""
    pairs_df.loc[pairs_df["accepted"] == 0, "rating"] = 0

    if "pair" not in pairs_df.columns:
        pairs_df["pair"] = pairs_df[0] + pairs_df[1]

    return pairs_df


def count_remaining(df):
    """Count how many letter pairs still need to be evaluated."""
    print(pairs_df[pairs_df["accepted"] == ""].shape[0])
    print(pairs_df[pairs_df["beginning"] == ""].shape[0])
    print(pairs_df[pairs_df["non_beginning"] == ""].shape[0])
    print(pairs_df[pairs_df["rating"] == ""].shape[0])


def track_vc_counts(v, c, letter):
    """Keep track of how many vowels / consonants have been used in a row."""
    if letter in ["a", "e", "i", "o", "u", "y"]:
        v += 1
        c = 0
    else:
        v = 0
        c += 1
    return v, c


def create_string_unit(df, string_length=3, starting_string=""):
    """Create a unit of text adhering to some prespecified language rules."""
    final_string = starting_string

    valid = df[(df["accepted"] == 1) & (df["beginning"] == 1)]
    first_selection_idx = random.choice(valid.index)
    first_selection = df.iloc[first_selection_idx]
    v = 0
    c = 0
    final_string += (first_selection[0])
    v, c = track_vc_counts(v, c, first_selection[0])
    final_string += (first_selection[1])
    v, c = track_vc_counts(v, c, first_selection[1])
    while len(final_string) < string_length:
        valid = df[(df["accepted"] == 1) & (df["non_beginning"] == 1)]
        final_character = final_string[-1]
        valid_second_selections = valid[valid[0] == final_character]
        if valid_second_selections.shape[0] > 0:
            second_selection_idx = random.choices(
                valid_second_selections.index,
                2**valid_second_selections["rating"])[0]
            second_selection = Series(df.iloc[second_selection_idx])
            v, c = track_vc_counts(v, c, second_selection[1])
            if c > 3 and v > 2:
                return final_string
            elif c > 3:
                continue
            elif c > 2:
                if final_string[-2] != "s":
                    continue
            elif v > 2:
                continue
            else:
                final_string += (second_selection[1])
        elif final_string[-1] == "q":
            final_string += "u"
            return final_string
        else:
            return final_string
    return final_string


def generate_word(syllables=2, starting_string=""):
    """Generate a word with a specified number of syllables."""
    pairs_df = pd.read_pickle("pairs.pkl")
    word = ""
    for i in range(1, syllables+1):
        length = round(random.gauss(4, 1))
        word += create_string_unit(pairs_df, string_length=length,
                                   starting_string=starting_string)
        starting_string = ""
    return word


def pattern_selection_algorithm(df, column="accepted"):
    """Train algorithm with valid / invalid letter pairs."""
    returned_val = False
    while returned_val != "q":
        todo = df[df[column] == ""].index
        selection = random.choice(todo)
        returned_val = test_pair(df.iloc[selection], column)
        if returned_val == "q":
            continue
        else:
            df.iloc[selection][column] = returned_val
            df.to_pickle("pairs.pkl")
    return df


def test_pair(df_row, column="accepted"):
    """Test a pair of letters to see if they fit a certain rule."""
    print(df_row[0] + df_row[1])
    inp = ""
    accepted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "q"]\
        if column == "rating" else [0, 1, "q"]
    while inp not in accepted:
        if column == "rating":
            query_string = "How valid is this string? (1-10)\n"
        else:
            query_string = ("Does this work in an English syllable? %s (0/1)"
                            % column)
        inp = input(query_string)
        try:
            inp = int(inp)
        except ValueError:
            pass
    return inp


if __name__ == "__main__":
    pairs_df = init()
    pairs_df = initialise_columns(pairs_df)
    if pairs_df[pairs_df["accepted"] == ""].shape[0] > 0:
        pairs_df = pattern_selection_algorithm(pairs_df)
    if pairs_df[pairs_df["beginning"] == ""].shape[0] > 0:
        pairs_df = pattern_selection_algorithm(pairs_df, "beginning")
    if pairs_df[pairs_df["non_beginning"] == ""].shape[0] > 0:
        pairs_df = pattern_selection_algorithm(pairs_df, "non_beginning")
    if pairs_df[pairs_df["rating"] == ""].shape[0] > 0:
        pairs_df = pattern_selection_algorithm(pairs_df, "rating")
