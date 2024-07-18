#!/usr/bin/env python
# coding: utf-8
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask import Flask, request, jsonify
import boto3
import os
import awsgi

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def read_data(s3_bucket, key):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = s3_client.get_object(Bucket=s3_bucket, Key=key)
    df = pd.read_csv(response.get("Body"))
    df["Gender"] = df.Gender.astype("category")
    df["VisitFrequency"] = df.VisitFrequency.astype("category")
    df["PreferredCuisine"] = df.PreferredCuisine.astype("category")
    df["TimeOfVisit"] = df.TimeOfVisit.astype("category")
    df["DiningOccasion"] = df.DiningOccasion.astype("category")
    df["MealType"] = df.MealType.astype("category")
    df["DiningOccasion"] = df.DiningOccasion.astype("category")
    df["Income_per_AverageSpend"] = df["Income"] / df["AverageSpend"]
    df["AverageSpend_per_GroupSize"] = df["AverageSpend"] / df["GroupSize"]
    df["Income_per_GroupSize"] = df["Income"] / df["GroupSize"]

    for col in df.columns:
        if df[col].dtype != "category":
            df[col] = df[col].astype(float)

    columns_to_dummy = [
        "VisitFrequency",
        "PreferredCuisine",
        "TimeOfVisit",
        "DiningOccasion",
    ]
    columns_to_encode = ["Gender", "MealType"]
    df = pd.get_dummies(df, columns=columns_to_dummy, dtype=int, drop_first=True)
    # labelencoder = LabelEncoder()

    # for col in columns_to_encode:
    #     df[col] = labelencoder.fit_transform(df[col])

    return df


def predict(model_file, df):
    with open(model_file, "rb") as f_in:
        dv, model = pickle.load(f_in)
    num_columns = [
        "Age",
        "Income",
        "AverageSpend",
        "GroupSize",
        "WaitTime",
        "ServiceRating",
        "FoodRating",
        "AmbianceRating",
    ]
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df[num_columns])
    df[num_columns] = pd.DataFrame(x_scaled, columns=num_columns)
    return model.predict(x_scaled)


def save_results(df, y_pred):
    df_result = pd.DataFrame()
    df_result["CustomerID"] = df["CustomerID"]
    df_result["predicted_rating"] = y_pred
    return df_result.loc[:, "predicted_rating"].mean()


app = Flask("customer-rating-prediction")


@app.route("/", methods=["POST"])
def index():
    try:
        AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
        df = read_data(
            "customer-satisfaction-823124982163",
            "predict/restaurant_customer_satisfaction 2.csv",
        )
        y_pred = predict("models/lin_xbg.bin", df)
        result = save_results(df, y_pred)
    except Exception as e:
        return jsonify({"error": str(e)}, status_code=500)

    return jsonify(result, stus_code=200)


def lambda_handler(event, context):
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
