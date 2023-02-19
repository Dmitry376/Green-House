# Это скрипт на Python, который определяет функцию main() для управления настройками системы, и он использует библиотеку Streamlit для пользовательского интерфейса. 
# Код считывает данные конфигурации из файла JSON под названием "properties.json" и сохраняет обновленные данные конфигурации в тот же файл.

# Импорт необходимых библиотек
from main import table_to_df, session, data_update
import streamlit as st
import json

# Определение основной функции
def main():
    # Открываем конфигурационный файл "properties.json" и загружаем данные с помощью библиотеки JSON. 
    # Значения параметров конфигурации хранятся в отдельных переменных для облегчения доступа к ним позже в коде.
    with open("properties.json", "r") as read_file:
        data = json.load(read_file)
    T = data['T']
    H = data['H']
    Hb = data['Hb']
    hand = data['hand']
    time = data['time']
    fork_state = data['airing']
    hum_state = data['humidification']
    s1 = data['soil_1']
    s2 = data['soil_2']
    s3 = data['soil_3']
    s4 = data['soil_4']
    s5 = data['soil_5']
    s6 = data['soil_6']
    # Настройка конфигурации страницы для приложения Streamlit и отображение заголовка страницы настроек.
    st.set_page_config(
        page_title="Settings",
        layout="wide"
    )
    st.title("Настройки")
    # Создание числовых полей ввода для каждого из параметров конфигурации и соответствующее обновление значений в словаре данных.
    data['time'] = st.number_input("Введите частоту обновления данных **в секундах**", value = time, step = 1)
    data['T'] = st.number_input("Введите значение параметра T", value = T, step = 0.5)
    data['H'] = st.number_input("Введите значение параметра H", value = H, step = 0.5)
    data['Hb'] = st.number_input("Введите значение параметра Hb", value = Hb, step = 0.5)
    # Отображение кнопки для включения или отключения ручного управления. Если ручное управление отключено, 
    # отображается кнопка "Включить ручное управление", а если оно включено, отображается кнопка "Выключить ручное управление". 
    # Когда пользователь нажимает одну из кнопок, значение переменной hand обновляется, и словарь данных записывается обратно в файл конфигурации. 
    # st.experimental_rerun() используется для перезагрузки приложения Streamlit с обновленной конфигурацией.
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
     
    st.subheader("Текущее состояние устройств (1 - включено/открыто, 0 - выключено/закрыто): ")
    st.text("Форточка: " + str(fork_state))
    st.text("Общий увлажнитель: " + str(hum_state))
    st.text("Полив бороздки №1: " + str(s1))
    st.text("Полив бороздки №2: " + str(s2))
    st.text("Полив бороздки №3: " + str(s3))
    st.text("Полив бороздки №4: " + str(s4))
    st.text("Полив бороздки №5: " + str(s5))
    st.text("Полив бороздки №6: " + str(s6))
    # Сохранение обновленных конфигурационных данных в файл "properties.json".
    with open("properties.json", "w") as write_file:
        json.dump(data, write_file)

# Вызов функции main() для запуска программы.
main()
