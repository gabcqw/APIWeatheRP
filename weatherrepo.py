import requests
from datetime import datetime
from datetime import timedelta
import pprint
import os
import pickle
#datetime.now().date(), datetime.strftime, datetime.strptime

URL_based = "https://api.open-meteo.com/v1/forecast/"
data_path_folder = "weather_report_folder"

#check if data folder excists
if not os.path.exists(data_path_folder):
     os.makedirs(data_path_folder)



#input date to search
searched_date = input("Enter a date in the format 'YYYY-mm-dd' (or press Enter for the next day): ")

if not searched_date:
    today= datetime.today()
    tomorrow = datetime.today()+ timedelta(days=1)
else:
    try:
        date_checked = datetime.strptime(searched_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter a date in the format 'YYYY-mm-dd'.")
        exit()
print(f"\n Request succeeded for {date_checked}. Generating data now. \n")

#geo status refers to CORK
latitude = 51.903614
longitude = -8.468399

#set parameters
params = {"latitude": latitude,
        "longitude": longitude,
        "daily": "precipitation_sum",
        "timezone": "Europe/London",
        "start_date": date_checked.strftime("%Y-%m-%d"),
        "end_date": date_checked.strftime("%Y-%m-%d") }

file_path = os.path.join(data_path_folder, f"{searched_date}.pickle")

#get data from cache
if os.path.exists(file_path):
    print(f"Data for the searched date is already stored, searching in the cache: \n")
    with open (file_path, 'rb') as f:
        data = pickle.load(f)
else:
    print(f"Data for the searched date does not exist in the cache. Generating data from API \n")
    params["start_date"] = searched_date
    params["end_data"] = searched_date
    resp = requests.get(url=URL_based, params=params)
    if resp.ok:
        data = (resp.json())
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    try:
        data = resp.json()
        precipitation_sum = data["daily"]["precipitation_sum"][0]
    except (requests.RequestException, KeyError):
        pprint("Failed to fetch weather data from the API.")
    if precipitation_sum is not None and precipitation_sum > 0.0:
        weather_status = f"Cork has {precipitation_sum} mm rain."
    elif precipitation_sum == 0.0:
        weather_status = "It will not rain."
    else:
        data = {}
        weather_status = "I don't know."
        print(f"Failed to access request. {weather_status}")


#store data in dict
print(data)