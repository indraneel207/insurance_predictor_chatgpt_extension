"""
This module contains a Flask application that serves as an API for a Test App.

The API provides two endpoints:
- "/" (root): Returns a welcome message when accessed with a GET request, and accepts a JSON payload when accessed with a POST request.
- "/getPredictionOutput": Accepts a JSON payload and returns a prediction output.

The Flask application is configured to allow cross-origin resource sharing (CORS).

Author: [Indraneel Vairagare]
"""

import os
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import prediction

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)


class Test(Resource):
    """
    Represents the root endpoint of the API.

    GET request: Returns a welcome message.
    POST request: Accepts a JSON payload and returns the payload as a response.

    Methods:
    - get(): Returns a welcome message.
    - post(): Accepts a JSON payload and returns the payload as a response.
    """

    def get(self):
        """
        Handles GET requests to the root endpoint.

        Returns:
        - str: Welcome message.
        """
        return "Welcome to the Test App API!"

    def post(self):
        """
        Handles POST requests to the root endpoint.

        Returns:
        - dict: JSON payload as a response.
        - dict: Error message if the payload is in an invalid format.
        """
        try:
            value = request.get_json()
            if value:
                return {"Post Values": value}, 201

            return {"error": "Invalid format."}

        except Exception as error:
            return {"error": error}


class GetPredictionOutput(Resource):
    """
    Represents the "/getPredictionOutput" endpoint of the API.

    GET request: Returns an error message.
    POST request: Accepts a JSON payload, performs a prediction, and returns the prediction output.

    Methods:
    - get(): Returns an error message.
    - post(): Accepts a JSON payload, performs a prediction, and returns the prediction output.
    """

    def get(self):
        """
        Handles GET requests to the "/getPredictionOutput" endpoint.

        Returns:
        - dict: Error message.
        """
        return {"error": "Invalid Method."}

    def post(self):
        """
        Handles POST requests to the "/getPredictionOutput" endpoint.

        Returns:
        - dict: Prediction output.
        - dict: Error message if an exception occurs during prediction.
        """
        try:
            data = request.get_json()
            predict = prediction.predict_insurance_premium(data)
            predict_output = predict
            return {"predict": predict_output}

        except Exception as error:
            return {"error": error}


api.add_resource(Test, "/")
api.add_resource(GetPredictionOutput, "/getInsurancePremiumPrediction")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
