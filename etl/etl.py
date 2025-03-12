import pandas as pd
from pymongo import MongoClient
import sys
import os

CSV_FILE = "dataset_sample.csv"
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

def _extract_data(date, path=CSV_FILE):
    '''
    Extract data from the CSV file for the specified date.
    '''
    print(f"Extracting data...")
    df = pd.read_csv(path)
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df = df[df["tpep_pickup_datetime"].dt.date == pd.to_datetime(date).date()]
    return df


def _clean_data(df):
    '''
    Clean the extracted data.
    '''
    print(f"Cleaning data...")

    # remove trips that are not from NYC
    MIN_LAT, MAX_LAT = 40.4774, 40.9176
    MIN_LON, MAX_LON = -74.2591, -73.7004
    df = df[
        (df["pickup_latitude"].between(MIN_LAT, MAX_LAT)) &
        (df["pickup_longitude"].between(MIN_LON, MAX_LON)) &
        (df["dropoff_latitude"].between(MIN_LAT, MAX_LAT)) &
        (df["dropoff_longitude"].between(MIN_LON, MAX_LON))
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
        (df["fare_amount"] >= 0) &
        (df["extra"] >= 0) &
        (df["mta_tax"] >= 0) &
        (df["tip_amount"] >= 0) &
        (df["tolls_amount"] >= 0) &
        (df["improvement_surcharge"] >= 0) &
        (df["total_amount"] > 0)
    ]

    # validate and convert time columns
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    df = df[df["tpep_pickup_datetime"] < df["tpep_dropoff_datetime"]]

    # handle store_and_fwd_flag 
    df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map({"Y": True, "N": False})

    return df


def _load_data(df, date, mongo_uri=MONGO_URI, db_name=MONGO_DB_NAME, collection_name=MONGO_COLLECTION_NAME):
    '''
    Load data to MongoDB, replacing existing records for the specified date.
    '''
    print(f"Loading data to MongoDB uri {mongo_uri}...")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    # Drop existing records for the specified date
    date = pd.to_datetime(date)
    collection.delete_many({
        "tpep_pickup_datetime": {
            "$gte": date,
            "$lt": date + pd.Timedelta(days=1)
        }
    })    

    # Insert new records
    records = df.to_dict(orient="records")
    collection.insert_many(records)


def run_etl(date):
    print(f"ETL process started for {date}...")        
    df = _extract_data(date)
    if df.empty:
        print(f"No data found for {date}")
    else:
        print(f"Found {len(df)} records for {date}")
        cleaned_df = _clean_data(df)
        _load_data(cleaned_df, date)
        print(f"ETL process completed for {date}")


if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else '2016-01-31'
    run_etl(date)