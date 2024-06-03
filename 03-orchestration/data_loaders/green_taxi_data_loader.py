import io
import pandas as pd
from datetime import datetime
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    base_url = 'https://data.cityofnewyork.us/api/views/8nfn-ifaj/rows.csv?accessType=DOWNLOAD'
    # oct_url = 'green_tripdata_2020-10.csv.gz'
    # nov_url = 'green_tripdata_2020-11.csv.gz'
    # dec_url = 'green_tripdata_2020-12.csv.gz'

    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                    }



    # return pd.read_csv(
    #     base_url+oct_url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
    #     )
    url = base_url
    # native date parsing 
    df = pd.read_csv(
        url, sep=',', dtype=taxi_dtypes
        )
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime']).dt.strftime('%Y-%m-%d')
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime']).dt.strftime('%Y-%m-%d')

    return df
    

@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
    assert df.shape[0] != 0, 'The output is undefined'