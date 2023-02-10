from main import table_to_df, session, data_update, watering
import streamlit as st
import json

def main():
    st.set_page_config(
        page_title="Soil",
        layout="wide"
    )
    st.title("Данные с датчиков влажности почвы")
    with open("properties.json", "r") as read_file:
        data = json.load(read_file)
    hand = data['hand']
    Hb = data['Hb']
    if hand:
        st.subheader("Включен ручной режим управления")
    
    last_soils = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        name = "soil_"
        data_count = len(table_to_df('soil')[name + str(i + 1)]) - 1
        if data_count != -1:
            last_soils[i] = table_to_df('soil')[name + str(i + 1)][data_count]
        else:
            last_soils[i] = 0
            
    placeholder = st.empty()
    with placeholder.container():
        col1, col2 = st.columns(2)
        soil_df = table_to_df('soil')
        with col1:
            col1.subheader("Влажность почвы")
            col1.dataframe(soil_df)
            col1.line_chart(data = soil_df, x = 'time', y = 'soil_1')
            col1.line_chart(data = soil_df, x = 'time', y = 'soil_2')
            col1.line_chart(data = soil_df, x = 'time', y = 'soil_3')
            col1.line_chart(data = soil_df, x = 'time', y = 'soil_4')
            col1.line_chart(data = soil_df, x = 'time', y = 'soil_5')
            col1.line_chart(data = soil_df, x = 'time', y = 'soil_6')
        with col2:
            col2.subheader("Полив почвы")
            col2.write("Текущее значение параметра Hb: " + str(Hb))
            col2.write("Последняя влажность бороздки #1: " + str(last_soils[0]))
            if not data['soil_1']:
                if (last_soils[0] < Hb) or hand:
                    btn1 = col2.button('Полив бороздки №1', disabled = False)
                else:
                    btn1 = col2.button('Полив бороздки №1', disabled = True)
                if btn1:
                    watering(1, 1)
                    data['soil_1'] = 1
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()
            else:
                btn1 = col2.button('Выключить полив бороздки №1')
                if btn1:
                    watering(1, 0)
                    data['soil_1'] = 0
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()

            col2.write("Последняя влажность бороздки #2: " + str(last_soils[1]))
            if not data['soil_2']:
                if (last_soils[1] < Hb) or hand:
                    btn2 = col2.button('Полив бороздки №2', disabled = False)
                else:
                    btn2 = col2.button('Полив бороздки №2', disabled = True)
                if btn2:
                    watering(2, 1)
                    data['soil_2'] = 1
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()
            else:
                btn2 = col2.button('Выключить полив бороздки №2')
                if btn2:
                    watering(2, 0)
                    data['soil_2'] = 0
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()

            col2.write("Последняя влажность бороздки #3: " + str(last_soils[2]))
            if not data['soil_3']:
                if (last_soils[2] < Hb) or hand:
                    btn3 = col2.button('Полив бороздки №3', disabled = False)
                else:
                    btn3 = col2.button('Полив бороздки №3', disabled = True)
                if btn3:
                    watering(3, 1)
                    data['soil_3'] = 1
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()
            else:
                btn3 = col2.button('Выключить полив бороздки №3')
                if btn3:
                    watering(3, 0)
                    data['soil_3'] = 0
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()

            col2.write("Последняя влажность бороздки #4: " + str(last_soils[3]))
            if not data['soil_4']:
                if (last_soils[3] < Hb) or hand:
                    btn4 = col2.button('Полив бороздки №4', disabled = False)
                else:
                    btn4 = col2.button('Полив бороздки №4', disabled = True)
                if btn4:
                    watering(4, 1)
                    data['soil_4'] = 1
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()
            else:
                btn4 = col2.button('Выключить полив бороздки №4')
                if btn4:
                    watering(4, 0)
                    data['soil_4'] = 0
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()

            col2.write("Последняя влажность бороздки #5: " + str(last_soils[4]))
            if not data['soil_5']:
                if (last_soils[4] < Hb) or hand:
                    btn5 = col2.button('Полив бороздки №5', disabled = False)
                else:
                    btn5 = col2.button('Полив бороздки №5', disabled = True)
                if btn5:
                    watering(5, 1)
                    data['soil_5'] = 1
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()
            else:
                btn5 = col2.button('Выключить полив бороздки №5')
                if btn5:
                    watering(5, 0)
                    data['soil_5'] = 0
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()

            col2.write("Последняя влажность бороздки #6: " + str(last_soils[5]))
            if not data['soil_6']:
                if (last_soils[5] < Hb) or hand:
                    btn6 = col2.button('Полив бороздки №6', disabled = False)
                else:
                    btn6 = col2.button('Полив бороздки №6', disabled = True)
                if btn6:
                    watering(6, 1)
                    data['soil_6'] = 1
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()
            else:
                btn6 = col2.button('Выключить полив бороздки №6')
                if btn6:
                    watering(6, 0)
                    data['soil_6'] = 0
                    with open("properties.json", 'w') as write_file:
                        json.dump(data, write_file)
                    st.experimental_rerun()

        with open("properties.json", 'w') as write_file:
                    json.dump(data, write_file)
                
        
        
main()