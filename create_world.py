#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:05:07 2020

@author: ikelockett
"""

import functions as sk
import pickle

reset_countries = True
reset_skijumpers = True

if reset_countries:
    countries = sk.generate_countries(n=25)
    hills = sk.extract_hills(countries)
    pickle.dump(countries, open("countries.pkl", "wb"))
    pickle.dump(hills, open("hills.pkl", "wb"))
else:
    countries = pickle.load(open("countries.pkl", "rb"))
    hills = pickle.load(open("hills.pkl", "rb"))
if reset_skijumpers:
    skijumpers = sk.generate_skijumpers(countries, n=100)
    pickle.dump(skijumpers, open("skijumpers.pkl", "wb"))
else:
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
