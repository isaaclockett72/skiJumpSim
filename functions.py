#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:18:56 2020

@author: ikelockett
"""

import pandas as pd
from pandas import DataFrame
import random
from objects import Country, SkiJumper, Jump
import time
from console_formatting.formatting import dashed_line, kv_print, line_break
from console_formatting.ansi_colours import light_green, light_purple, light_white, yellow


def extract_hills(countries):
    """Extract the hills that were generated as part of the country gen."""
    hills_list = []
    for country in countries.values():
        hills_list.extend(country.hills)
    hills = {h.name: h for h in hills_list}
    return hills


def generate_countries(n=10):
    """Generate n countries."""
    countries_list = [Country() for x in range(n)]
    countries = {c.name: c for c in countries_list}
    return countries


def generate_skijumpers(countries, n=50):
    """Generate n ski jumpers, from the country list countries."""
    skijumpers_list = [SkiJumper(countries) for x in range(n)]
    skijumpers = {sk.name: sk for sk in skijumpers_list}
    return skijumpers


def go_to_next_hill(host_hills):
    """Move to the next hill in the tournament."""
    try:
        current_hill = host_hills.__next__()
    except StopIteration:
        print("Tournament complete!")
        current_hill = ""
    return current_hill


def obj_list_to_df(obj_list, index_col="name"):
    """Convert a list of objects to a df."""
    obj_dict = {k: v.__dict__ for k, v in obj_list.items()}
    obj_df = DataFrame(obj_dict).T
    obj_df = obj_df.set_index(index_col)
    for col in obj_df.columns:
        try:
            obj_df[col] = pd.to_numeric(obj_df[col])
        except (TypeError, ValueError):
            pass
    return obj_df


def select_country(countries):
    """Select and announce the country selected for the tournament."""
    host_countries = {k: v for k, v in countries.items() if v.hill_count > 0}
    tournament_country = random.choice(list(host_countries.values()))
    tournament_country.introduce_country()
    return tournament_country


def standard_round(hill, roster, skijumpers):
    """Run a standard round, in order of the roster."""
    results = {}
    jump_results = []
    i = 0
    try:
        while True:
            try:
                current_skijumper = skijumpers[roster.__next__()]
                i += 1
            except StopIteration:
                return results
            print(f"Jumper {i}")
            current_skijumper.print_stats()
            user_input = tap_to_continue()

            # BASIC RESULTS
            if results:
                # kv_print("Current Record", max(results.values()), "m")
                current_results = DataFrame(jump_results)
                print(current_results.sort_values("jump_distance",
                                                  ascending=False)[
                                                      ["skijumper",
                                                       "jump_distance"]].head(5))
                line_break()
            else:
                kv_print("Calculation line", hill.calculation_line, "m")
            # JUMP
            current_jump = Jump(current_skijumper, hill)
            current_jump.initiate_jump()

            jump_distance = max(round(current_jump.jump_distance, 2), 0)
            
            jump_results.append(current_jump.get_series_data())
            tap_to_continue()
            time.sleep(0.5)
            dashed_line(colour=light_green)
            kv_print("Result", jump_distance, "m")
            dashed_line(colour=light_green)
            results[current_skijumper.name] = jump_distance
            line_break()
            dashed_line()
            if jump_distance > hill.hill_record:
                print("\nIt's a new hill record!\n")
                line_break()
                hill.hill_record = jump_distance
            print(DataFrame(jump_results).sort_values("jump_distance",
                                              ascending=False)[
                                                  ["skijumper",
                                                   "home_country",
                                                   "jump_distance",
                                                   ]].head(5))
            user_input = tap_to_continue({"b": "Breakdown Results"})
            if user_input == "b":
                current_jump.print_jump_breakdown()
                tap_to_continue()
    except KeyboardInterrupt:
        return jump_results


def start_hill(hill, skijumpers):
    """Announce and begin the selected hill."""
    tap_to_continue()
    hill.print_stats()
    attendance = hill.calculate_attendance(skijumpers)
    kv_print("Attendance", f"{attendance:,}")
    if attendance == hill.capacity:
        line_break()
        print("It's a sellout!")

 
def tap_to_continue(options=None):
    """Pause until user enters a key."""
    if options:
        print(f"\n\n{yellow}**Custom options:")
        for option in options:
            kv_print((option, light_white), options[option])
    else:
        line_break()
    user_input = input(f"{light_purple}--- Tap Enter to continue ---\n\n{light_white}")
    return user_input
