from datetime import datetime
from batch import read_data, prepare_data
import pandas as pd


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)


def test_prepare_data():
    df_prep = prepare_data(['PULocationID', 'DOLocationID'], df)
    assert df_prep.shape[0] == 2
    assert df_prep.columns.tolist() == ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
    assert df_prep.iloc[0].duration == 9.0
    assert df_prep.iloc[0].PULocationID == '-1'
    assert df_prep.iloc[0].DOLocationID == '-1'
    assert df_prep.iloc[0].tpep_pickup_datetime == dt(1, 1)
    assert df_prep.iloc[0].tpep_dropoff_datetime == dt(1, 10)