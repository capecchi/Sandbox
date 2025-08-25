# import matplotlib.pyplot as plt
import datetime
import numpy as np
import requests

url = 'https://www.runnersworld.com/uk/training/ultra/a774983/16-week-50-mile-ultra-marathon-training-schedule/'
r = requests.get(url)
training = r.text
training = training[training.find('The 50-mile Ultra Marathon training plan:'):]

day1 = datetime.datetime(2020, 5, 25)
tod = datetime.datetime.now()
tom = datetime.datetime.now() + datetime.timedelta(days=1)

wkday = tod.strftime('%A')  # Monday, Tuesday, etc.
next_wkday = tom.strftime('%A')
if next_wkday == 'Monday':
    next_text = 'Week'
else:
    next_text = next_wkday

weeknum = int(np.floor((tod-day1).days/7))
training = training[training.find(f'Week {weeknum}'):]
training = training[training.find(f'{wkday}:') + len(wkday) + 1:training.find(f'{next_text}')].strip()

if training == 'S&amp;C':
    training = 'Strength and Conditioning'

print(training)
