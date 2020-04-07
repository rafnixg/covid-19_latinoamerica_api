"""API COVID-19."""
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from flask_restplus import Resource, Api, fields
import pandas as pd
import numpy as np
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


# Initialize data
updateData()


# Start webservice
app = Flask(__name__)
CORS(app)
api = Api(app,
          version="COVID19 Latin America API",
          description="API para extraer casos de COVID19 por país en Latinoamérica")


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
        df_tmp = df[df["Country"] == str(id).capitalize()]
        out = df_tmp.to_dict(orient='records')
        return out


@api.route('/paises-disponibles')
class GetCountries(Resource):
    """Countries in database."""

    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df["Country"].unique()
        out = dict(enumerate(df_tmp, 1))
        return out


@api.route('/resumen-por-pais')
class GetCountrySummary(Resource):
    """Summary by country."""

    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df.groupby(by="Country").sum()
        df_tmp.reset_index(inplace=True)
        out = df_tmp.to_dict(orient='records')
        return out


@api.route('/resumen-pais-provincia')
class GetDataByCountryRegion(Resource):
    """Summary by country and region."""

    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df.groupby(by=["Country", "Subdivision"]).sum()
        df_tmp.reset_index(inplace=True)
        print(df_tmp)
        out = df_tmp.to_dict(orient='records')
        return out


@api.route('/ultima-actualizacion')
class GetLastUpdateDate(Resource):
    """Last update."""

    def get(self):
        """GET method."""
        df = pd.read_csv('data.csv')
        df_tmp = df[df["Confirmed"] > 0]
        df_tmp = df_tmp[["Country", "Date"]]
        df_tmp["Date"] = pd.to_datetime(df_tmp["Date"], format="%Y-%m-%d")
        df_tmp = df_tmp.loc[df_tmp.groupby('Country')['Date'].idxmax()]
        df_tmp.drop_duplicates(inplace=True)
        df_tmp["Last Update"] = df_tmp["Date"].astype(str)
        df_tmp = df_tmp[["Country", "Last Update"]]
        out = df_tmp.to_dict(orient='records')
        return out


@api.route('/forzar-actualization')
class ForceUpdate(Resource):
    """Force Update."""

    def get(self):
        """GET method."""
        updateData()
        return {'Actualization': str(datetime.now())}


if __name__ == '__main__':
    app.run(debug=True)
