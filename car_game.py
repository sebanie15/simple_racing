# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from time import perf_counter

from simple_racing import Car, Track, Race

# print(help(Race))
track = Track(name='Tor wyścigowy', lap_length=0.01, laps=1)
car1 = Car(name='Volvo', avg_fuel_consumption=6.1, max_speed=220)
car1.tank_capacity = 70
car2 = Car(name='Mitsubishi', avg_fuel_consumption=2.2, max_speed=200)
car2.tank_capacity = 100
car3 = Car(name='Subaru', avg_fuel_consumption=5.5, max_speed=250)
car3.tank_capacity = 90
car4 = Car(name='Mazda', avg_fuel_consumption=10, max_speed=190)
car4.tank.capacity = 45
cars = (car1, car2, car3, car4)
race1 = Race(track=track, cars=cars)

race1.start(time_scale=5)

folder = ''
filename = f'{folder}{race1.track.name}_{dt.now()}.txt'
race1.save_to_file(filename)
# print(f'Volvo - {race1.sum_time_loops(car_name="Volvo")}')
# print(f'Volvo - {race1.sum2_time_loops(_sum, car_name="Volvo")}')

#print((race1._ranking()))

# for item in race1.race_data:
#	print(item)


print()
print('Ranking:')
print('-' * 20)
print((race1.car_list_with_statistics()))
print(race1._ranking())
# print(race1.ranking_by(sort_by='race_time', reverse=True))
# print(race1.ranking_by())

# for car, parameters in race1.ranking.items():
#	print(f'{car}:')
#	for key, value in parameters.items():
#		print(f'  - {key}: {value}')
