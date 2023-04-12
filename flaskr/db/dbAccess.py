import atexit
import os

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL_PROD']
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
    result = load_all_with_paging('t_station_delay')
    return sum_delay_data(result)


def load_station_delay_by_date(date):
    cursor = conn.cursor()
    cursor.execute('SELECT date, data FROM public."t_station_delay" where date=%s', (date,))
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
    result = load_all_with_paging("t_traintype_delay")
    return sum_delay_data(result)


def load_traintype_delay_by_date(date):
    cursor = conn.cursor()
    cursor.execute('SELECT date, data FROM public."t_traintype_delay" where date=%s', (date,))
    result = cursor.fetchall()
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


def sum_delay_data(result):
    summed_delays = {}
    for day in result:
        for key in day[0]:
            if key not in summed_delays:
                summed_delays[key] = {'delaycount': 0, 'delaysum': 0, 'totaldatapoints': 0}
            summed_delays[key]['delaycount'] += day[0][key]['delaycount']
            summed_delays[key]['delaysum'] += day[0][key]['delaysum']
            summed_delays[key]['totaldatapoints'] += day[0][key]['totaldatapoints']
    return summed_delays


def load_all_with_paging(table, page_size=5):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM public."' + table + '"')
    count = cursor.fetchone()[0]
    pages = (count // page_size) + (count % page_size > 0)
    result = []
    for page in range(pages):
        offset = page * page_size
        cursor.execute('SELECT data FROM public."' + table + '" ORDER BY id OFFSET %s LIMIT %s',
                       (offset, page_size))
    page_result = cursor.fetchall()
    result += page_result
    cursor.close()
    return result
