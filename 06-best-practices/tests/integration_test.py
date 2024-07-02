from io import BytesIO
import os
from batch import read_data, prepare_data
import pandas as pd
import boto3
from datetime import datetime


def save_data(df, bucket, key):

    df.to_parquet("output.parquet", engine="pyarrow", compression=None, index=False)
    s3 = boto3.client(
        "s3",
        endpoint_url=f"http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    with open("output.parquet", "rb") as f:
        s3.put_object(Key=key, Body=f, Bucket=bucket)


# Example usage
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

save_data(df, "nyc-duration", "file.parquet")

def test_read_data():
    df_test = read_data("s3://nyc-duration/file.parquet", categorical=["PULocationID", "DOLocationID"])
    assert df_test.shape[0] == 2