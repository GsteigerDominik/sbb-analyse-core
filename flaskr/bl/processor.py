import json
from datetime import datetime, timedelta

from flaskr.db import dbAccess
from flaskr.log import logger, slack


def run_initial():
    logger.log_info("Starting initial Processing")
    to_process = dbAccess.load_unprocessed_dates()
    processed_station = dbAccess.load_station_delay_dates()
    processed_traintype = dbAccess.load_traintype_delay_dates()
    for date in to_process:
        if date not in processed_station:
            process_station_delay(date[0].strftime('%Y-%m-%d'))
        if date not in processed_traintype:
            process_traintype_delay(date[0].strftime('%Y-%m-%d'))
    logger.log_info("Finished initial Processing")


def run_process_job():
    logger.log_info("ProcessJob: Status changed to started")
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime('%Y-%m-%d')
    process_station_delay(formatted_date)
    process_traintype_delay(formatted_date)
    slack.post_job_finished_msg(formatted_date, 'Processed')
    logger.log_info("PollJob: Status changed to finished")


def process_station_delay(date):
    logger.log_info("Started processing of station delays from " + date)
    stations_dict = {}
    result = dbAccess.load_unprocessed_data(date)
    for row in result:
        if 'records' in row[2]:
            data_set = row[2]['records']
            for data_point in data_set:
                stationname = data_point['record']['fields']['haltestellen_name']
                process_data_point(stationname, stations_dict, data_point, True)
        else:
            logger.log_warn('No records key in record')
    dbAccess.save_station_delay(date, json.dumps(stations_dict))
    logger.log_info("Finished processing of station delays from " + date)


def process_traintype_delay(date):
    logger.log_info("Started processing of train types delays from " + date)
    traintype_dict = {}
    result = dbAccess.load_unprocessed_data(date)
    for row in result:
        if 'records' in row[2]:
            data_set = row[2]['records']
            for data_point in data_set:
                traintype = data_point['record']['fields']['verkehrsmittel_text']
                process_data_point(traintype, traintype_dict, data_point, False)
        else:
            logger.log_warn('No records key in record')
    dbAccess.save_traintype_delay(date, json.dumps(traintype_dict))
    logger.log_info("Finished processing of train types delays from " + date)


def process_data_point(key, dictionary, data_point, save_geopos):
    if key not in dictionary:
        dictionary[key] = {'delaycount': 0, 'delaysum': 0, 'totaldatapoints': 0}
        if save_geopos and data_point['record']['fields']['geopos'] is not None:
            dictionary[key]['geopos_lat'] = data_point['record']['fields']['geopos']['lat']
            dictionary[key]['geopos_lon'] = data_point['record']['fields']['geopos']['lon']
    if data_point['record']['fields']['ankunftsverspatung'] == 'true':
        dictionary[key]['delaycount'] += 1
        actual = datetime.fromisoformat(data_point['record']['fields']['an_prognose'])
        planed = datetime.fromisoformat(data_point['record']['fields']['ankunftszeit'])
        dictionary[key]['delaysum'] += int((actual - planed).total_seconds() / 60)
    dictionary[key]['totaldatapoints'] += 1
