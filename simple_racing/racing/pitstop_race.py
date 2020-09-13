# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""

from random import randint
from .race import Race
from .race_data import RaceData


class PitstopRace(Race):
    def __init__(self, track, laps, cars, pitstop=10):
        super().__init__(track, laps, cars)
        self._pitstop_time = pitstop

    @property
    def pitstop_time(self):
        return self.pitstop_time

    @pitstop_time.setter
    def pitstop_time(self, minutes=10):
        self.pitstop_time = minutes / 60

    def __car_timestamp(self, car):
        car_speed = randint(car.max_speed // 2, car.max_speed + 1)
        calc_distance = (self.__time_scale / 60) * car_speed
        loop_time = 0.0
        fuel_consumption = 0.0
        tanked = False

        if car.odometer + calc_distance > self.track.total_length:
            calc_distance = self.track.total_length - car.odometer

        if car.fuel_level > 0 and car.odometer < self.track.total_length:
            fuel_consumption, loop_time = car.drive(distance=calc_distance, speed=car_speed)

        if self.__is_end_of_fuel(car):
            car.tank_fuel(car.tank_capacity)
            tanked = True

        result = RaceData(self.__racing_time, car.name, car_speed, car.odometer, fuel_consumption, self.__calc_lap(car),
                          loop_time, tanked)
        return result, self.__is_finished(car)
