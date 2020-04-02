"""API COVID-19."""
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class DailyData(Resource):
    """Daily data.

    /api/dailydata
    """

    def get(self):
        """GET method."""
        return {'message': 'OK'}, 200


api.add_resource(DailyData, '/api/dailydata')

if __name__ == '__main__':
    app.run(debug=True)
