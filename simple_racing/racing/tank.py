# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""


class Tank():
	def __init__(self, capacity=60.0):
		self.capacity = capacity
		self._fuel_level = 0.0
		self._min_fuel_level = 10.0

	@property
	def min_fuel_level(self):
		"""
		the function returns information about the minimum fuel level at which the indicator light is on
		args:
		return:
		    min fuel level in liters
		"""
		return self._min_fuel_level

	@min_fuel_level.setter
	def min_fuel_level(self, volume):
		"""
		the function allow to set the minimum fuel level at which the indicator light is on
		args:
			volume in liters
		return:
		    None
		"""
		self._min_fuel_level = volume

	@property
	def fuel_level(self):
		return self._fuel_level

	def add_fuel(self, value):
		if self._fuel_level + value <= self.capacity:
			self._fuel_level += value
		else:
			self._fuel_level = self.capacity
			print('Nie możesz tyle zatankować!!')

	def sub_fuel(self, value):
		if self.fuel_level - value >= 0:
			self._fuel_level -= value
		else:
			self._fuel_level = 0

	# print('Już dawno nie masz paliwa w baku!!')

	@property
	def fuel_indicator(self):
		if self.fuel_level <= self._min_fuel_level:
			return True

		return False
