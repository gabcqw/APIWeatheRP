import requests
from datetime import datetime
from datetime import timedelta
import os
import json
import re

#structure- class, function- reading, writting, and making request 
#class WeatherForecast:pass, wf = WeatherForecast()

def create_weather_folder():
    data_path_folder = "weather_report_folder"
    if not os.path.exists(data_path_folder):
        print("Cannot locate the folder.")
        os.makedirs(data_path_folder)


def get_weather_status_statment(status):
    status = float(status)
    if status > 0.0:
        return "It will rain"
    elif status == 0.0:
        return "It will not rain"
    else:
        return "Failed to fetch weather data from the API."
    
class WeatherForecast:
    request_url = "https://api.open-meteo.com/v1/forecast/"
    forecast_file_path = "forecast.txt"
    requests_params = {"daily": "precipitation_sum", "timezone": "Europe/London" }
    items = {}

    def __init__(self, latitude, longitude):
        self.requests_params['latitude'] = latitude
        self.requests_params['longitude'] = longitude
        self.init_items()
    
    def init_items(self):
        if not os.path.exists(self.forecast_file_path):
            return
        f = open(self.forecast_file_path, 'r')
        content = f.read()
        f.close()
        if not content:
            return
        else:
            f = open(self.forecast_file_path, 'r')
            for line in f.readlines():
                line = line.strip()
                k = line.split(' ')[0]
                v = line.split(' ')[1]
                self.items[k] = v;
            f.close()

    def __setitem__(self, date, weather_status):
        with open("summary.txt", "a") as file:
            file.write(f"{date}:{weather_status}\n")


    def fetch_weather_status(self) :
        try:
            response = requests.get(self.request_url, self.requests_params)
            response = json.loads(response.content)
            if 'daily' not in response:
                print(response['reason'])
                exit()
            daily = response['daily']
            precipitation_sum = daily['precipitation_sum'][0]
            return precipitation_sum
        except requests.exceptions.Timeout:
            print("request timeout")
            exit()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    

    def __getitem__(self, date):
        self.requests_params['start_date'] = date
        self.requests_params['end_date'] = date

        if not bool(self.items) or date not in self.items:
            print("date is not found")
            f = open(self.forecast_file_path, 'a+')
            weather_status = self.fetch_weather_status()
            f.write(str(date)+' '+str(weather_status)+'\n')
            f.close()
            self.items[date] = weather_status
            print("Weather data managed successfully:")
            return get_weather_status_statment(weather_status)
        else:
            return get_weather_status_statment(self.items[date])

    def __iter__(self):
        
        with open(self.file_path, "r") as file:
            for line in file:
                date, _ = line.strip().split(":")
                yield datetime.strptime(date, "%Y-%m-%d")



def get_user_input() : 
    user_input = input("Enter a date in the format 'YYYY-mm-dd' (or press Enter for the next day): ")
    if not user_input:
        return datetime.now() + timedelta(days=1)
    elif re.match('\d{4}-\d{2}-\d{2}', user_input):
        return user_input
    else :
        print("Invalid date format. Please enter a date in the format 'YYYY-mm-dd'.")
        exit()


def main():
    latitude = 51.903614
    longitude = -8.468399
    date = get_user_input()
    weather_forecast = WeatherForecast(latitude, longitude)
    print(f"Weather status for {date}:", weather_forecast[date])
    
    weather_forecast["2023-01-01"] = "not raining"

    


if __name__ == "__main__":
    main()

