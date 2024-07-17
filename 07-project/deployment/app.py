from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk import Duration, Stack, App, aws_lambda as _lambda
from aws_cdk.aws_apigateway import (
    LambdaIntegration,
    RestApi,
)
from constructs import Construct


class AwsCdkFlaskStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = RestApi(self, "flask-api", rest_api_name="flask-api")

        flask_lambda = PythonFunction(
            self,
            "lambda_handler",
            function_name="flask-lambda",
            entry="lambda",
            index="lambda_handler.py",
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=Duration.seconds(30),
        )

        root_resource = api.root

        any_method = root_resource.add_method("ANY", LambdaIntegration(flask_lambda))


app = App()
AwsCdkFlaskStack(app, "MLflowStack")
app.synth()
