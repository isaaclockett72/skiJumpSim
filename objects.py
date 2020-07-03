#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 22:03:03 2020

@author: ikelockett
"""

import locale
import math
import numpy as np
from pandas import Series
import random
import country_naming as cn
from name_generator import generate_word
from console_formatting.formatting import dashed_line, kv_print, line_break
from console_formatting.ansi_colours import light_blue, light_green, light_white, yellow

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
        pass

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def introduce_country(self):
        """Announce a country upon arrival."""
        dashed_line()
        print(f"Welcome to {light_green}{self.name}")
        dashed_line()
        line_break()
        kv_print('Official country name', (self.full_name, light_green))
        kv_print('Population', f"{self.population:,}")
        kv_print('Hill count', self.hill_count)
        line_break()
        all_hills = ', '.join([hill.name for hill in self.hills])
        print("Hills:")
        print(f"""{light_green}{all_hills}{light_white}""")
        line_break()
        hill_name = self.hills[0].name
        print(f"Our first hill will be {light_green}{hill_name}{light_white}")
        pass


class Hill():
    """
    A hill is an object that can be jumped on.

    A hill is in a country, and is the home hill of ski jumpers
    """

    def __init__(self, country_name):

        self.country = country_name
        self.height = round(random.gauss(130, 6), 2)
        self.calculation_line = round(self.height * 0.9, 1)
        self.hill_record = self.calculation_line
        self.capacity = random.randint(1, 100000)
        self.wind_variability = random.randint(1, 10)
        self.name = self.generate_name()
        pass

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
        dashed_line()
        print(f"Welcome to {light_green}{self.name} Hill!")
        dashed_line()
        line_break()
        kv_print("Hill Name", (self.name, light_green))
        line_break()
        kv_print("Height", self.height, "m")
        kv_print("Calculation Line", self.calculation_line, "m")
        kv_print("Hill Record", self.hill_record, "m")
        line_break()
        kv_print("Hill Capacity", f"{self.capacity:,}")
        pass

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

        return round(max(min(
                random.gauss(
                    self.capacity/2 + base, self.capacity/3),
                self.capacity), 0))


class Jump():
    """A jump is something that a skijumper does to a hill."""

    def __init__(self, skijumper, hill, print_breakdown=False):
        """Initialise variables."""
        self.skijumper = skijumper
        self.hill = hill
        self.jump_distance = hill.calculation_line * 0.9
        self.estimate = self.jump_distance
        self.print_breakdown = print_breakdown
        pass

    def calculate_consistency_bonus(self):
        """Calculate consistency bonus."""
        self.consistency_bonus = round(
            np.mean([self.skijumper.consistency - 5, self.skijumper.form]), 2)
        self.jump_distance += self.consistency_bonus

    def calculate_father_bonus(self):
        """Calculate the penalty / bonus for father presence."""
        self.father_present = random.random()
        print(f"{light_white}They're looking around...")
        line_break()
        if self.father_present > 0.5:
            print(f"* Their father is in the crowd")
            line_break()
            self.father_bonus = round(
                (self.father_present-0.5) *
                self.skijumper.relationship_with_father, 2)
        else:
            print(f"* Looks like Dad didn't show up")
            line_break()
            self.father_bonus = round(
                (self.father_present - 0.5) *
                (10 - self.skijumper.relationship_with_father), 2)
        self.jump_distance += self.father_bonus
        self.estimate = round(self.estimate, 2)

    def calculate_form_bonus(self):
        """Calculate the form bonus."""
        self.form_bonus = self.skijumper.form
        self.jump_distance += self.skijumper.form
        self.estimate += self.skijumper.form

    def calculate_height_bonus(self):
        """Calculate the height bonus."""
        self.height_bonus = round(self.skijumper.height / self.hill.height, 2)
        self.jump_distance += self.height_bonus
        self.estimate += self.height_bonus
        pass

    def calculate_horizontal_wind(self):
        """Calculate the horizontal wind's impact on the jump."""
        self.wind_alpha = 2 / self.hill.wind_variability
        self.wind_horizontal = random.expovariate(self.wind_alpha)
        direction = -1 if random.random() < 0.5 else 1
        self.wind_horizontal *= direction
        self.wind_horizontal *= (self.skijumper.balance - 5)
        self.wind_horizontal = round(self.wind_horizontal, 2)
        self.angle = math.radians(self.wind_horizontal)
        self.jump_distance = self.jump_distance * math.cos(self.angle)

    def calculate_jump_speed(self):
        """Calculate the jump speed and bonus."""
        self.jump_bonus = round(random.randint(1, self.skijumper.speed), 1)
        self.jump_speed = round(self.hill.height/1.5 + self.jump_bonus, 1)
        self.jump_distance += self.jump_bonus/2
        pass

    def calculate_popularity_bonus(self):
        """Calculate popularity bonus."""
        if self.hill.name == self.skijumper.home_hill:
            self.hill_bonus = max((self.skijumper.popularity-5)/1.5, 0)
        else:
            self.hill_bonus = 0
        self.jump_distance += self.hill_bonus
        if self.hill.country == self.skijumper.country_of_origin:
            self.home_bonus = max(((self.skijumper.popularity-5)/2), 0)
        else:
            self.home_bonus = 0
        self.jump_distance += self.home_bonus
        pass

    def calculate_risk_bonus(self):
        """Calculate the risk bonus / penalty."""
        self.risk_bonus = round((2*random.random()-1) *
                                self.skijumper.risk_taking, 2)
        self.jump_distance += self.risk_bonus
        pass

    def calculate_weight_bonus(self):
        """Calculate the weight bonus."""
        self.weight_bonus = round(self.skijumper.height / self.skijumper.weight, 2)
        self.jump_distance += self.weight_bonus
        self.estimate += self.weight_bonus
        pass

    def get_series_data(self):
        """Return the jump data as a Series."""
        series_tmp = Series(self.__dict__)
        series_tmp["home_country"] = series_tmp["skijumper"].country_of_origin
        return series_tmp

    def initiate_jump(self):
        """Initiate the jump."""
        dashed_line()
        print(f"{light_green}{self.skijumper.name}{light_white} is beginnning their jump...")
        dashed_line()
        line_break()
        self.calculate_height_bonus()
        self.calculate_weight_bonus()
        self.calculate_popularity_bonus()
        self.calculate_consistency_bonus()
        self.calculate_jump_speed()
        self.calculate_risk_bonus()
        self.calculate_form_bonus()
        self.calculate_father_bonus()
        self.calculate_horizontal_wind()
        self.jump_distance = max(round(self.jump_distance, 2), 0)
        kv_print("Expected distance", self.estimate, "m")
        pass

    def print_jump_breakdown(self):
        """Print the jump breakdown results."""
        dashed_line(n=50)
        kv_print("Height Bonus", self.height_bonus, "m", signed=True)
        kv_print("Weight Bonus", self.weight_bonus, "m", signed=True)
        kv_print("Home Hill Bonus", self.hill_bonus, "m", signed=True)
        kv_print("Home Country Bonus", self.home_bonus, "m", signed=True)
        dashed_line(n=50)
        kv_print("Jump Speed", self.jump_speed, "km/h", signed=True)
        kv_print("Jump Speed Bonus", self.jump_bonus/2, "m", signed=True)
        dashed_line(n=50)
        kv_print("Consistency Bonus", self.consistency_bonus, "m", signed=True)
        kv_print("Risk Impact", self.risk_bonus, "m", signed=True)
        kv_print("Form Impact", self.form_bonus, "m", signed=True)
        kv_print("Father Presence", self.father_bonus, "m", signed=True)
        dashed_line(n=50)
        kv_print("Wind Horizontal", self.wind_horizontal, "km/h", signed=True)
        pass


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
        self.height = round(random.gauss(178, 10), 2)
        self.weight = round(random.gauss(64, 4), 2)
        self.popularity = random.randint(1, 10)
        self.speed = random.randint(1, 10)
        self.balance = random.randint(1, 10)
        self.style = random.randint(1, 10)
        self.consistency = random.randint(1, 10)
        self.risk_taking = random.randint(1, 10)
        self.relationship_with_father = random.randint(1, 10)
        self.set_form()
        self.assign_personality()
        pass

    def __repr__(self):
        """Use name for object representation."""
        return self.name

    def assign_personality(self):
        """Determine the personality traits of the skijumper."""
        self.personality = []
        if self.height > 180 and self.weight > 70:
            self.personality.append("Absolute Unit")
        if self.height / self.weight > 3:
            self.personality.append("Bulemic")
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
            self.personality.append("Paternally Fragile")
        if self.overall_score > 7:
            self.personality.append("Bookkeeper's Favourite")
        pass


    def print_stats(self):
        """Print out the stats for a ski jumper."""
        dashed_line()
        kv_print("Skijumper Name", (self.name, light_green))
        dashed_line()
        kv_print("Country", (self.country_of_origin, light_green))
        kv_print("Home Hill", (self.home_hill, light_green))
        line_break()
        # print(f"{yellow}{'-'*21} STATS {'-'*22}{light_white}")
        print(f"{yellow}{' STATS ':-^50}{light_white}")
        line_break()
        kv_print("Personality", (", ".join(self.personality), light_blue))
        kv_print("Height", round(self.height, 2), "cm")
        kv_print("Weight", round(self.weight, 2), "kg")
        kv_print("Popularity", self.popularity, colour_map=True, symbol="◼︎")
        kv_print("Speed", self.speed, colour_map=True, symbol="◼︎")
        kv_print("Balance", self.balance, colour_map=True, symbol="◼︎")
        kv_print("Style", self.style, colour_map=True, symbol="◼︎")
        kv_print("Consistency", self.consistency, colour_map=True, symbol="◼︎")
        kv_print("Risk taker", self.risk_taking, colour_map=True, symbol="◼︎")
        kv_print("Relationship with father", self.relationship_with_father,
                 colour_map=True, symbol="◼︎")
        line_break()
        print(f"{yellow}{' OVERALL SCORE ':-^50}{light_white}")
        kv_print("Overall score", self.overall_score)
        pass


    def set_form(self):
        """Pick the form for the ski jumper and reset score."""
        self.form = round(random.gauss(5, 2), 2)
        self.overall_score = round(np.mean([
            self.popularity, self.speed, self.balance,
            self.consistency, self.relationship_with_father,
            self.form]), 4)
        pass
