"""ETL job that processes and loads data into MongoDB."""

import sys
import os
import pandas as pd
from pymongo import MongoClient

CSV_FILE = "dataset_sample.csv"
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")


def _extract_data(processing_date, path=CSV_FILE):
    """
    Extract data from the CSV file for the specified date.
    """
    print("Extracting data...")
    df = pd.read_csv(path)
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df = df[
        df["tpep_pickup_datetime"].dt.date == pd.to_datetime(processing_date).date()
    ]
    return df


def _clean_data(df):
    """
    Clean the extracted data.
    """
    print("Cleaning data...")

    # remove trips that are not from NYC
    min_lat, max_lat = 40.4774, 40.9176
    min_lon, max_lon = -74.2591, -73.7004
    df = df[
        (df["pickup_latitude"].between(min_lat, max_lat))
        & (df["pickup_longitude"].between(min_lon, max_lon))
        & (df["dropoff_latitude"].between(min_lat, max_lat))
        & (df["dropoff_longitude"].between(min_lon, max_lon))
    ]

    # remove trips with zero passengers
    df = df[df["passenger_count"] > 0]

    # remove trips with unrealistic trip_distance
    df = df[(df["trip_distance"] > 0.5) & (df["trip_distance"] < 100)]

    # validate rate codes & payment types
    df = df[df["RatecodeID"].isin([1, 2, 3, 4, 5, 6])]
    df = df[df["payment_type"].isin([1, 2, 3, 4, 5])]

    # remove negative or unrealistic fares
    df = df[
        (df["fare_amount"] >= 0)
        & (df["extra"] >= 0)
        & (df["mta_tax"] >= 0)
        & (df["tip_amount"] >= 0)
        & (df["tolls_amount"] >= 0)
        & (df["improvement_surcharge"] >= 0)
        & (df["total_amount"] > 0)
    ]

    # validate and convert time columns
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    df = df[df["tpep_pickup_datetime"] < df["tpep_dropoff_datetime"]]

    # handle store_and_fwd_flag
    df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map({"Y": True, "N": False})

    return df


def _load_data(
    df,
    processing_date,
    mongo_config=None,
    collection=None,
):
    """
    Load data to MongoDB, replacing existing records for the specified date.
    """
    if not collection:
        mongo_config = mongo_config or {
            "uri": MONGO_URI,
            "db": MONGO_DB_NAME,
            "collection": MONGO_COLLECTION_NAME,
        }
        print(f"Loading data to MongoDB uri {mongo_config["uri"]}...")
        client = MongoClient(mongo_config["uri"])
        db = client[mongo_config["db"]]
        collection = db[mongo_config["collection"]]

    # Drop existing records for the specified date
    processing_date = pd.to_datetime(processing_date)
    collection.delete_many(
        {
            "tpep_pickup_datetime": {
                "$gte": processing_date,
                "$lt": processing_date + pd.Timedelta(days=1),
            }
        }
    )

    # Insert new records
    records = df.to_dict(orient="records")
    collection.insert_many(records)


def run_etl(processing_date, collection=None):
    """
    Run the ETL process for the specified date.
    """
    print(f"ETL process started for {processing_date}...")
    df = _extract_data(processing_date)
    if df.empty:
        print(f"No data found for {processing_date}")
    else:
        print(f"Found {len(df)} records for {processing_date}")
        cleaned_df = _clean_data(df)
        _load_data(cleaned_df, processing_date, collection=collection)
        print(f"ETL process completed for {processing_date}")


if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else "2016-01-31"
    run_etl(date)
