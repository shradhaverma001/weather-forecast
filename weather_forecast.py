import requests
import json
import datetime

# lat- 28.535517
# lon- 77.391029
# api key- 398c381047e6ad14ff4d2ebb7f560c08
config = {
    'apiKey': '398c381047e6ad14ff4d2ebb7f560c08'
}
print(
'''
    Welcome To Weather App
'''
)

print(
'''Please Select among these options
0 :=> to quit
1 :=> for latitude and longitude
2 :=> for city and date(YYYY-MM-DD) for scheduled flight
'''
)

# helper functions
def getPreviousDateTime(inputDate, noOfDay):
    cur_date=datetime.datetime.strptime(inputDate, '%Y-%m-%d').date()
    previous_date = cur_date - datetime.timedelta(days=noOfDay)

    timestamp = int((datetime.datetime(previous_date.year, previous_date.month, previous_date.day) - datetime.datetime(1970, 1, 1)).total_seconds())
    return timestamp


def getLatLong(cityName):
    url = 'http://api.openweathermap.org/geo/1.0/direct?limit=1&appid=' + config['apiKey']
    params = {
        "q": cityName
    }
    response = requests.get(url,params=params)
    data = response.json()
    citylat = data[0]["lat"]
    citylon = data[0]["lon"]
    return {
        'lat': citylat,
        'lon': citylon
    }


# def getCurrentWeather():
#     url = "http://api.openweathermap.org/data/2.5/weather?appid=" + config['apiKey']
#     params = {
#         "lat":lat,
#         "lon":lon
#     }
#     response = requests.get(url,params=params)
#     data = response.json()
#     print('')
#     print("Today's Weather Conditions")
#     print('')
#     print(f'Humidity: {data["main"]["humidity"]}')
#     print(f'Pressure: {data["main"]["pressure"]}')
#     print(f'Average Temperature: {data["main"]["temp"]}')
#     print(f'Wind Speed: {data["wind"]["speed"]}')
#     print(f'Wind Degree: {data["wind"]["deg"]}')
#     print('UV Index: Not available in API ')
#     print("")

class today:
    def __init__(self,lat,lon,test):
        self.lat=lat
        self.lon=lon
    def getCurrentWeather(self):
        url = "http://api.openweathermap.org/data/2.5/weather?appid=" + config['apiKey']
        params = {
            "lat":lat,
            "lon":lon
        }
        response = requests.get(url,params=params)
        data = response.json()
        print('')
        print("Today's Weather Conditions")
        print('')
        print(f'Humidity: {data["main"]["humidity"]}')
        print(f'Pressure: {data["main"]["pressure"]}')
        print(f'Average Temperature: {data["main"]["temp"]}')
        print(f'Wind Speed: {data["wind"]["speed"]}')
        print(f'Wind Degree: {data["wind"]["deg"]}')
        print('UV Index: Not available in API ')
        print("")

def getHistoryWeather(lat, lon, timestamp):
    # print(lat)
    # print(lon)
    # print(timestamp)
    url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?appid=' + config['apiKey']
    params = {
        'lat': lat,
        'lon': lon,
        'dt': timestamp
    }
    response = requests.get(url,params=params)
    data = response.json()
    # print(response.json())
    print(f'Humidity: {data["current"]["humidity"]}')
    print(f'Pressure: {data["current"]["pressure"]}')
    print(f'Average Temperature: {data["current"]["temp"]}')
    print(f'Wind Speed: {data["current"]["wind_speed"]}')
    print(f'Wind Degree: {data["current"]["wind_deg"]}')
    print(f'UV Index: {data["current"]["uvi"]} ')
    print("")


def getFutureForecast(lat,lon):
    url = 'https://api.openweathermap.org/data/2.5/onecall?&appid=' + config['apiKey']
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': "current,minutely,hourly,alerts"
    }
    # print(lat)
    # print(lon)
    # print(params['exclude'])
    response = requests.get(url,params=params)
    data = response.json()
    
    # print(response.json())
    for i in range(1,3):
        print(f'Forecast of the upcoming day {i} is: ')
        print(f'date: {datetime.datetime.fromtimestamp(data["daily"][i]["dt"]).strftime("%c")}')
        print(f'Humidity: {data["daily"][i]["humidity"]}')
        print(f'Pressure: {data["daily"][i]["pressure"]}')
        print(f'Average Temperature: {data["daily"][i]["temp"]["min"]} (showing minimum temp.)')
        print(f'Wind Speed: {data["daily"][i]["wind_speed"]}')
        print(f'Wind Degree: {data["daily"][i]["wind_deg"]}')
        print(f'UV Index: {data["daily"][i]["uvi"]} ')
        print("")
    
# def check(value):
#     switch()



while True:
    print("Enter the choice: ")
    try:
        x = int(input())
    except ValueError:
        print("Please enter a valid input!")
        continue

    if x == 0:
        break
    
    if(x == 1):
        print('Enter Latitude: ')
        lat=input()
        print('Enter Longitude: ')
        lon=input()
        obj1=today(lat,lon,{'apiKey': '398c381047e6ad14ff4d2ebb7f560c08'})
        obj1.getCurrentWeather()
    elif(x == 2):
        print('Enter City: ')
        city=input()
        print('Enter Date(YYYY-MM-DD): ')
        d=input()
        print("")

        # -----start of previous 2 day data

        # get previous 2 days data
        latLongDict = getLatLong(city)
        # previous day1
        print("Forecast of previous day before the entered date")
        previous1Time = getPreviousDateTime(d, 1)
        getHistoryWeather(latLongDict['lat'],latLongDict['lon'],previous1Time)

        # previous day2
        print("")
        print("Forecast of previous day 2")
        previous2Time = getPreviousDateTime(d, 2)
        getHistoryWeather(latLongDict['lat'],latLongDict['lon'],previous2Time)

        print("")
        # ------end of previous 2 day data

        # future days data
        getFutureForecast(latLongDict['lat'],latLongDict['lon'])

    else:
        print("Please enter a valid input!")




# TODO:FAILURE CONDITIONS
# PREVIOUS DATE NOT ANY DATA
# DECISION TO RE ENTER THE INPUT -Done
# USE CLASSES 
# MINIMUM 2 TEST CASES FOR BLOG PROJECT
# 



