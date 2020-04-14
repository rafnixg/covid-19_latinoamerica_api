"""ETL."""
import pandas as pd
import io
import requests
import os
from datetime import date, timedelta, datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

_logger = logging.getLogger(__name__)

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=60)
def etl():
    """ETL."""
    file_date = date(2020, 2, 25)
    dates = []

    while file_date <= date.today():
        dates.append(file_date)
        file_date += timedelta(days=1)

    files = []
    try:
        os.stat('data')
    except:
        os.mkdir('data')

    for file in dates:
        file = file.strftime("%Y-%m-%d")
        print(file)
        url = r"https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/daily_reports/{date}.csv".format(date=file)
        raw_string = requests.get(url).content
        if b'404: Not Found\n' not in raw_string:
            try:
                df = pd.read_csv(io.StringIO(raw_string.decode('utf-8')))
                df.to_csv('data/{}.csv'.format(file), index=False)
                df.rename(columns={'Last Update': 'Date'}, inplace=True)
                df['Date'] = pd.to_datetime(file)
                df = df.fillna(0).replace({'missing': 0})
                df['Confirmed'] = df['Confirmed'].astype(int)
                df['Deaths'] = df['Deaths'].astype(int)
                df['Recovered'] = pd.to_numeric(df['Recovered']).astype(int)
                files.append(df)
            except:
                _logger.warning(f'Error in file format {file}.csv')
        else:
            _logger.warning(f'File {file} Not Found')

    df = pd.concat(files, axis=0, ignore_index=True, sort=False)

    _logger.info(f'Updating data')
    print("[INFO] Updating data")
    data.to_csv('data.csv', index=False)
    _logger.info(f'Data has been updated on {datetime.now}')
    print(f"[INFO] Data has been updated on {datetime.now}.")

sched.start()
