# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""

from dataclasses import dataclass


@dataclass
class Parameters:
	race_name: str
	number_of_laps: int
	length_of_lap: float
	number_of_cars: int
	cars_names: []


@dataclass
class RaceData:
	race_time: int
	car_name: str
	car_speed: int
	odometer: int
	fuel_consumption: float
	lap: int
	loop_time: float
	tanked: bool = False
