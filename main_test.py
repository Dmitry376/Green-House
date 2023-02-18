import sqlite3 as sl
import requests
import json
import datetime
import pandas as pd
import streamlit as st
import pytest

# Import the functions we want to test
from main import session, stop_session, data_update, fork, watering, total_hum, table_to_df


# Test the session function
def test_session():
    con = session()
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    assert "temp" in table_names
    assert "hum" in table_names
    assert "soil" in table_names
    con.close()


# Test the stop_session function
def test_stop_session():
    con = session()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM temp")
    temp_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM hum")
    hum_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM soil")
    soil_count = cursor.fetchone()[0]
    assert temp_count >= 0
    assert hum_count >= 0
    assert soil_count >= 0
    stop_session()
    cursor.execute("SELECT COUNT(*) FROM temp")
    temp_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM hum")
    hum_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM soil")
    soil_count = cursor.fetchone()[0]
    assert temp_count == 0
    assert hum_count == 0
    assert soil_count == 0
    con.close()


# Test the data_update function
def test_data_update():
    con = session()
    temp, hum, soil = data_update()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM temp ORDER BY time DESC LIMIT 1")
    last_temp = cursor.fetchone()
    cursor.execute("SELECT * FROM hum ORDER BY time DESC LIMIT 1")
    last_hum = cursor.fetchone()
    cursor.execute("SELECT * FROM soil ORDER BY time DESC LIMIT 1")
    last_soil = cursor.fetchone()
    assert last_temp[2] == temp[0]
    assert last_temp[3] == temp[1]
    assert last_temp[4] == temp[2]
    assert last_temp[5] == temp[3]
    assert last_hum[2] == hum[0]
    assert last_hum[3] == hum[1]
    assert last_hum[4] == hum[2]
    assert last_hum[5] == hum[3]
    assert last_soil[2] == soil[0]
    assert last_soil[3] == soil[1]
    assert last_soil[4] == soil[2]
    assert last_soil[5] == soil[3]
    assert last_soil[6] == soil[4]
    assert last_soil[7] == soil[5]
    stop_session()
    con.close()


# Test the fork function
def test_fork():
    response = fork(1)
    assert response == 200
    response = fork(0)
    assert response == 200
    response = fork(2)
    assert response == 404
    
def test_watering():
    assert watering(1, 1) == 200
    assert watering(1, 0) == 200
    assert watering(6, 1) == 200
    assert watering(6, 0) == 200
    assert watering(1, 2) == 404
    assert watering(7, 1) == 404
    assert watering(7, 0) == 404
    
def test_total_hum():
    response = total_hum(1)
    assert response == 200
    response = total_hum(0)
    assert response == 200
    response = total_hum(2)
    assert response == 404
    
@pytest.fixture(scope="session")
def test_db():
    conn = sl.connect(":memory:")
    c = conn.cursor()
    c.execute("""CREATE TABLE test_table
              (id INT PRIMARY KEY, name TEXT, value REAL)""")
    c.execute("INSERT INTO test_table VALUES (1, 'foo', 0.5)")
    c.execute("INSERT INTO test_table VALUES (2, 'bar', 1.2)")
    conn.commit()
    yield conn
    conn.close()
