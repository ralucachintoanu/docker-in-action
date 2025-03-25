"""Main entry point for the API service."""

import os
from flasgger import Swagger
from flask import Flask, request, jsonify, redirect
from pymongo import MongoClient
from bson import ObjectId


def create_app(mock_collection=None):
    """
    Create a Flask app with Swagger documentation
    """
    app = Flask(__name__)
    Swagger(app)

    if mock_collection:
        collection = mock_collection
    else:
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        db = client[os.getenv("MONGO_DB_NAME", "test")]
        collection = db[os.getenv("MONGO_COLLECTION_NAME", "trips")]

    @app.route("/", methods=["GET"])
    def home():
        """
        Redirect to API documentation
        """
        return redirect("/apidocs")

    @app.route("/trips/<trip_id>", methods=["GET"])
    def get_trip(trip_id):
        """
        Get trip details by ID
        ---
        parameters:
          - name: trip_id
            in: path
            required: true
            schema:
              type: string
        responses:
          200:
            description: Trip details retrieved successfully
          404:
            description: Trip not found
        """
        trip = collection.find_one({"_id": ObjectId(trip_id)})
        if trip:
            trip["_id"] = str(trip["_id"])
            return jsonify(trip)
        return jsonify({"error": "Trip not found"}), 404

    @app.route("/trips/top-longest", methods=["GET"])
    def get_top_longest_trips():
        """
        Get Top N Longest Trips by Distance
        ---
        parameters:
          - name: limit
            in: query
            schema:
              type: integer
            required: false
            description: Number of trips to return (default is 5)
        responses:
          200:
            description: List of top N longest trips
        """
        limit = int(request.args.get("limit", 5))
        trips = list(collection.find().sort("trip_distance", -1).limit(limit))
        for trip in trips:
            trip["_id"] = str(trip["_id"])
        return jsonify(trips)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
