import os
import pickle
import click
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    dv = load_pickle(os.path.join(data_path, "dv.pkl"))

    rf = RandomForestRegressor(max_depth=10, random_state=0)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_val)

    rmse = mean_squared_error(y_val, y_pred, squared=False)
    with open('./models/ran_for.bin', 'wb') as f_out:
        pickle.dump((dv, rf), f_out)


    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("nyc-taxi-homework")
    with mlflow.start_run():

        mlflow.set_tag("developer", "daisy_lin")

        mlflow.log_param("train-data-path", "./green_tripdata_2023-01.parquet")
        mlflow.log_param("valid-data-path", "./green_tripdata_2023-02.parquet")
        mlflow.log_param("test-data-path", "./green_tripdata_2023-03.parquet")

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric('min_samples_split', rf.min_samples_split)

        mlflow.log_artifact(local_path="./models/ran_for.bin", artifact_path="models_pickle")


if __name__ == '__main__':
    run_train()
