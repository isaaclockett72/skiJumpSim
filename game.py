#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:05:07 2020

@author: ikelockett
"""

import functions as sk
import pickle
from create_world import create_world

reset_all = True

if reset_all:
    create_world()

countries = pickle.load(open("countries.pkl", "rb"))
hills = pickle.load(open("hills.pkl", "rb"))
skijumpers = pickle.load(open("skijumpers.pkl", "rb"))

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


# PICK A COUNTRY
host_country = sk.select_country(countries)
