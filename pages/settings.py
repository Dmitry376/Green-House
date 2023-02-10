from main import table_to_df, session, data_update
import streamlit as st
import json

def main():
    with open("properties.json", "r") as read_file:
        data = json.load(read_file)
    T = data['T']
    H = data['H']
    Hb = data['Hb']
    hand = data['hand']
    time = data['time']
    st.set_page_config(
        page_title="Settings",
        layout="wide"
    )
    st.title("Настройки")
    data['time'] = st.number_input("Введите частоту обновления данных **в секундах**", value = time, step = 1)
    data['T'] = st.number_input("Введите значение параметра T", value = T, step = 0.5)
    data['H'] = st.number_input("Введите значение параметра H", value = H, step = 0.5)
    data['Hb'] = st.number_input("Введите значение параметра Hb", value = Hb, step = 0.5)
    if not hand:
        btn = st.button("Включить ручное управление")
        if btn:
            hand = 1
            data["hand"] = 1
            with open("properties.json", "w") as write_file:
                json.dump(data, write_file)
            st.experimental_rerun()
    else:
        btn2 = st.button("Выключить ручное управление", type = 'primary')
        if btn2:
            hand = 0
            data["hand"] = 0
            with open("properties.json", "w") as write_file:
                json.dump(data, write_file)
            st.experimental_rerun()
            
    with open("properties.json", "w") as write_file:
        json.dump(data, write_file)
    
main()