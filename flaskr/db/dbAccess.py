import os
import psycopg2
from contextlib import contextmanager

DATABASE_URL = os.environ['DATABASE_URL']

@contextmanager
def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()


def save_unprocessed(date, json_data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO public."t_unprocessed" (date, data) VALUES (%s, %s)',
                       (date, json_data))
        conn.commit()
        cursor.close()


def load_unprocessed_data(date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."t_unprocessed" where date=%s', (date,))
        result = cursor.fetchall()
        cursor.close()
        return result


def load_unprocessed_dates():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('select date from public."t_unprocessed" group by date;')
        result = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return result


def load_station_delay_all():
    result = load_all_with_paging('t_station_delay', page_size=2)
    return sum_delay_data(result)


def load_station_delay_by_date(date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date, data FROM public."t_station_delay" where date=%s', (date,))
        result = cursor.fetchall()
        cursor.close()
        return result


def load_station_delay_dates():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('select date from public."t_station_delay" group by date;')
        result = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return result


def load_traintype_delay_all():
    result = load_all_with_paging("t_traintype_delay")
    return sum_delay_data(result)


def load_traintype_delay_by_date(date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date, data FROM public."t_traintype_delay" where date=%s', (date,))
        result = cursor.fetchall()
        cursor.close()
        return result


def load_traintype_delay_dates():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('select date from public."t_traintype_delay" group by date;')
        result = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return result


def save_station_delay(date, json_data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO public."t_station_delay" (date, data) VALUES (%s, %s)',
                       (date, json_data))
        conn.commit()
        cursor.close()


def save_traintype_delay(date, json_data):
    with get_connection() as conn:
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
                summed_delays[key] = {'delaycount': 0,
                                      'delaysum': 0,
                                      'totaldatapoints': 0}
                if 'geopos_lat' in day[0][key]:
                    summed_delays[key]['geopos_lat']=day[0][key]['geopos_lat']
                    summed_delays[key]['geopos_lon']=day[0][key]['geopos_lon']
            summed_delays[key]['delaycount'] += day[0][key]['delaycount']
            summed_delays[key]['delaysum'] += day[0][key]['delaysum']
            summed_delays[key]['totaldatapoints'] += day[0][key]['totaldatapoints']
    return summed_delays


def load_all_with_paging(table, page_size=5):
    with get_connection() as conn:
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
