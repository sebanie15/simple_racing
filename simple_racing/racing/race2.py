# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""
import random
import json
from time import sleep, perf_counter
from typing import List
from racing import Car, Track, RaceData, Parameters


class Race():
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

	def __init__(self, track: Track, laps: int, cars: tuple):
		"""Class Race initialization"""
		self.track = track
		self.laps = laps
		self.cars = cars
		self._winner = ('',)
		self.__parameters = {
			'race_name': self.track.name,
			'number_of_laps': self.laps,
			'length_of_lap': self.track.length,
			'number_of_cars': len(self.cars),
			'cars': [car.name for car in self.cars]
		}
		self.__race_data = []
		self._statistics = {'parameters': {'race_name': self.track.name,
		                                   'number_of_laps': self.laps,
		                                   'length_of_lap': self.track.length,
		                                   'number_of_cars': len(self.cars),
		                                   'cars': [car.name for car in self.cars],
		                                   },
		                    'ranking': {},
		                    'statistics': {}
		                    }

	def start(self, time_scale=1):
		"""
		this method starts the entire race
		first of all, it refuels the cars to full tank
		then in the loop from 1 to the number of laps for each car checks if there is fuel in the tank.
		if there is fuel in the tank, it allows the car to drive the length of the lap at random speed
		 end calculated lap time is added to the statistics
		if there is no fuel in the tank - 0 lap time is added to the statistics
		"""
		self._statistics['parameters'].update({'refresh_rate': time_scale})
		self.__parameters.update({'refresh_rate': time_scale})

		temp_dict = {}
		for car in self.cars:
			car.tank_fuel(car.tank_capacity)  # tank
			temp_dict[car.name] = {}

		self._statistics['statistics'] = temp_dict

		racing_time = 0
		distance = self.track.length * self.laps
		lap = 0
		fuel_supply = 0
		number_of_cars_in_race = len(self.cars)
		tanked = False
		while number_of_cars_in_race > 0:
			for car in self.cars:
				car_speed = random.randint(car.max_speed // 2, car.max_speed + 1)
				calc_distance = time_scale / 60 * car_speed
				if car.odometer + calc_distance > distance:
					calc_distance = distance - car.odometer

				if car.fuel_level > 0 and car.odometer < distance:
					_, loop_time = car.drive(distance=calc_distance,
					                         speed=car_speed)
					if car.odometer >= distance:
						print(f'{car.name} właśnie skończył wyścig')

					if car.fuel_level == 0:
						print(f'{car.name} skończyło się paliwo')
						car.tank_fuel(car.tank_capacity)
						print(f'{car.name} zatankował się, doliczono 10 min')
						loop_time += 0.16666  # 10 min = 0,16666 h
						tanked = True

					if car.odometer >= distance or car.fuel_level == 0:
						number_of_cars_in_race -= 1

					fuel_supply += car.fuel_level

					lap = car.odometer // self.track.length
					if lap > self.laps:
						break

					car_dict = self._statistics['statistics'][car.name]
					loop_dict = {racing_time + time_scale: {
						'car_speed': car_speed,
						'odometer': car.odometer,
						'fuel_level': car.fuel_level,
						'lap': lap,
						'loop_time': loop_time,
						'tanked': tanked
					}}
					car_dict.update(loop_dict)
					car_statistics = {car.name: car_dict}
					self._statistics.update(car_statistics)

					self.__race_data.append(RaceData(
						car_name=car.name,
						car_speed=car_speed,
						odometer=car.odometer,
						fuel_level=car.fuel_level,
						lap=lap,
						loop_time=loop_time,
						tanked=tanked
					))

			racing_time += time_scale
			tanked = False

			if fuel_supply > 0:
				fuel_supply = 0
			else:
				end_race = True

		print('End of race')
		# sleep(1)

		#self._ranking()
		#print(self.car_list_with_stat(self.__race_data))

	# self._winner_is(self._statistics)

	@property
	def race_data(self):
		return self.__race_data

	def _sort(self, dict_in, opt='race_time', reverse=False):
		result = {}
		temp_list = {}

		for car, details in dict_in.items():
			temp_list[car] = details[opt]

		for car, race_time in sorted(temp_list.items(), key=lambda x: x[1], reverse=reverse):
			result[car] = dict_in[car]

		return result
	def _sort2(self, entries: List[RaceData]):

		return sorted(entries)

	def _ranking(self):
		result = {}
		avg_speed = 0.0
		distance = 0
		race_time = 0
		max_lap = 0

		for car, statistics in self._statistics['statistics'].items():
			for _, parameters in statistics.items():
				for key, parametr in parameters.items():
					if key == 'lap':
						if parametr > max_lap:
							max_lap = int(parametr)
					if key == 'odometer':
						if parametr > distance:
							distance = parametr

				avg_speed = parameters['car_speed']
				for lap in range(1, max_lap + 1):
					avg_speed = (avg_speed + parameters['car_speed']) / 2
					race_time += parameters['loop_time']

			result[car] = {
				'race_time': race_time / 60,
				'finished_laps': max_lap,
				'distance': distance,
				'avg_speed': avg_speed
			}

			max_lap = 0
			race_time = 0
			distance = 0

		self._statistics['ranking'] = self._sort(dict_in=result, opt='race_time')

	def ranking_by(self, sort_by='race_time', reverse=False):

		return self._sort(self._statistics['ranking'], opt=sort_by, reverse=reverse)

	@property
	def statistics(self):
		"""
		this method allow to read the statistics about cars end times for each laps of the race

		returns:
				dict{'car': [time_of_lap_01, ...]}
		"""
		return self._statistics['statistics']

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
		return self._statistics['ranking']

	@property
	def parameters(self):
		"""
		this method allow to read parameters of a race

		return:
				dict{'car':
									{'time":
													{'car_speed': value,
													 'odometer': value,
													 'fuel_level': value,
													 'lap': number of lap
													}
									}
					}
	"""
		return self._statistics['parameters']

	def save_to_file(self, filename):
		"""
		function allow to save the statistics of race to file

		args:
			filename - path to file
		return:
			None
		"""
		json_file = json.dumps(self._statistics, indent=4)

		with open(filename, 'w') as file:
			file.write(json_file)

	def car_list_with_stat(self, entries: List[RaceData]):
		result = []
		for entry in entries[::-1]:
			if not self.is_in_list(entry.car_name, result):
				result.append(
					(
						entry.car_name,
						self.sum_time_loops(entries, car_name=entry.car_name),
						entry.lap,
						entry.fuel_level,
						entry.odometer,
						self.avg_speed(entries, car_name=entry.car_name)
					)
				)

		return result

	def ranking3(self, entries: List[RaceData]):
		cars = []
		for entry in entries:
			if not self.is_in_list(entry.car_name, cars):
				cars.append((
					entry.car_name,
					self.sum_time_loops(
						entries,
						car_name=entry.car_name,
					),
					entry.lap
				))
		result = sorted(cars, key=lambda tup: tup[1])
		result = sorted(result, key=lambda tup: tup[2], reverse=True)
		return result

	def is_in_list(self, search, list: list):
		for item in list:
			if search in item:
				return True

	def sum_time_loops(self, entries: List[RaceData], **serch_field):
		result = 0
		field, value = tuple(serch_field.items())[0]
		for entry in entries:
			if getattr(entry, field) == value:
				result += entry.loop_time
		return result

	def avg_speed(self, entries: List[RaceData], **serch_field):
		result = 0
		field, value = tuple(serch_field.items())[0]
		for entry in entries:
			if getattr(entry, field) == value:
				if result == 0:
					result = entry.car_speed
				else:
					result = (result + entry.car_speed) / 2
		return result