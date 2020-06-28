#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:05:07 2020

@author: ikelockett
"""

import functions as sk
import pickle



def create_world(reset_countries=True, reset_skijumpers=True):

    if reset_countries:
        countries = sk.generate_countries(n=25)
        hills = sk.extract_hills(countries)
        pickle.dump(countries, open("countries.pkl", "wb"))
        pickle.dump(hills, open("hills.pkl", "wb"))
    if reset_skijumpers:
        skijumpers = sk.generate_skijumpers(countries, n=100)
        pickle.dump(skijumpers, open("skijumpers.pkl", "wb"))