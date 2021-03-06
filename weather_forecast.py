import requests
import json
import datetime
import re

# lat- 28.535517
# lon- 77.391029
# api key- 398c381047e6ad14ff4d2ebb7f560c08
config = {
    'apiKey': '398c381047e6ad14ff4d2ebb7f560c08'
}

class Today:
    
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def is_valid(self):
        return (self.is_valid_lat() and self.is_valid_lon())

    def is_valid_lat(self):
        if (float(self.lat)<=90.0 and float(self.lat)>=-90.0):
            return True
        else:
            return False

    def is_valid_lon(self):
        if (float(self.lon)<=180.0 and float(self.lon)>=-180.0):
            return True
        else:
            return False
    
    def getCurrentWeather(self):
        url = "http://api.openweathermap.org/data/2.5/weather?appid=" + config['apiKey']
        params = {
            "lat": self.lat,
            "lon": self.lon
        }
        response = requests.get(url,params=params)
        data = response.json()
        # print(response.json())
        self.print_Weather(data)


    def print_Weather(self, data):
        if data is not None:
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
        else:
            print('Data is not available')
 

class History():

    def __init__(self, city, d, lat = None, lon = None, timestamp = None):
        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp
        self.city = city
        self.d = d

    def is_valid(self):
        return (self.is_valid_city() and self.is_valid_date())

    def is_valid_city(self):
        if (re.match(r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", self.city)):
            return True
        else:
            return False

    def is_valid_date(self):
        if (re.match(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",self.d)):
            return True
        else:
            return False

    def getPreviousDateTime(self, dayNo):
        cur_date=datetime.datetime.strptime(self.d, '%Y-%m-%d').date()
        previous_date = cur_date - datetime.timedelta(days = dayNo)

        self.timestamp = int((datetime.datetime(previous_date.year, previous_date.month, previous_date.day) - datetime.datetime(1970, 1, 1)).total_seconds())


    def getLatLong(self):
        url = 'http://api.openweathermap.org/geo/1.0/direct?limit=1&appid=' + config['apiKey']
        params = {
            "q": self.city
        }
        response = requests.get(url,params=params)
        data = response.json()
        if data:
            citylat = data[0]["lat"]
            citylon = data[0]["lon"]
            self.lat = citylat
            self.lon = citylon
            return True
        else:
            return False

    def getHistoryWeather(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?appid=' + config['apiKey']
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'dt': self.timestamp
        }
        response = requests.get(url,params=params)
        data = response.json()
        if data is not None and response.status_code==200:
            self.print_Weather(data)
        else:
            print('Data is not available')

        

    def print_Weather(self,data):
            print("")
            print(f'date: {datetime.datetime.fromtimestamp(data["current"]["dt"]).strftime("%c")}')
            print(f'Humidity: {data["current"]["humidity"]}')
            print(f'Pressure: {data["current"]["pressure"]}')
            print(f'Average Temperature: {data["current"]["temp"]}')
            print(f'Wind Speed: {data["current"]["wind_speed"]}')
            print(f'Wind Degree: {data["current"]["wind_deg"]}')
            print(f'UV Index: {data["current"]["uvi"]} ')
            print("")



    def getFutureForecast(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall?&appid=' + config['apiKey']
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'exclude': "current,minutely,hourly,alerts"
        }
        
        response = requests.get(url,params=params)
        data = response.json()
        if data is not None and response.status_code==200:
            for i in range(1,3):
                print("")
                print(f'date: {datetime.datetime.fromtimestamp(data["daily"][i]["dt"]).strftime("%c")}')
                print(f'Humidity: {data["daily"][i]["humidity"]}')
                print(f'Pressure: {data["daily"][i]["pressure"]}')
                print(f'Average Temperature: {data["daily"][i]["temp"]["min"]} (showing minimum temp.)')
                print(f'Wind Speed: {data["daily"][i]["wind_speed"]}')
                print(f'Wind Degree: {data["daily"][i]["wind_deg"]}')
                print(f'UV Index: {data["daily"][i]["uvi"]} ')
                print("")

        else:
            print('Data is not available')
        # print(response.json())
        
def main():
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
            lat = input()
            print('Enter Longitude: ')
            lon = input()
            todayObj = Today(lat,lon)
            if(todayObj.is_valid()):
                todayObj.getCurrentWeather()
            else:
                print("Please enter correct Latitude or Longitude!")
        elif(x == 2):
            print('Enter City: ')
            city = input()

            print('Enter Date(YYYY-MM-DD): ')
            d = input()
            print("")

            historyObj = History(city, d)
            if(historyObj.is_valid()):
                historyObj.getLatLong()
                print("Forecast of previous days")
                historyObj.getPreviousDateTime(1)
                historyObj.getHistoryWeather()
                print("")
                historyObj.getPreviousDateTime(2)
                historyObj.getHistoryWeather()
                print("")
                # future days data
                print("Forecast of upcoming days")
                historyObj.getFutureForecast()
            else:
                print('''Please enter correct city or
date format should be YYYY-MM-DD''')

            print("")

            

        else:
            print("Please enter a valid input!")

if __name__ == '__main__':
	main()