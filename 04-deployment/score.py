#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pickle
import pandas as pd


# In[5]:


def read_data(filename):
    categorical = ['PULocationID', 'DOLocationID']
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def predict(model_file, df):
    with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    return model.predict(X_val)


def save_results(df, y_pred, output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[41]:


df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[ ]:


def run():
    df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')
    y_pred = predict('model.bin', df)
    df['ride_id'] = f'{2023:04d}/{3:02d}_' + df.index.astype('str')
    save_results(df, y_pred, f'output/{2023:04d}-{3:02d}.parquet')
    
if __name__ == '__main__':
    run()

