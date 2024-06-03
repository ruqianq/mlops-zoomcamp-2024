import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
    # oct_url = 'green_tripdata_2020-10.csv.gz'
    # nov_url = 'green_tripdata_2020-11.csv.gz'
    # dec_url = 'green_tripdata_2020-12.csv.gz'
    # return pd.read_csv(
    #     base_url+oct_url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
    #     )
    url = base_url
    # native date parsing 
    df = pd.read_parquet(url)
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert output.shape[0] != 0, 'The output is undefined'