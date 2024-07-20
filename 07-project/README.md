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
4. Deploy model through CDK as a Lambda function

## Prerequisites
1. AWS Account
You need an AWS account with sufficient permissions to create and manage resources such as S3 buckets, Lambda functions, and SageMaker instances.

2.AWS CLI
Install and configure the AWS Command Line Interface (CLI) to interact with AWS services.
[Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
Configure AWS CLI with your credentials
```
aws configure
```
3.Python and Pipenv
Ensure you have at least 3.10 python installed and latest pipenv
[Install pipenv](https://chatgpt.com/c/51105a15-ecd5-46cc-b242-5d69d0163c7c#:~:text=and%20virtual%20environments.-,Install%20pipenv,-Install%20pipenv%20using)

4. Docker
Install Docker to build and deploy containerized applications.

## Installation
1. Clone the Repository
```
git clone https://github.com/yourusername/mlops-zoomcamp-2024.git
cd mlops-zoomcamp-2024/07-project
```
2. Install Required Packages and activate the virtual environment
Install required package through pipenv
```
pipenv install
pipenv shell
```
3. Set Up Environment
```
export AWS_ACCESS_KEY_ID = [YOUR AWS ACCESS KEY ID]
export AWS_SECRET_ACCESS_KEY = [YOUR AWS SECRET ACCESS KEY]
export AWS_REGION=[YOUR AWS REGION]
```

## Usage
1. Deploying MLflow Server as experiment tracking in AWS
    a. Navigate to the MLflow Directory
    ```
    cd experiment-tracking
    ```
    b. Deploy MLflow using AWS CDK
    ```
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account | tr -d '"')
    AWS_REGION=$(aws configure get region)
    cdk bootstrap aws://${ACCOUNT_ID}/${AWS_REGION}
    cdk deploy --parameters ProjectName=mlflow --require-approval never
    ```
    c. Then you can navigate to your CloudFormation output and get the URL of your remote MLflow server
    ```
    import mlflow
    mlflow.set_tracking_uri('<YOUR LOAD BALANCER URI>')
    ```
    NOTE: this example is from [this repo](https://github.com/aws-samples/amazon-sagemaker-mlflow-fargate) from AWS
    ![image info](images/Screenshot 2024-07-20 at 5.27.26 PM.png)

2. Training and register model in SageMaker
    a. Open SageMaker Studio in AWS and Create a domain
    b. Navigate to notebooks
    ```
    cd notebooks
    ```
    c. Upload notebooks and run all the blocks and in the end you should be able to register the model and see the model artifest save under S3 bucket:
    ![image info](images/Screenshot 2024-07-20 at 5.37.49 PM.png)
    ![image info](images/Screenshot 2024-07-20 at 5.41.43 PM.png)

3. Training and register model in Mage
    a. Navigate to orchestration
    ```
    cd orchestration
    ```
    b. Run the docker compose
    ```
    docker-compose up
    ```
    c. Navigate to [localhost](http://localhost:6789/)
    b. Run the pipeline
    ![image info](images/Screenshot 2024-07-20 at 5.54.47 PM.png)
