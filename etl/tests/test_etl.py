"""Tests for the ETL app."""

# pylint: disable=missing-function-docstring,redefined-outer-name

import pandas as pd
import pytest
from etl.etl import _extract_data, _clean_data, _load_data


@pytest.fixture
def sample_csv(tmp_path):
    content = (
        "tpep_pickup_datetime,pickup_latitude,pickup_longitude,dropoff_latitude,"
        "dropoff_longitude,passenger_count,trip_distance,RatecodeID,payment_type,"
        "fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,"
        "total_amount,tpep_dropoff_datetime,store_and_fwd_flag\n"
        "2016-01-31 10:00:00,40.7,-73.9,40.8,-73.95,1,2.5,1,1,10,1,0.5,2,0,0.3,13.8,"
        "2016-01-31 10:15:00,Y\n"
    )
    file = tmp_path / "sample.csv"
    file.write_text(content)
    return str(file)


def test_extract_data_filters_by_date(sample_csv):
    df = _extract_data("2016-01-31", path=sample_csv)
    assert not df.empty
    assert (
        pd.to_datetime(df.iloc[0]["tpep_pickup_datetime"]).date()
        == pd.to_datetime("2016-01-31").date()
    )


def test_clean_data_filters_invalid_entries():
    df = pd.DataFrame(
        [
            {
                "tpep_pickup_datetime": "2016-01-31 10:00:00",
                "tpep_dropoff_datetime": "2016-01-31 10:10:00",
                "pickup_latitude": 40.7,
                "pickup_longitude": -73.9,
                "dropoff_latitude": 40.8,
                "dropoff_longitude": -73.95,
                "passenger_count": 1,
                "trip_distance": 2.0,
                "RatecodeID": 1,
                "payment_type": 1,
                "fare_amount": 10,
                "extra": 1,
                "mta_tax": 0.5,
                "tip_amount": 2,
                "tolls_amount": 0,
                "improvement_surcharge": 0.3,
                "total_amount": 13.8,
                "store_and_fwd_flag": "Y",
            }
        ]
    )
    cleaned = _clean_data(df)
    assert not cleaned.empty
    assert cleaned["store_and_fwd_flag"].all()


def test_load_data_mocks_mongo(mocker):
    df = pd.DataFrame([{"tpep_pickup_datetime": pd.Timestamp("2016-01-31 10:00:00")}])
    mock_collection = mocker.MagicMock()
    _load_data(df, "2016-01-31", collection=mock_collection)
    assert mock_collection.delete_many.called
    assert mock_collection.insert_many.called
