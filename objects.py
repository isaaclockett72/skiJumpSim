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
        self.population = random.randint(1, 25000000)
        self.hill_count = random.choices(range(0, 10), range(10, 0, -1))[0]
        self.hills = [Hill(self.name) for x in range(self.hill_count)]

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def introduce_country(self):
        """Announce a country upon arrival."""
        print(f"""
{"-" * 32}
Welcome to {self.name}
{"-" * 32}

Official country name:  {self.full_name}.
Population:             {self.population:,}.
Hill count:             {self.hill_count}

Hills:
    {", ".join([hill.name for hill in self.hills])}

Our first hill will be {self.hills[0].name}
""")


class Hill():
    """
    A hill is an object that can be jumped on.

    A hill is in a country, and is the home hill of ski jumpers
    """

    def __init__(self, country_name):

        self.country = country_name
        self.height = round(random.gauss(130, 6), 2)
        self.calculation_line = round(self.height * 0.9)
        self.hill_record = self.calculation_line
        self.capacity = random.randint(0, 100000)
        self.name = self.generate_name()

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def generate_name(self):
        """Generate the name for the hill."""
        starting_strings = [self.country[:2], ""]
        starting_weights = [2, 3]
        starting_string = random.choices(starting_strings, starting_weights)[0]
        return generate_word(random.randint(2, 3),
                             starting_string=starting_string).title()

    def print_stats(self):
        """Print stats for the hill."""
        print(f"""
{"-" * 32}
Welcome to {self.name} Hill!
{"-" * 32}

Hill Name:          {self.name}
Height:             {self.height}m
Calculation Line:   {self.calculation_line}m
Hill Record:        {self.hill_record}m
Capacity:           {self.capacity}
""")

    def calculate_attendance(self, skijumpers):
        """Calculate the attendance of the event."""
        home_country_count = 0
        home_hill_count = 0
        for skijumper in skijumpers:
            if skijumper.country_of_origin == self.country:
                home_country_count += 1
            if skijumper.home_hill == self.name:
                home_hill_count += 1
        base = (home_country_count * 2 +
                home_hill_count * 3) * self.capacity/100

        return round(min(
                random.gauss(
                    self.capacity/2 + base, self.capacity/3),
                self.capacity))


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
        self.style = random.randint(1, 10)
        self.consistency = random.randint(1, 10)
        self.stamina = random.randint(1, 10)
        self.risk_taking = random.randint(1, 10)
        self.relationship_with_father = random.randint(1, 10)
        self.set_form()
        self.assign_personality()

    def __repr__(self):
        """Use name for object representation."""
        return self.name
    
    def assign_personality(self):
        """Determine the personality traits of the skijumper."""
        self.personality = []
        if self.height > 180 and self.weight > 70:
            self.personality.append("Absolute Unit")
        if self.popularity == 10:
            self.personality.append("Fan Favourite")
        if self.speed == 10:
            self.personality.append("Speedster")
        if self.balance == 10:
            self.personality.append("Windproof")
        if self.style == 10:
            self.personality.append("Stylish")
        if (
            self.consistency > 8 and
            self.balance > 8 and
            self.style > 8
                ):
            self.personality.append("Perfect landing")
        if self.risk_taking > 9:
            self.personality.append("Daredevil")
        if self.relationship_with_father < 3:
            self.personality.append("Fragile")
        if self.overall_score > 7:
            self.personality.append("Bookkeepers' Favourite")


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
Style:                      {self.style}/10
Stamina:                    {self.stamina}/10
Consistency:                {self.consistency}/10
Risk Taker:                 {self.risk_taking}/10
Relationship With Father:   {self.relationship_with_father}/10

--------- OVERALL SCORE ---------
Overall Score: {self.overall_score}
""")

    def set_form(self):
        """Pick the form for the ski jumper and reset score."""
        self.form = random.gauss(5, 2)
        self.overall_score = round(np.mean([
            self.popularity, self.speed, self.balance, self.stamina,
            self.consistency,
            self.risk_taking, self.relationship_with_father,
            self.form]), 4)
        
    def jump(self, hill):
        base = hill.calculation_line
        random_jump_distance = random.gauss(base, base/12)
        return random_jump_distance
