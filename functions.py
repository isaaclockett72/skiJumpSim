#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:18:56 2020

@author: ikelockett
"""

import pandas as pd
from pandas import DataFrame
import random
from objects import Country, SkiJumper


def extract_hills(countries):
    """Extract the hills that were generated as part of the country gen."""
    hills_list = []
    for country in countries.values():
        hills_list.extend(country.hills)
    hills = {h.name: h for h in hills_list}
    return hills


def generate_countries(n=10):
    """Generate n countries."""
    countries_list = [Country() for x in range(n)]
    countries = {c.name: c for c in countries_list}
    return countries


def generate_skijumpers(countries, n=50):
    """Generate n ski jumpers, from the country list countries."""
    skijumpers_list = [SkiJumper(countries) for x in range(n)]
    skijumpers = {sk.name: sk for sk in skijumpers_list}
    return skijumpers


def go_to_next_hill(host_hills):
    """Move to the next hill in the tournament"""
    try:
        current_hill = host_hills.__next__()
    except StopIteration:
        print("Tournament complete!")    
        current_hill = ""
    return current_hill


def obj_list_to_df(obj_list, index_col="name"):
    """Convert a list of objects to a df."""
    obj_dict = {k: v.__dict__ for k, v in obj_list.items()}
    obj_df = DataFrame(obj_dict).T
    obj_df = obj_df.set_index(index_col)
    for col in obj_df.columns:
        try:
            obj_df[col] = pd.to_numeric(obj_df[col])
        except (TypeError, ValueError):
            pass
    return obj_df


def select_country(countries):
    """Select and announce the country selected for the tournament."""
    host_countries = {k: v for k, v in countries.items() if v.hill_count > 0}
    tournament_country = random.choice(list(host_countries.values()))
    tournament_country.introduce_country()
    return tournament_country


def start_hill(hill, skijumpers):
    attendance = hill.calculate_attendance(skijumpers)
    print(f"Attendance: {attendance:,} / {hill.max_crowd_size:,}")
    if attendance == hill.max_crowd_size:
        print("It's a sellout!")
    pass