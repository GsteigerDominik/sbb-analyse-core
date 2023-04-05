import atexit
import os

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
# /!\ IMPORTANT /!\ : Shut down the db connection when exiting the app
atexit.register(lambda: conn.close())


def save_unprocessed(date, json_data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO public."t_unprocessed" (date, data) VALUES (%s, %s)',
                   (date, json_data))
    conn.commit()
    cursor.close()


def load_unprocessed_data(date):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM public."t_unprocessed" where date=%s', (date,))
    result = cursor.fetchall()
    cursor.close()
    return result


def load_unprocessed_dates():
    cursor = conn.cursor()
    cursor.execute('select date from public."t_unprocessed" group by date;')
    result = cursor.fetchall()
    cursor.close()
    return result


def load_station_delay_all():
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM public."t_station_delay"')
    result = cursor.fetchall()
    cursor.close()
    return result


def load_station_delay_by_date(date):
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM public."t_station_delay" where date=%s', (date,))
    result = cursor.fetchall()
    cursor.close()
    return result


def load_station_delay_dates():
    cursor = conn.cursor()
    cursor.execute('select date from public."t_station_delay" group by date;')
    result = cursor.fetchall()
    cursor.close()
    return result


def load_traintype_delay_all():
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM public."t_traintype_delay"')
    result = cursor.fetchall()
    cursor.close()
    return result


def load_traintype_delay_by_date(date):
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM public."t_traintype_delay" where date=%s', (date,))
    result = cursor.fetchall()[0][0]
    cursor.close()
    return result


def load_traintype_delay_dates():
    cursor = conn.cursor()
    cursor.execute('select date from public."t_traintype_delay" group by date;')
    result = cursor.fetchall()
    cursor.close()
    return result


def save_station_delay(date, json_data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO public."t_station_delay" (date, data) VALUES (%s, %s)',
                   (date, json_data))
    conn.commit()
    cursor.close()


def save_traintype_delay(date, json_data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO public."t_traintype_delay" (date, data) VALUES (%s, %s)',
                   (date, json_data))
    conn.commit()
    cursor.close()
