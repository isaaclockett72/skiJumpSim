#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:18:56 2020

@author: ikelockett
"""

from objects import Hill, Country, SkiJumper

def generate_countries(n=10):
    countries_list = [Country() for x in range(n)]
    countries = {c.name: c for c in countries_list}
    return countries

def generate_skijumpers(countries, n=50):
    skijumpers_list = [SkiJumper(countries) for x in range(n)]
    skijumpers = {sk.name: sk for sk in skijumpers_list}
    return skijumpers

def extract_hills(countries):
    hills_list = []
    for country in countries.values():
        hills_list.extend(country.hills)
    hills = {h.name: h for h in hills_list}
    return hills