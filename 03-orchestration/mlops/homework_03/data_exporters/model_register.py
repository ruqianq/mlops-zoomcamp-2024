import mlflow
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment('ny_mage_taxi')
    mlflow.sklearn.autolog()
    mlflow.sklearn.log_model(
        sk_model=data,
        artifact_path="ny-model",
        registered_model_name="sk-learn-random-forest-reg-model",
    )
    result = mlflow.register_model(
    "runs:/bb997e6ccf4842318174ad3ddd4c6847/sklearn-model", "sk-learn-ny-lr")
    return result


