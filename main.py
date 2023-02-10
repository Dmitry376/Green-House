import sqlite3 as sl
import requests
import json
import datetime
import pandas as pd
import streamlit as st

def session():
    con = sl.connect('data.db')
    with con:
        sql_data = con.execute("select count(*) from sqlite_master where type='table' and name='temp'")
        for row in sql_data:
            if row[0] == 0:
                con.execute("""
                    CREATE TABLE temp (
                    date TEXT,
                    time TEXT PRIMARY KEY,
                    temp_1 REAL,
                    temp_2 REAL,
                    temp_3 REAL,
                    temp_4 REAL,
                    avg_temp REAL
                    );
                    """)
        sql_data = con.execute("select count(*) from sqlite_master where type='table' and name='hum'")
        for row in sql_data:
            if row[0] == 0:
                con.execute("""
                    CREATE TABLE hum (
                    date TEXT,
                    time TEXT PRIMARY KEY,
                    hum_1 REAL,
                    hum_2 REAL,
                    hum_3 REAL,
                    hum_4 REAL,
                    avg_hum REAL
                    );
                    """)
        sql_data = con.execute("select count(*) from sqlite_master where type='table' and name='soil'")
        for row in sql_data:
            if row[0] == 0:
                con.execute("""
                    CREATE TABLE soil (
                    date TEXT,
                    time TEXT PRIMARY KEY,
                    soil_1 REAL,
                    soil_2 REAL,
                    soil_3 REAL,
                    soil_4 REAL,
                    soil_5 REAL,
                    soil_6 REAL
                    );
                    """)
    return con


def stop_session():
    con = session()
    with con:
        con.execute("DELETE FROM temp")
        con.execute("DELETE FROM hum")
        con.execute("DELETE FROM soil")
    con.close()
    
def data_update():
    con = session()
    temp_link = 'https://dt.miet.ru/ppo_it/api/temp_hum/'
    temp_sql = 'INSERT INTO temp (date, time, temp_1, temp_2, temp_3, temp_4, avg_temp) values(?, ?, ?, ?, ?, ?, ?)'
    hum_sql = 'INSERT INTO hum (date, time, hum_1, hum_2, hum_3, hum_4, avg_hum) values(?, ?, ?, ?, ?, ?, ?)'
    temp = [0]*4
    hum = [0]*4
    for i in range(4):
        response = requests.get(temp_link + str(i + 1))
        if response.status_code != 200:
            temp[i] = 0
            hum[i] = 0
            continue
        data = json.loads(response.text)
        temp[i] = data['temperature']
        hum[i] = data['humidity']
    soil_link = 'https://dt.miet.ru/ppo_it/api/hum/'
    soil_sql = 'INSERT INTO soil (date, time, soil_1, soil_2, soil_3, soil_4, soil_5, soil_6) values(?, ?, ?, ?, ?, ?, ?, ?)'
    soil = [0]*6
    for i in range(6):
        response = requests.get(soil_link + str(i + 1))
        if response.status_code != 200:
            soil[i] = 0
            continue
        data = json.loads(response.text)
        soil[i] = data['humidity']
    dt = datetime.datetime.now()
    time = (dt.strftime("%H:%M:%S"),)
    date = (dt.strftime("%d-%m-%Y"),)
    avg_temp = sum(temp)/4
    avg_temp = float("{:.2f}".format(avg_temp))
    avg_hum = sum(hum)/4
    avg_hum = float("{:.2f}".format(avg_hum))
    with con:
        con.execute(temp_sql, date + time + tuple(temp) + (avg_temp,))
        con.execute(hum_sql, date + time + tuple(hum) + (avg_hum,))
        con.execute(soil_sql, date + time + tuple(soil))
    return temp, hum, soil

def fork(state):
    link = "https://dt.miet.ru/ppo_it/api/fork_drive?state=" + str(state)
    response = requests.patch(link)
    return response.status_code

def watering(device_id, state):
    link = "https://dt.miet.ru/ppo_it/api/watering?state=" + str(state) + "&id=" + str(device_id)
    response = requests.patch(link)
    return response.status_code

def total_hum(state):
    link = "https://dt.miet.ru/ppo_it/api/total_hum?state=" + str(state)
    response = requests.patch(link)
    return response.status_code

def table_to_df(table_name):
    return pd.read_sql_query("select * from " + table_name, session())

def main():
    with open("properties.json", "r") as read_file:
        data = json.load(read_file)
    T = data['T']
    H = data['H']
    Hb = data['Hb']
    hand = data['hand']
    fork_state = data['airing']
    hum_state = data['humidification']
    st.title("Данные с датчиков температуры и влажности")
    
main()