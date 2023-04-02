from datetime import datetime

from flaskr.db import dbAccess
from flaskr.log import logger

def run_process_job():
    process_station_delay('2023-03-28')
    process_station_delay('2023-03-29')
    process_station_delay('2023-03-30')
    process_station_delay('2023-03-31')
    process_station_delay('2023-04-01')

def process_station_delay(date):
    logger.log_info("Started processing of station delays from " + date)
    stations_dict = {}
    result = dbAccess.load_unprocessed_data(date)
    for row in result:
        if 'records' in row[2]:
            data_set = row[2]['records']
            for data_point in data_set:
                stationname = data_point['record']['fields']['haltestellen_name']
                if stationname not in stations_dict:
                    stations_dict[stationname] = {'delaycount': 0, 'delaysum': 0, 'totaldatapoints': 0}
                if data_point['record']['fields']['ankunftsverspatung'] == 'true':
                    stations_dict[stationname]['delaycount'] += 1
                    actual = datetime.fromisoformat(data_point['record']['fields']['an_prognose'])
                    planed = datetime.fromisoformat(data_point['record']['fields']['ankunftszeit'])
                    stations_dict[stationname]['delaysum'] = int((actual - planed).total_seconds() / 60)
                stations_dict[stationname]['totaldatapoints'] += 1
        else:
            logger.log_warn('No records key in record')
    for station in stations_dict:
        dbAccess.save_station_delay(date,
                                    station,
                                    stations_dict[station]['delaycount'],
                                    stations_dict[station]['delaysum'],
                                    stations_dict[station]['totaldatapoints'])
    logger.log_info("Finished processing of station delays from " + date)





