import os
import psycopg2
import atexit

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
# /!\ IMPORTANT /!\ : Shut down the db connection when exiting the app
atexit.register(lambda: conn.close())


def save_unprocessed_data(date, json_data):
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


def load_station_delay_dates():
    cursor = conn.cursor()
    cursor.execute('select date from public."t_station_delay" group by date;')
    result = cursor.fetchall()
    cursor.close()
    return result


def load_traintyp_delay_dates():
    cursor = conn.cursor()
    cursor.execute('select date from public."t_traintyp_delay" group by date;')
    result = cursor.fetchall()
    cursor.close()
    return result


def save_station_delay(date, station_name, delay_count, delay_sum, total_data_points):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO public.t_station_delay(date, "stationName", "delayCount", "delaySum", "totalDataPoints")'
        'VALUES ( %s, %s, %s, %s, %s)',
        (date, station_name, delay_count, delay_sum, total_data_points))
    conn.commit()
    cursor.close()


def save_traintyp_delay(date, traintyp_name, delay_count, delay_sum, total_data_points):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO public.t_traintyp_delay(date, "trainTypName", "delayCount", "delaySum", "totalDataPoints")'
        'VALUES ( %s, %s, %s, %s, %s)',
        (date, traintyp_name, delay_count, delay_sum, total_data_points))
    conn.commit()
    cursor.close()
