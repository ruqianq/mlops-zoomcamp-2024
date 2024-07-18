# 2024 MLops Zoomcamp Customer Satisfaction at Restaurants Prediction Project

## Description
This is the project folder for the 2024 MLops Zoomcamp project.  I use a ML data set from Kaggle [[Predict Restaurant Customer Satisfaction Dataset](https://www.kaggle.com/datasets/rabieelkharoua/predict-restaurant-customer-satisfaction-dataset/data)] to build my mlops pipeline.

## Table of Contents

- [Overview](#overview)
- [prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Overview
This project I break it down into different compounent, the services are all deployed to AWS and using CloudFormation(CDK) to deploy.

1. Deploy a MLflow server through CDK
2. Train a Random Forest Classifier and XGBoost Classifier in SageMaker studio and store model artifast in S3 bucket
3. Hyperparameter tuning XGBoost model and register the best parameter in MLflow

## Prerequisites
You will need to have pipenv installed and an aws account.

## Installation
Install required package
```
pipenv install
```

## Usage
Instructions on how to use your project and any relevant examples.