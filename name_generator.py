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
    try:
        pairs_df = pd.read_pickle("pairs.pkl")
    except FileNotFoundError:
        pairs_of_letters = list(product(string.ascii_lowercase, string.ascii_lowercase))
        random.shuffle(pairs_of_letters)
        pairs_df = DataFrame(pairs_of_letters)
    
        pairs_df.to_pickle("pairs.pkl")
    return pairs_df


def now_the_triples():
    try:
        triples_df = pd.read_pickle("triples.pkl")
    except FileNotFoundError:
        triples_of_letters = list(product(string.ascii_lowercase,
                                          string.ascii_lowercase,
                                          string.ascii_lowercase))
        random.shuffle(triples_of_letters)
        triples_df = DataFrame(triples_of_letters)
        triples_df.to_pickle("triples.pkl")
    return triples_df


def initialise_columns(pairs_df, triples_df):
    if "accepted" not in pairs_df.columns:
        pairs_df["accepted"] = ""

    # if "accepted" not in triples_df.columns:
    #     triples_df["accepted"] = ""


    if "beginning" not in pairs_df.columns:
        pairs_df["beginning"] = ""
        pairs_df.loc[pairs_df["accepted"] == 0, "beginning"] = 0
        
    # if "beginning" not in triples_df.columns:
    #     triples_df["beginning"] = ""
    #     triples_df.loc[triples_df["accepted"] == 0, "beginning"] = 0
        
    if "non_beginning" not in pairs_df.columns:
        pairs_df["non_beginning"] = ""
        pairs_df.loc[pairs_df["accepted"] == 0, "non_beginning"] = 0
        
    # if "non_beginning" not in triples_df.columns:
    #     triples_df["non_beginning"] = ""
    #     triples_df.loc[triples_df["accepted"] == 0, "non_beginning"] = 0
        
    if "rating" not in pairs_df.columns:
        pairs_df["rating"] = ""
    pairs_df.loc[pairs_df["accepted"] == 0, "rating"] = 0
        
            
    if "pair" not in pairs_df.columns:
        pairs_df["pair"] = pairs_df[0] + pairs_df[1]
        
    if "pair_1" not in triples_df.columns:
        triples_df["pair_1"] = triples_df[0] + triples_df[1]
        
    if "pair_2" not in triples_df.columns:
        triples_df["pair_2"] = triples_df[1] + triples_df[2]
    
    
    return pairs_df, triples_df



def count_remaining(df):
    print(pairs_df[pairs_df["accepted"] == ""].shape[0])
    print(pairs_df[pairs_df["beginning"] == ""].shape[0])
    print(pairs_df[pairs_df["non_beginning"] == ""].shape[0])
    print(pairs_df[pairs_df["rating"] == ""].shape[0])


def track_vc_counts(v, c, letter):
    if letter in ["a","e","i","o","u","y"]:
        v += 1
        c = 0
    else:
        v = 0
        c += 1
    return v, c


def create_string_unit(df, string_length=3, starting_string="", ):
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
                valid_second_selections["rating"].replace("", 5))[0]
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


def generate_syllable(length=5, starting_string=""):
    return 


def generate_word(syllables=2, starting_string=""):
    pairs_df = pd.read_pickle("pairs.pkl")
    word = ""
    for i in range(1,syllables+1):
        length = round(random.gauss(4, 1))
        word += create_string_unit(pairs_df, string_length=length,
                                   starting_string=starting_string)
        starting_string = ""
    return word



def pattern_selection_algorithm(df, column="accepted"):
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
    print(df_row[0] + df_row[1])
    inp = ""
    accepted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "q"] if column == "rating" else [0, 1, "q"]
    while inp not in accepted:
        if column == "rating":
            query_string = "How valid is this string? (1-10)\n"
        else:
            query_string = "Does this pattern work within an English syllable? %s (0/1)" % column
        inp = input(query_string)
        try:
            inp = int(inp)
        except ValueError:
            pass
    return inp

    
if __name__ == "__main__":
    pairs_df = init()
    triples_df = now_the_triples()
    pairs_df, triples_df = initialise_columns(pairs_df, triples_df)
    # triples_df = triples_df.merge(pairs_df.drop([0,1], axis=1),
    #                               left_on="pair_1", right_on="pair",
    #                               suffixes=("","_1"))
    
    # triples_df = triples_df.merge(pairs_df.drop([0,1], axis=1),
    #                               left_on="pair_2", right_on="pair",
    #                               suffixes=("","_2"))
        
    # triples_df["accepted"] = triples_df["accepted_1"] * triples_df["accepted_2"]
    # triples_df["beginning"] = triples_df["beginning_1"] * triples_df["beginning_2"]
    # triples_df["non_beginning"] = triples_df["non_beginning_1"] * triples_df["non_beginning_2"]
    
    # valid_triples = triples_df[triples_df["accepted"]!=0]
        
    if pairs_df[pairs_df["accepted"] == ""].shape[0] > 0:        
        pairs_df = pattern_selection_algorithm(pairs_df)
        
    if pairs_df[pairs_df["beginning"] == ""].shape[0] > 0:        
        pairs_df = pattern_selection_algorithm(pairs_df, "beginning")
        
    if pairs_df[pairs_df["non_beginning"] == ""].shape[0] > 0:        
        pairs_df = pattern_selection_algorithm(pairs_df, "non_beginning")
        
    if pairs_df[pairs_df["rating"] == ""].shape[0] > 0:
        pairs_df = pattern_selection_algorithm(pairs_df, "rating")
        