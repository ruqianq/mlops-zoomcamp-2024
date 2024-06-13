#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pickle
import pandas as pd
import argparse
from flask import Flask, request, jsonify


def read_data(filename, categorical):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def predict(model_file, df, categorical):
    with open(model_file, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    return model.predict(X_val)


def save_results(df, y_pred):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    return (df_result.loc[:, 'predicted_duration'].mean())


app = Flask('duration-prediction')

@app.route('/score', methods=['POST'])
def predict_endpoint():
    categorical = ['PULocationID', 'DOLocationID']
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-05.parquet', categorical=categorical)
    y_pred = predict('model.bin', df, categorical=categorical)
    df['ride_id'] = f'{2023:04d}/{5:02d}_' + df.index.astype('str')
    result = save_results(df, y_pred)

    return jsonify(result)    
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
