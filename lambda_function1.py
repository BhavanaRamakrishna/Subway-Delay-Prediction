import json
import csv
import botocore
from botocore.vendored import requests

def lambda_handler(event, context):
    # TODO implement
    URL = 'http://api.openweathermap.org/data/2.5/forecast?q=Queens,us&appid={API-KEY}'
    r = requests.get(URL)
    data = r.json()
    length = len(data["list"])
    maximum_temp = []
    minimum_temp = []
    day = 0
    with open('weather.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['maxtemp', 'mintemp'])
        while day < length:
            max_temp = -999
            min_temp = 999
            for cur in range(day, day + 8):
                if cur < length:
                    temp_F = (9/5*(data["list"][cur]["main"]["temp_max"] - 273.15)) + 32
                    #print(temp_F)
                    max_temp = max(max_temp,temp_F)
            
#temp_min
                    temp_F1 = (9/5*(data["list"][cur]["main"]["temp_min"] - 273.15)) + 32
                #print(temp_F1)
                    min_temp = min(min_temp, temp_F1)
                    
            # maximum_temp.append(max_temp)
            # minimum_temp.append(min_temp)
            filewriter.writerow([max_temp, min_temp])
            day += 8
    print("Max", maximum_temp)
    print("Min", minimum_temp)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
