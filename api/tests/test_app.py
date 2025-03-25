"""Tests for the API app."""

# pylint: disable=missing-function-docstring,redefined-outer-name

import pytest
from bson import ObjectId
from api.app import create_app


@pytest.fixture
def client(mocker):
    mock_collection = mocker.MagicMock()
    app = create_app(mock_collection=mock_collection)
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client, mock_collection


def test_home_redirects_to_apidocs(client):
    test_client, _ = client
    response = test_client.get("/")
    assert response.status_code == 302
    assert "/apidocs" in response.headers["Location"]


def test_get_trip_found(client):
    test_client, mock_collection = client
    fake_trip = {"_id": ObjectId("507f1f77bcf86cd799439011"), "trip_distance": 12.5}
    mock_collection.find_one.return_value = fake_trip

    response = test_client.get("/trips/507f1f77bcf86cd799439011")
    assert response.status_code == 200
    assert response.json["_id"] == "507f1f77bcf86cd799439011"


def test_get_trip_not_found(client):
    test_client, mock_collection = client
    mock_collection.find_one.return_value = None

    response = test_client.get("/trips/507f1f77bcf86cd799439011")
    assert response.status_code == 404
    assert response.json == {"error": "Trip not found"}


def test_get_top_longest_trips(client, mocker):
    test_client, mock_collection = client

    mock_cursor = mocker.MagicMock()
    mock_cursor.sort.return_value.limit.return_value = [
        {"_id": ObjectId("507f1f77bcf86cd799439011"), "trip_distance": 10.1},
        {"_id": ObjectId("507f1f77bcf86cd799439012"), "trip_distance": 9.9},
    ]

    mock_collection.find.return_value = mock_cursor

    response = test_client.get("/trips/top-longest?limit=2")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["trip_distance"] == 10.1
    assert data[1]["_id"] == "507f1f77bcf86cd799439012"
