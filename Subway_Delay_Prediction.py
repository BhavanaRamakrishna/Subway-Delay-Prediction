#!/usr/bin/env python
import pandas as pd
import numpy as np
import requests
import json
import math
from sklearn.linear_model import LinearRegression

#read data
subway_delay = pd.read_csv("Monthly_Subway_Line_Delay_Data.csv")
weather_data = pd.read_csv("Monthly_Weather_Data.csv")

#obtain number of passengers for the line given month
num_passengers = subway_delay[['Month','line', 'num_passengers']]
#obtain average dealy time for the line given month
subway_delay = subway_delay[['Month','line', 'num_passengers','average_delay_time']]
weather_data1 = weather_data[['Month','Max_Temp', 'Min_Temp']]
weather_data2 = weather_data[['Month','Max_Temp', 'Min_Temp']]

#obtain request line information
request_line = "1"
line = "line"
mask = num_passengers['line'] == request_line
#filter input for given line
num_passengers = num_passengers[mask]
mask = subway_delay['line'] == request_line
#filter input for given line
subway_line = subway_delay[mask]

#obtain train data with num of passengers
result = pd.merge(weather_data1, num_passengers, on='Month')
train_data  = result[['Max_Temp', 'Min_Temp','num_passengers']]

#weather api
URL = 'http://api.openweathermap.org/data/2.5/forecast?q=Queens,us&appid=1026b7625ff1ec232a7927edbe48af1e'
r = requests.get(URL)
data = r.json()
length = len(data["list"])
maximum_temp = []
minimum_temp = []
day = 0
while day < length:
	max_temp = -999
	min_temp = 999
	for cur in range(day, day + 8):
		if cur < length:
			temp_F = (9/5*(data["list"][cur]["main"]["temp_max"] - 273.15)) + 32
			max_temp = max(max_temp,temp_F)


			temp_F1 = (9/5*(data["list"][cur]["main"]["temp_max"] - 273.15)) + 32
			min_temp = min(min_temp, temp_F1)
	maximum_temp.append(max_temp)
	minimum_temp.append(min_temp)
	day += 8

#maximum and minum temperatures for next 5 days
# print(maximum_temp)
# print(minimum_temp)


dictionary = {'Max_Temp': maximum_temp, 'Min_Temp' : minimum_temp}
test_data = pd.DataFrame(dictionary)
npMatrix = np.matrix(train_data)

X, Y = npMatrix[:,0:2], npMatrix[:,2]

#fit linear regression to predict number of passengers
Linreg = LinearRegression().fit(X,Y)
results = Linreg.predict(test_data)
results = [math.ceil(i) for i in results]


test_data['num_passengers'] = results
result = pd.merge(weather_data2, subway_line, on='Month')
#training data including num of passengers
train_data  = result[['Max_Temp', 'Min_Temp','num_passengers','average_delay_time']]
npMatrix = np.matrix(train_data)
X, Y = npMatrix[:,0:3], npMatrix[:,3]

#fit linear regression to predict average delay per day
Linreg = LinearRegression().fit(X,Y)
results = Linreg.predict(test_data)
results



time = []
for result in results:
	current = []
	minute = math.floor(result)
	seconds = (result * 60)%60
	output = str(minute) + ' minute, ' + str(int(seconds)) + ' seconds'
	time.append(output)
# print(time)
