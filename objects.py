#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 22:03:03 2020

@author: ikelockett
"""

import locale
import numpy as np
import random
import country_naming as cn
from name_generator import generate_word

locale.setlocale(locale.LC_ALL, '')

class Hill():
    def __init__(self, country_name):
        self.country = country_name
        self.height = random.gauss(130,6)
        self.max_crowd_size = random.randint(0, 100000)
        self.name = generate_word(random.randint(2,3)).title()
        
    def __str__(self):
        return f"""
Hill Name:      {self.name}
Height:         {self.height}m
"""
        
    def __repr__(self):
        return self.name
        

class Country():
    def __init__(self):
        self.name = ""
        if random.random() > 0.1:
            self.name += random.choice(cn.country_titles) + " of "
        if random.random() > 0.8:
            self.name += random.choice(cn.country_interjections) + " "
        if random.random() > 0.5:
            naming = random.choice(cn.country_prefixes).title()
            self.name += generate_word(random.randint(1,2), starting_string=naming)
        else:
            self.name += generate_word(random.randint(1,2)).title()
            self.name += random.choice(cn.country_suffixes)
        self.population = random.randint(1, 2500000000)
        self.hill_count = random.choices(range(0,10), range(10, 0, -1))[0]
        self.hills = [Hill(self.name) for x in range(self.hill_count)]
        
        
    def __str__(self):
        return f"""
Name:           {self.name}
Population:     {self.population:,}
Hill Count:     {self.hill_count}
List of hills:  {[x.name for x in self.hills]}
"""

    def __repr__(self):
        return self.name


    
    
class SkiJumper():
    def __init__(self, countries):
        self.country_of_origin = random.choice(list(countries.values()))
        self.name = (
            generate_word(random.randint(1,2)).title() + " " +
            generate_word(random.randint(1,2)).title())
        try:
            self.home_hill = random.choice(self.country_of_origin.hills)
        except IndexError:
            self.home_hill = None
        self.height = random.gauss(178, 10)
        self.weight = random.gauss(64, 4)
        self.popularity = random.randint(1,10)
        self.speed = random.randint(1,10)
        self.balance = random.randint(1,10)
        self.stamina = random.randint(1,10)
        self.risk_taking = random.randint(1,10)
        self.relationship_with_father = random.randint(1,10)
        self.overall_score = round(np.mean([
            self.popularity, self.speed, self.balance, self.stamina,
            self.risk_taking, self.relationship_with_father]), 4)
    
    def __str__(self):
        return f"""
New Ski Jumper
Name:                       {self.name}
Country:                    {self.country_of_origin.name}
Home Hill:                  {self.home_hill.name}

------------- STATS -------------
Height:                     {round(self.height, 2)}cm
Weight:                     {round(self.weight, 2)}kg
Popularity:                 {self.popularity}/10
Speed:                      {self.speed}/10
Balance:                    {self.balance}/10
Stamina:                    {self.stamina}/10
Risk Taking Rank:           {self.risk_taking}/10
Relationship With Father:   {self.relationship_with_father}/10

--------- OVERALL SCORE ---------
Overall Score: {self.overall_score}
"""
    
    def __repr__(self):
        return self.name