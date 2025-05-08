import requests
from bs4 import BeautifulSoup
import csv


url = 'https://tenki.jp/forecast/5/26/5110/23100/10days.html'

headers = {
    'User-Agent': 'Mozilla/5.0'
}
res = requests.get(url, headers=headers)
res.encoding = res.apparent_encoding 


soup = BeautifulSoup(res.text, 'html.parser')

forecast_items = soup.select('dd.forecast10days-actab')


weather_data = []

for item in forecast_items:

    divs = item.select('div')

    if len(divs) < 5:
        continue
   
    divs = divs[:5]  

    date = divs[0].get_text(strip=True)

    weather = divs[1].get_text(strip=True)

    temp = divs[2].get_text(strip=True)

    rain_chance = divs[3].get_text(strip=True)

    raw = divs[4].get_text(strip=True)
    if 'mm' in raw:
        rain_amount = raw
        reliability = ''
    else:
        rain_amount = ''
        reliability = raw

    weather_data.append([date, weather, temp, rain_chance, rain_amount,reliability])

print("🟢 forecast_items 数:", len(forecast_items))
print("🟢 weather_data 数:", len(weather_data))
print("🟢 これからCSVを書き出します")

with open('nagoya_14days_weather.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['日付','天気','気温','降水確率','降水量','信頼度'] )
    writer.writerows(weather_data)

print("✅ csvファイル 'nagoya_14days_weather.csv' を保存しました。")





