# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""
import random
import json
from time import sleep, perf_counter
from typing import List
from .race_data import RaceData
from .track import Track


class Race:
    """
    module for creating car races

    input:
        track - class Track (defined race track)
        laps - number of laps
        *cars - class Cars (list of cars)
    methods:
        start - start the games
        ranking - returns a dictionary with a ranking of cars by race_time
        ranking_by - Returns a dictionary with a ranking sorted by the selected parameter
                                    for example: race_time, finished_laps, distance, avg_speed
        statistics - returns a dictionary with statistics
        parameters - returns a dictionary with race parameters
        save_to_file - allows you to save the ranking, statistics and parameters to a file
    """

    def __init__(self, track: Track, cars):
        """Class Race initialization"""
        self.track = track
        self.cars = cars
        self.__time_scale = 33
        self.__racing_time = 0
        self.__race_data = []

    @property
    def parameters(self):
        return {
            'race_name': self.track.name,
            'number_of_laps': self.track.laps,
            'race_length': self.track.total_length,
            'number_of_cars': len(self.cars),
            'cars': [car.name for car in self.cars]
        }

    @property
    def race_data(self):
        return self.__race_data

    @property
    def total_track_length(self):
        return self.track.total_length

    @property
    def time_scale(self):
        return self.__time_scale

    @time_scale.setter
    def time_scale(self, freq=60):
        if 100 <= freq >= 1:
            self.__time_scale = 1000//freq

    def __tank_all(self):
        for car in self.cars:
            car.tank_fuel(car.tank_capacity)

    def __is_finished(self, car):
        if car.odometer >= self.track.total_length:
            return True

    @staticmethod
    def __is_end_of_fuel(car):
        if car.fuel_level == 0:
            return True

    def __calc_lap(self, car):
        return car.odometer // self.track.lap_length

    def __car_timestamp(self, car):
        car_speed = random.randint(car.max_speed // 2, car.max_speed + 1)
        calc_distance = (self.__time_scale * car_speed) / 3600000
        loop_time = 0.0
        fuel_consumption = 0.0
        tanked = False

        if car.odometer + calc_distance > self.track.total_length:
            calc_distance = self.total_track_length - car.odometer

        if car.fuel_level > 0 and car.odometer < self.track.total_length:
            fuel_consumption, loop_time = car.drive(distance=calc_distance, speed=car_speed)

        finished = self.__is_end_of_fuel(car=car) or self.__is_finished(car)

        result = RaceData(self.__racing_time, car.name, car_speed, car.odometer, fuel_consumption, self.__calc_lap(car),
                          loop_time, tanked)
        return result, finished

    def __race_timestamp(self):
        number_of_car_ended = 0
        for car in self.cars:
            if car.fuel_level > 0 and not self.__is_finished(car):
                loop_data, finished = self.__car_timestamp(car)
                self.__race_data.append(loop_data)
                print(f'{car.name} - {car.odometer} km, {loop_data.loop_time}')
                if finished:
                    number_of_car_ended += 1
            sleep(self.__time_scale / 1000)
        return number_of_car_ended

    def start(self, time_scale=1):
        self.__tank_all()
        number_of_cars_in_race = len(self.cars)
        while number_of_cars_in_race > 0:
            number_of_cars_in_race -= self.__race_timestamp()
            # self.__racing_time += time_scale

    @staticmethod
    def _sort(dict_in, opt='race_time', reverse=False):
        result = {}
        temp_list = {}

        for car, details in dict_in.items():
            temp_list[car] = details[opt]

        for car, race_time in sorted(temp_list.items(), key=lambda x: x[1], reverse=reverse):
            result[car] = dict_in[car]

        return result

    def _ranking(self):
        result = {}

        for car in self.cars:
            result.update({car.name: {
                'time_total': self.sum_time_loops(car.name),
                'avg_speed': self.avg_speed(car.name),
                'min_speed': self.min_speed(car_name=car.name),
                'max_speed': self.max_speed(car_name=car.name),
                'laps': self.max_lap(car_name=car.name),
                'total_fuel_consumption': self.total_used_fuel(car_name=car.name)
            }
            })

        return result

    # def ranking_by(self, sort_by='race_time', reverse=False):
    # return self._sort(self._statistics['ranking'], opt=sort_by, reverse=reverse)

    @property
    def statistics(self):
        """
        this method allow to read the statistics about cars end times for each laps of the race

        returns:
                dict{'car': [time_of_lap_01, ...]}
        """
        result = []
        for item in self.__race_data:
            result.append((item.race_time, item.car_name, item.car_speed, item.odometer, item.fuel_consumption,
                           item.lap, item.loop_time, item.tanked))
        return result

    @property
    def ranking(self):
        """
            allow to read the ranking about cars end times for the race

            return:
                    dict{'car':
                                {race_time: time in hour,
                                 finished_laps: number of laps,
                                 distance: distance driven in the race
                                 avg_speed: average speed
                                }
                        }
        """

    # return self._statistics['ranking']
        return None
    # TODO: stworzyć ranking

    def save_to_file(self, filename):
        """
        function allow to save the statistics of race to file

        args:
            filename - path to file
        return:
            None
        """
        parameters = {'parameters': self.parameters}
        json_file = json.dumps(parameters, indent=4)

        with open(filename, 'w') as file:
            file.write(json_file)
        ...  # TODO: zapis wyscigu do pliku

    def car_list_with_statistics(self):
        result = []
        for entry in self.__race_data[::-1]:
            if not self.is_in_list(entry.car_name, result):
                result.append(
                    (
                        entry.car_name,
                        self.sum_time_loops(entry.car_name),
                        entry.lap,
                        entry.fuel_consumption,
                        entry.odometer,
                        self.avg_speed(entry.car_name)
                    )
                )

        return result

    def statistics_car(self):
        result = {}
        copy_race_data = self.__race_data.copy()

        for car in self.cars:
            for entry in copy_race_data:
                ...
        return result

    def ranking3(self, entries: List[RaceData]):
        cars = []
        for entry in entries:
            if not self.is_in_list(entry.car_name, cars):
                cars.append((
                    entry.car_name,
                    self.sum_time_loops(entry),
                    entry.lap
                ))
        result = sorted(cars, key=lambda tup: tup[1])
        result = sorted(result, key=lambda tup: tup[2], reverse=True)
        return result

    @staticmethod
    def is_in_list(search, lista: list):
        for item in lista:
            if search in item:
                return True

    def sum_time_loops(self, car_name):
        result = 0
        for entry in self.__race_data:
            if entry.car_name == car_name:
                result += entry.loop_time
        return result

    @staticmethod
    def _sum(*args):
        return sum(args)

    def total_used_fuel(self, **search_field):
        result = 0
        field, value = tuple(search_field.items())[0]
        for entry in self.__race_data:
            if getattr(entry, field) == value:
                result += entry.fuel_consumption
        return result

    def avg_speed(self, car_name):
        result = 0
        for entry in self.__race_data:
            if entry.car_name == car_name:
                if result == 0:
                    result = entry.car_speed
                else:
                    result = (result + entry.car_speed) / 2
        return result

    def max_speed(self, **search_field):
        result = 0
        field, value = tuple(search_field.items())[0]
        for entry in self.__race_data:
            if getattr(entry, field) == value:
                if entry.car_speed > result:
                    result = entry.car_speed
        return result

    def min_speed(self, **search_field):
        result = 0
        field, value = tuple(search_field.items())[0]
        for entry in self.__race_data:
            if getattr(entry, field) == value:
                if result == 0:
                    result = entry.car_speed
                elif entry.car_speed < result:
                    result = entry.car_speed
        return result

    def max_lap(self, **search_field):
        result = 0
        field, value = tuple(search_field.items())[0]
        for entry in self.__race_data:
            if getattr(entry, field) == value:
                if entry.lap > result:
                    result = entry.lap
        return result
