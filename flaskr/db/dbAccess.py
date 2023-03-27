import os
import psycopg2
import atexit

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: conn.close())


def saveUnprocessedData(date, json_data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO public."t_unprocessed" (date, data) VALUES (%s, %s)',
                   (date, json_data))
    conn.commit()
    cursor.close()
