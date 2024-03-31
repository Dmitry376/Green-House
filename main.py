import json
import requests
from flask import render_template, Flask, url_for, request
from markupsafe import escape


app = Flask(__name__)

data____ = requests.get("https://olimp.miet.ru/ppo_it_final/date", headers={'X-Auth-Token': 'ppo_9_30001'})
dates = data____.json()
print(dates)
# print(dates)
# print(data____.status_code)
assert data____.status_code == 200

big_data = []
for i in dates["message"][1:]:
    print(i)
    day, month, year = i.split("-")
    val = requests.get(f"https://olimp.miet.ru/ppo_it_final?day={day}&month={month}&year={year}", headers={'X-Auth-Token': 'ppo_9_30001'})
    big_data.append(val.json())
    data = val.json()["message"]

    print(data)

    floor_count = data["flats_count"]["data"]
    windows_for_rooms = data["windows_for_flat"]["data"]
    s = sum(windows_for_rooms)
    floors = data["windows"]["data"]
    all_bools = []

    for i in floors.values():
        all_bools.extend(i)

    floors_123 = []
    i = 0
    for floor in floors:
        k = 0
        res = []
        for j in windows_for_rooms:
            res.append(all_bools[i * s + k: i * s + k+j])
            k += j
        floors_123.append({i: res})
        i += 1

    rooms_count = 0
    c = 0
    rooms_nums = []
    for elem in floors_123:
        for i, j in elem.items():
            for k in j:
                c += 1
                if True in k:
                    rooms_count += 1
                    rooms_nums.append(c)



@app.route('/')
@app.route('/index')
def hello(floor_count=floor_count, windows_for_rooms=windows_for_rooms):
    return render_template('index.html', 
                           floor_count=floor_count, 
                           windows_for_rooms=windows_for_rooms,
                           rooms_count=rooms_count,
                           rooms_nums=rooms_nums)


if __name__ == '__main__':
    app.run()