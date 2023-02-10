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
    st.set_page_config(
        page_title = "Temp and hum data",
        layout = "wide")
    st.title("Данные с датчиков температуры и влажности")
    if hand:
        st.subheader("Включен ручной режим управления")

    resbtn = st.button("Обновить данные")
    if resbtn:
        st.experimental_rerun()
        
    col1, col2 = st.columns(2)
    
    temp_df = table_to_df('temp')
    data_count = len(temp_df['avg_temp']) - 1
    if data_count != -1:
        last_avg_temp = temp_df['avg_temp'][data_count]
    else:
        last_avg_temp = 0
    with col1:
        col1.header("Температура")
        col1.write("Последняя средняя температура: " + str(last_avg_temp))
        if not fork_state:
            if not hand:
                col1.write("Текущее значение параметра T: " + str(T))
                if last_avg_temp <= T:
                    btn1 = col1.button('Открыть форточку', disabled = True)
                else:
                    btn1 = col1.button('Открыть форточку')
            else:
                btn1 = col1.button('Открыть форточку')
            if btn1:
                fork(1)
                data['airing'] = 1
                with open("properties.json", 'w') as write_file:
                    json.dump(data, write_file)
                st.experimental_rerun()
        else:
            btn1 = col1.button('Закрыть форточку')
            if btn1:
                fork(0)
                data['airing'] = 0
                with open("properties.json", 'w') as write_file:
                    json.dump(data, write_file)
                st.experimental_rerun()
        col1.dataframe(data = temp_df, use_container_width = True)
        col1.write("График средней температуры")
        col1.line_chart(data = temp_df, x = 'time', y = 'avg_temp')
        col1.write("Графики с каждого датчика температуры (1-4)")
        col1.line_chart(data = temp_df, x = 'time', y = 'temp_1')
        col1.line_chart(data = temp_df, x = 'time', y = 'temp_2')
        col1.line_chart(data = temp_df, x = 'time', y = 'temp_3')
        col1.line_chart(data = temp_df, x = 'time', y = 'temp_4')
        
    hum_df = table_to_df('hum')
    data_count = len(hum_df['avg_hum']) - 1
    if data_count != -1:
        last_avg_hum = hum_df['avg_hum'][data_count]
    else:
        last_avg_hum = 0
    with col2:
        col2.header("Влажность")
        col2.write("Последняя средняя влажность: " + str(last_avg_hum))
        if not hum_state:
            if not hand:
                col2.write("Текущее значение параметра H: " + str(H))
                if last_avg_hum > H:
                    btn2 = col2.button("Запустить увлaжнитель", disabled = True)
                else:
                    btn2 = col2.button("Запустить увлaжнитель")
            else:
                btn2 = col2.button("Запустить увлaжнитель")
            if btn2:
                total_hum(1)
                data['humidification'] = 1
                with open("properties.json", 'w') as write_file:
                    json.dump(data, write_file)
                st.experimental_rerun()
            
        else:
            btn2 = col2.button("Выключить увлажнитель")
            if btn2:
                total_hum(0)
                data['humidification'] = 0
                with open("properties.json", 'w') as write_file:
                    json.dump(data, write_file)
                st.experimental_rerun()
        col2.dataframe(data = hum_df, use_container_width = True)
        col2.write("График средней влажности")
        col2.line_chart(data = hum_df, x = 'time', y = 'avg_hum')
        col2.write("Графики с каждого датчика влажности (1-4)")
        col2.line_chart(data = hum_df, x = 'time', y = 'hum_1')
        col2.line_chart(data = hum_df, x = 'time', y = 'hum_2')
        col2.line_chart(data = hum_df, x = 'time', y = 'hum_3')
        col2.line_chart(data = hum_df, x = 'time', y = 'hum_4')
    with open("properties.json", 'w') as write_file:
        json.dump(data, write_file)
main()