import requests
import sys
import json
import datetime
from datetime import date
import os
import time

string_from_terminal = str(sys.argv[1])

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"
querystring = {"lon": "18.48", "lat": "54.36"}

#with open("string.txt", "r") as f:
#    string_from_txt = f.read().strip()

file_date_check = time.ctime(os.path.getmtime("out.txt"))
file_date_check = datetime.datetime.strptime(file_date_check, "%a %b %d %H:%M:%S %Y")
file_date_is= file_date_check.strftime('%Y-%m-%d %H:%M:%S')    # mod file date
max_date = file_date_check + datetime.timedelta(days=1)

if datetime.datetime.now() < max_date:
    with open("out.txt", "r") as f:
        file_data = f.read()
        dane=json.loads(file_data)
else:
    headers = {
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
        'x-rapidapi-key': string_from_terminal
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    with open("out.txt", "w", encoding="UTF-8") as f:
        f.write(response.text)
        dane = response.json()

if len(sys.argv) > 2:
    check_date = sys.argv[2]
else:
    NextDay_Date = date.today() + datetime.timedelta(days=1)
    check_date = NextDay_Date.strftime("%Y-%m-%d")
    print(NextDay_Date.strftime("%Y-%m-%d"))
for day in dane["data"]:
    date = day["valid_date"]
    velessa = day["weather"]["description"]
    if date != check_date:
        continue
    if "Snow" in velessa or "snow" in velessa or "Rain" in velessa or "rain" in velessa:
        print("It's going to rain")
    else:
        print("It will not be raining")
    break
else:
    print("No idea!")