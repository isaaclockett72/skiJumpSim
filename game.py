#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:05:07 2020

@author: ikelockett
"""

import functions as sk
import numpy as np
import pickle
import pandas as pd
from pandas import DataFrame
from create_world import create_world

reset_all = True

if reset_all:
    create_world()

countries = pickle.load(open("countries.pkl", "rb"))
hills = pickle.load(open("hills.pkl", "rb"))
skijumpers = pickle.load(open("skijumpers.pkl", "rb"))

for skijumper in skijumpers.values():
    skijumper.set_form()
    skijumper.assign_personality()
    
# median_form = np.median([sj.form for sj in skijumpers.values()])
# filtered_skijumpers = [sj for sj in skijumpers.values() if sj.form >= median_form]

countries_df = sk.obj_list_to_df(countries)
countries_df["skijumpers"] = [
    [skijumper.name for skijumper in skijumpers.values()
     if skijumper.country_of_origin == country]
    for country in countries_df.index]
skijumpers_df = sk.obj_list_to_df(skijumpers)
hills_df = sk.obj_list_to_df(hills)
hills_df["skijumpers"] = [
    [skijumper.name for skijumper in skijumpers.values()
     if skijumper.home_hill == hill]
    for hill in hills_df.index]


# INIIATE SKIJUMPER ROSTER
roster = skijumpers_df.sort_values("overall_score") \
    .head(100) \
    .index \
    .to_list() \
    .__iter__() \


# PICK A COUNTRY
host_country = sk.select_country(countries)
host_hills = (h for h in hills.values() if h.country == host_country.name)

# GET HILL
current_hill = sk.go_to_next_hill(host_hills)
current_hill.set_horizontal_wind()
sk.start_hill(current_hill, skijumpers.values())
hill_results = {}

user_input = sk.tap_to_continue({"ss": "Skip future taps"})

# INITIATE A JUMP
sk.standard_round(current_hill, roster, skijumpers,
                  skip_continue_taps=(user_input=="ss"))
round_results_df = pd.read_pickle("results.pkl")