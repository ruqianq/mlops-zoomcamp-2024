import pandas as pd
import boto3
from datetime import datetime
import os


S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", None)

options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

def save_data(df, bucket, key):
    parquet_buffer = df.to_parquet(
        "s3://nyc-duration/file.parquet",
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options,
    )
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, key).put(Body=parquet_buffer.getvalue())

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

save_data(df, 'your-s3-bucket', 'your-file-key.csv')
