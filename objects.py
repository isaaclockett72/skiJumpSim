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
    """
    A hill is an object that can be jumped on.

    A hill is in a country, and is the home hill of ski jumpers
    """

    def __init__(self, country_name):

        self.country = country_name
        self.height = random.gauss(130, 6)
        self.calculation_line = self.height * 0.9
        self.hill_record = self.calculation_line
        self.max_crowd_size = random.randint(0, 100000)
        self.name = generate_word(random.randint(2, 3)).title()

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def print_stats(self):
        """Print stats for the hill."""
        print(f"""
Hill Name:      {self.name}
Height:         {self.height}m
""")


class Country():
    """
    A country is a place where hills live.

    Ski jumpers come from countries.
    """

    def __init__(self):
        self.name = ""
        self.full_name = ""
        if random.random() > 0.1:
            self.full_name += random.choice(cn.country_titles) + " of "
        if random.random() > 0.8:
            self.name += random.choice(cn.country_interjections) + " "
        if random.random() > 0.5:
            naming = random.choice(cn.country_prefixes).title()
            self.name += generate_word(random.randint(1, 2),
                                       starting_string=naming)
        else:
            self.name += generate_word(random.randint(1, 2)).title()
            self.name += random.choice(cn.country_suffixes)
        self.full_name += self.name
        self.population = random.randint(1, 2500000000)
        self.hill_count = random.choices(range(0, 10), range(10, 0, -1))[0]
        self.hills = [Hill(self.name) for x in range(self.hill_count)]

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def introduce_country(self):
        """Announce a country upon arrival."""
        print(f"""
Our tournament takes place in: {self.full_name}.

This country has a population of {self.population:,}.
There are {self.hill_count} hills in total:
    {", ".join([hill.name for hill in self.hills])}

Our first hill will be {self.hills[0].name}
""")


class SkiJumper():
    """
    A ski jumper is a person who participates in ski jumps.

    A ski jumper comes from a country and may have a home hill.
    """

    def __init__(self, countries):
        country = random.choice(list(countries.values()))
        self.country_of_origin = country.name
        self.name = (
            generate_word(random.randint(1, 2)).title() + " " +
            generate_word(random.randint(1, 2)).title())
        try:
            self.home_hill = random.choice(country.hills).name
        except IndexError:
            self.home_hill = None
        self.height = random.gauss(178, 10)
        self.weight = random.gauss(64, 4)
        self.popularity = random.randint(1, 10)
        self.speed = random.randint(1, 10)
        self.balance = random.randint(1, 10)
        self.stamina = random.randint(1, 10)
        self.risk_taking = random.randint(1, 10)
        self.relationship_with_father = random.randint(1, 10)
        self.set_form()

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def print_stats(self):
        """Print out the stats for a ski jumper."""
        print(f"""
New Ski Jumper
Name:                       {self.name}
Country:                    {self.country_of_origin}
Home Hill:                  {self.home_hill}

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
""")

    def set_form(self):
        """Pick the form for the ski jumper and reset score."""
        self.form = random.gauss(5, 2)
        self.overall_score = round(np.mean([
            self.popularity, self.speed, self.balance, self.stamina,
            self.risk_taking, self.relationship_with_father,
            self.form]), 4)
