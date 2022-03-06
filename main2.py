import requests
import sys
import json
from datetime import date, datetime, timedelta
import time
import os


class WeatherForecast:
    def __init__(self, key):
        self.key = key
        self.dane = None
# self.check_date = check_date
# self.NextDay_Date=NextDay_Date

    def get_key(key):
        self.key = str(sys.argv[1])

    def get_data(self):
# ###print("get dates")
        url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"
        querystring = {"lon": "18.48", "lat": "54.36"}
        # with open("string.txt", "r") as f:
        #    string_from_txt = f.read().strip()

        file_date_check = time.ctime(os.path.getmtime("out2.txt"))
        file_date_check = datetime.strptime(file_date_check, "%a %b %d %H:%M:%S %Y")
        file_date_is = file_date_check.strftime('%Y-%m-%d %H:%M:%S')  # mod file date
        max_date = file_date_check + timedelta(days=1)

        if datetime.now() < max_date:
            with open("out2.txt", "r") as f:
                file_data = f.read()
# ##print("self-dane-0")
                self.dane = json.loads(file_data)
        else:
            headers = {
                'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
                'x-rapidapi-key': self.key
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            with open("out2.txt", "w", encoding="UTF-8") as f:
                f.write(response.text)
# ##print("self-dane-1")
                self.dane = response.json()

    def __getitem__(self, item):            # w item data
        if not self.dane:
            self.get_data()

    def weather_check(self):
        if not self.dane:
            self.get_data()
# ##print("wethercheck")
        if len(sys.argv) > 2:
            check_date = sys.argv[2]
        else:
            NextDay_Date = date.today() + timedelta(days=1)
            check_date = NextDay_Date.strftime("%Y-%m-%d")
# ##print(NextDay_Date.strftime("%Y-%m-%d"))
        for day in self.dane["data"]:
            date2 = day["valid_date"]
            velessa = day["weather"]["description"]
            if date2 != check_date:
                continue
            if "Snow" in velessa or "snow" in velessa or "Rain" in velessa or "rain" in velessa:
                print("Bedzie padac")
            else:
                print("Nie bedzie padac")
            break
        else:
            print("Nie wiem")

    def item_na_prognoze(self,day):
        velessa = day["weather"]["description"]
        if "Snow" in velessa or "snow" in velessa or "Rain" in velessa or "rain" in velessa:
           return "Bedzie padac"
        else:
           return "Nie bedzie padac"

    def items(self):                        # ma zwrocic generator tupli
# ##print(self.dane["data"])
        for item in self.dane["data"]:
# print(item["valid_date"])
# ## print(self.item_na_prognoze(item))
#for items in self.dane: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            yield item["valid_date"], self.item_na_prognoze(item)

    def __iter__(self):
        for nr in self.dane:
            yield nr
        return iter(self.dane)

    def __next__(self):
        pass


# 1. pogoda dla podanej daty
wf = WeatherForecast(sys.argv[1])
wf.weather_check()
# print(wf[check_date])

# 2 generator tupli w formacie (data, pogoda) dla już zcache’owanych rezultatów przy wywołaniu
"""for x, y in wf.items():
    print(x,y)"""
for z in wf.items():
    print(z)

# wf to iterator zwracający wszystkie daty, dla których znana jest pogoda
# printuje: "data"
# city_name
# lon
# timezone
# lat
# country_code
# state_code
#printuje 1 kolumne 1 element json, powienien 2 kolumne 20 elem2.pnt czyli:
for x in wf:
    print(x)

