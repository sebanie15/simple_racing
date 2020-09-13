# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""

from .tank import Tank


class Car():
    """
    testowa wartość

    """

    def __init__(self, name, avg_fuel_consumption=0.0, max_speed=100):
        self.name = name
        self.avg_fuel_consumption = avg_fuel_consumption
        self._max_speed = max_speed
        self.tank = Tank()
        self._is_wrecked = False
        self._odometer = 0

    @property
    def is_wrecked(self):
        """ funkcja zwraca informację czy auto jest powypadkowe czy też nie

        Parameters:

        Returns:
            state of arg is_wrecked -> True or False
        """
        return self._is_wrecked

    @is_wrecked.setter
    def is_wrecked(self, state):
        """
        this function allows you to change the value of the argument is_wrecked

        Parameters:
            state(bool): True or False
        Returns:

        """
        self._is_wrecked = state
        if self._is_wrecked is True:
            print('Uszkodzone')

    @property
    def max_speed(self):
        """
        function returns the number of kilometers traveled
        args:
        return:
            max_speed
        """
        return self._max_speed

    @property
    def odometer(self):
        """
        function returns the value of

        args:

        return:
            odometer value
        """
        return self._odometer

    @property
    def fuel_level(self):
        """
        function returns the value of the fuel level in the tank

        args:
        return:
            fuel_level
        """
        return self.tank.fuel_level

    def drive(self, distance, speed):
        """
        the function calculates how much fuel we use to travel a given distance
        and calculates how much time we need to cover this distance with the given speed

        args:
            distance [km]
            speed    [km/h]
        return:
            used_fuel [l]
            time_of_travel [h]
        """
        possible_distance = (self.tank.fuel_level / (speed * self.avg_fuel_consumption / 100))

        if possible_distance >= distance:
            norm_distance = distance
        else:
            norm_distance = possible_distance

        used_fuel = norm_distance / 100 * self.avg_fuel_consumption
        self.tank.sub_fuel(used_fuel)
        self._odometer += norm_distance

        if norm_distance > 0:
            time_of_travel = norm_distance / speed
        else:
            time_of_travel = 0

        return used_fuel, time_of_travel

    @property
    def tank_capacity(self):
        """
        function returns the value of the tank capacity

        args:
        return:
            tank capacity in liters
        """
        return self.tank.capacity

    @tank_capacity.setter
    def tank_capacity(self, volume:float):
        """
        function allows you to set the value of an argument concerning the tank capacity

        args:
            volume in liters
        return:
            None
        """
        self.tank.capacity = volume


    def tank_fuel(self, volume):
        """
        function allows you to add fuel to the tank

        args:
            volume in liters
        return:
            None
        """
        self.tank.add_fuel(volume)
