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
from formatting import dashed_line, kv_print, line_break
from ansi_colours import light_green, white, yellow

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
        dashed_line()
        print(f"Welcome to {light_green}{self.name}")
        dashed_line()
        line_break()
        kv_print('Official country name', (self.full_name, light_green))
        kv_print('Population', f"{self.population:,}")
        kv_print('Hill count', self.hill_count)
        line_break()
        print("Hills:")
        print(f"""{light_green}{', '.join([hill.name for hill in self.hills])}{white}""")
        line_break()
        print(f"Our first hill will be {light_green}{self.hills[0].name}{white}")


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
        dashed_line()
        print(f"Welcome to {light_green}{self.name} Hill!")
        dashed_line()
        line_break()
        kv_print("Hill Name", (self.name, light_green))
        kv_print("Height", self.height, "m")
        kv_print("Calculation Line", self.calculation_line, "m")
        kv_print("Hill Record", self.hill_record, "m")
        kv_print("Hill Capacity", f"{self.capacity:,}")

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
            self.personality.append("Fragile")
        if self.overall_score > 7:
            self.personality.append("Bookkeeper's Favourite")

    def print_stats(self):
        """Print out the stats for a ski jumper."""
        dashed_line()
        kv_print("Skijumper Name", (self.name, light_green))
        dashed_line()
        kv_print("Country", (self.country_of_origin, light_green))
        kv_print("Home Hill", (self.home_hill, light_green))
        line_break()
        print(f"{yellow}------------- STATS -------------{white}")
        line_break()
        kv_print("Personality", ", ".join(self.personality))
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
        print(f"{yellow}--------- OVERALL SCORE ---------{white}")
        kv_print("Overall score", self.overall_score)

    def set_form(self):
        """Pick the form for the ski jumper and reset score."""
        self.form = round(random.gauss(5, 2), 2)
        self.overall_score = round(np.mean([
            self.popularity, self.speed, self.balance,
            self.consistency, self.relationship_with_father,
            self.form]), 4)

    def jump(self, hill, breakdown=False):
        """Make the skijumper jump on the selected hill."""
        dashed_line()
        print(f"{light_green}{self.name}{white} is beginnning their jump...")
        dashed_line()
        line_break()

        base = hill.calculation_line
        estimation = base

        # HEIGHT BONUS
        height_bonus = round(self.height / hill.height, 2)
        base += height_bonus
        estimation += height_bonus
        # print(f"""Height bonus: {height_bonus}""")

        # WEIGHT BONUS
        weight_bonus = round(self.height / self.weight, 2)
        base += weight_bonus
        base += weight_bonus
        # print(f"""Weight bonus: {weight_bonus}\n""")

        # POPULARITY IMPACT
        if hill.name == self.home_hill:
            hill_bonus = max((self.popularity-5), 0)
            base += hill_bonus
            # print(f"Home hill popularity bonus: {hill_bonus}")
        else:
            hill_bonus = 0
        if hill.country == self.country_of_origin:
            # print(f"Popularity: {self.popularity}")
            home_bonus = max(((self.popularity-5)/2), 0)
            base += home_bonus
            # print(f"Home popularity bonus: {home_bonus}\n")
        else:
            home_bonus = 0

        # JUMP SPEED SIMPLE
        jump_bonus = round(random.randint(1, self.speed), 1)
        jump_speed = round(hill.height/1.5 + jump_bonus, 1)

        base += jump_bonus/2

        # print(f"Jump speed: {jump_speed}km/h")
        # print(f"Jump speed bonus: {jump_bonus/2}\n")

        # BALANCE OMITTED UNTIL WIND GENERATED

        # STYLE OMITTED UNTIL STYLE POINTS

        # CONSISTENCY CALCULATION
        consistency_bonus = round(
            np.mean([self.consistency - 5, self.form]), 2)
        base += consistency_bonus
        # print(f"Consistency bonus: {consistency_bonus}")

        # TAKE A RISK
        risk_bonus = round((2*random.random()-1) * self.risk_taking, 2)
        base += risk_bonus
        # print(f"Risk impact: {risk_bonus}")

        # ADD FORM
        base += self.form
        estimation += self.form
        # print(f"Form impact: {self.form}\n")

        # FATHER PRESENCE
        father_present = random.random()
        print(f"{white}They're looking around...")
        if father_present > 0.5:
            print(f"* Their father is in the crowd")
            line_break()
            father_bonus = round((father_present-0.5) *
                                 self.relationship_with_father, 2)
        else:
            print(f"* Looks like Dad didn't show up")
            line_break()
            father_bonus = round((father_present-0.5) *
                                 (10 - self.relationship_with_father), 2)
        base += father_bonus
        estimation = round(estimation, 2)

        if breakdown:
            dashed_line(n=50)
            kv_print("Height Bonus", height_bonus, "m")
            kv_print("Weight Bonus", weight_bonus, "m")
            kv_print("Home Hill Bonus", hill_bonus, "m")
            kv_print("Home Country Bonus", home_bonus, "m")
            dashed_line(n=50)
            kv_print("Jump Speed", jump_speed, "km/h")
            kv_print("Jump Speed Bonus", jump_bonus/2, "m")
            dashed_line(n=50)
            kv_print("Consistency Bonus", consistency_bonus, "m")
            kv_print("Risk Impact", risk_bonus, "m")
            kv_print("Form Impact", self.form, "m")
            kv_print("Father Presence", father_bonus, "m")
            dashed_line(n=50)
        kv_print("Expected distance", estimation, "m")
        line_break()
        random_jump_distance = random.gauss(base, base/24)
        return round(random_jump_distance, 2)
