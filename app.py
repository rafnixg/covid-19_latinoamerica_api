"""API COVID-19."""
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from flask_restplus import Resource, Api, fields
import pandas as pd
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import sys
from etl import etl

sys.path.append("./")

# Function to fetch data from csv repository
def updateData():
    """Function to update dataset."""
    print("[INFO] Updating data")
    data = etl()
    data.to_csv('data.csv', index=False)
    print(f"[INFO] Data has been updated on {datetime.now}.")


# and update data every hour
sched = BackgroundScheduler(daemon=True)
sched.add_job(updateData, 'interval', minutes=60)
sched.start()

# Start webservice
app = Flask(__name__)
CORS(app)
api = Api(app,
          version="COVID19 Latin America API",
          description="API para extraer casos de COVID19 por pais en Latinoamerica")


@api.route('/data')
class GetAllData(Resource):
    """Get all data."""

    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        out = df.to_dict(orient='records')
        return out


@api.route('/pais/<id>')
class GetDataByCountry(Resource):
    """Get data by country."""

    def get(self, id):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df[df["Country/Region"] == str(id).capitalize()]
        out = df_tmp.to_dict(orient='records')
        return out

@api.route('/paises-disponibles')
class GetCountries(Resource):
    """Countries in database."""
    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df["Country/Region"].unique()
        out = dict(enumerate(df_tmp, 1))
        return out

@api.route('/resumen-por-pais')
class GetCountrySummary(Resource):
    """Summary by country."""
    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df.groupby(by="Country/Region").sum()
        df_tmp.reset_index(inplace=True)
        out = df_tmp.to_dict(orient='records')
        return out

@api.route('/resumen-pais-provincia')
class GetDataByCountryRegion(Resource):
    def get(self):
        df = pd.read_csv('data.csv')
        df_tmp = df.groupby(by=["Country/Region","Province/State"]).sum()
        df_tmp.reset_index(inplace=True)
        print(df_tmp)
        out = df_tmp.to_dict(orient='records')
        return out

@api.route('/ultima-actualizacion')
class GetLastUpdateDate(Resource):
    def get(self):
        df = pd.read_csv('data.csv')
        countries=[]
        lastUpdateOn=[]
        for country in df["Country/Region"].unique():
            df_tmp = df[(df["Country/Region"]==country) & (df["Confirmed"]>0)]
            print(df_tmp[df_tmp.Date == df_tmp["Date"].max()])
            lastUpdateOn.append(df_tmp["Date"].max())
            countries.append(country)
        df_out = pd.DataFrame({"Country/Region":countries, "Ultima Actualization": lastUpdateOn})
        out = df_out.to_dict(orient='records')
        return out


if __name__ == '__main__':
    app.run(debug=True)
