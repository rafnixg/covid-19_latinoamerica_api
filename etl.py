"""ETL."""
import pandas as pd
import io
import requests
import os
from datetime import date, timedelta


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
        url = r"https://raw.githubusercontent.com/DataScienceResearchPeru/covid-19_latinoamerica/master/latam_covid_19_data/latam_covid_19_daily_reports/{date}.csv".format(date=file)
        raw_string = requests.get(url).content
        df = pd.read_csv(io.StringIO(raw_string.decode('utf-8')))
        if b'404: Not Found\n' not in raw_string:
            df.to_csv('data/{}.csv'.format(file), index=False)
        df.rename(columns={'Last Update': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(file)
        files.append(df)
    df = pd.concat(files, axis=0, ignore_index=True, sort=False)

    return df


if __name__ == '__main__':
    data = etl()
    data.to_csv('data.csv', index=False)
