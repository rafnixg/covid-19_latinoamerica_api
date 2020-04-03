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


if __name__ == '__main__':
    app.run(debug=True)
