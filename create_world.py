#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:05:07 2020

@author: ikelockett
"""

import functions as sk
import pickle

reset = True

if reset:
    countries = sk.generate_countries(n=100)
    skijumpers = sk.generate_skijumpers(countries, n=50)
    hills = sk.extract_hills(countries)
    pickle.dump(countries, open("countries.pkl", "wb"))
    pickle.dump(skijumpers, open("skijumpers.pkl", "wb"))
    pickle.dump(hills, open("hills.pkl", "wb"))
else:
    countries = pickle.load(open("countries.pkl", "rb"))
    skijumpers = pickle.load(open("skijumpers.pkl", "rb"))
    hills = pickle.load(open("hills.pkl", "rb"))