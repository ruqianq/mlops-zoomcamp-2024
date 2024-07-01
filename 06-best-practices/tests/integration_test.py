from datetime import datetime
from batch import read_data, prepare_data
import pandas as pd
import boto3
from io import BytesIO
import os


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
]

columns = [
    "PULocationID",
    "DOLocationID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]
df = pd.DataFrame(data, columns=columns)


def save_data(df, bucket, key):
    df.to_parquet(
        "s3://nyc-duration/file.parquet",
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options,
    )

save_data(df, "nyc-duration", "file.parquet")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", None)

options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}


def test_read_data():
    df_output = read_data(
        "s3://nyc-duration/file.parquet", ["PULocationID", "DOLocationID"]
    )
    
    assert df_output.shape[0] == 2
