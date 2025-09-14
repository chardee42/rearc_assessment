
# *** The following code was written with ChatGPT. ***

from aws_cdk import (
    App, Stack, RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_sagemaker as sagemaker,
    aws_sqs as sqs,
    aws_s3_notifications as s3n,
    aws_lambda_event_sources as sources,
    Duration,
)
from constructs import Construct


class AssessmentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ----------------------------
        # S3 Bucket
        # ----------------------------
        data_bucket = s3.Bucket(
            self, "DataBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # ----------------------------
        # Import Existing IAM Role for Lambdas
        # ----------------------------
        lambda_role = iam.Role.from_role_name(
            self, "ExistingLambdaRole", "lambda-bls-s3-role"
        )

        # ----------------------------
        # Lambda 1 (website → S3)
        # ----------------------------
        lambda_copy_bls = _lambda.Function(
            self, "LambdaCopyBLS",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_copy_bls",
            code=_lambda.Code.from_asset("lambda_copy_bls"),
            role=lambda_role
        )

        events.Rule(
            self, "DailyWebsiteRule",
            schedule=events.Schedule.rate(Duration.days(1)),
            targets=[targets.LambdaFunction(lambda_copy_bls)]
        )

        # ----------------------------
        # Lambda 2 (API → S3)
        # ----------------------------
        lambda_get_api = _lambda.Function(
            self, "LambdaGetAPI",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_get_api",
            code=_lambda.Code.from_asset("lambda_get_api"),
            role=lambda_role
        )

        events.Rule(
            self, "DailyAPIRule",
            schedule=events.Schedule.rate(Duration.days(1)),
            targets=[targets.LambdaFunction(lambda_get_api)]
        )

        # ----------------------------
        # SQS Queue (triggered by S3 JSON writes)
        # ----------------------------
        report_queue = sqs.Queue(self, "ReportQueue")

        # Notify SQS only when JSON objects are written
        data_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SqsDestination(report_queue),
            s3.NotificationKeyFilter(suffix=".json")
        )

        # ----------------------------
        # Lambda 3 (Reports → consumes SQS)
        # ----------------------------
        lambda_reports = _lambda.Function(
            self, "LambdaReports",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_reports",
            code=_lambda.Code.from_asset("lambda_reports"),
            role=lambda_role
        )

        # Allow Reports Lambda to read from the queue
        report_queue.grant_consume_messages(lambda_reports)

        # Hook up SQS as event source
        lambda_reports.add_event_source(
            sources.SqsEventSource(report_queue, batch_size=1)
        )

        # ----------------------------
        # SageMaker Notebook
        # ----------------------------
        sm_role = iam.Role(
            self, "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
        )
        data_bucket.grant_read(sm_role)

        sm_notebook = sagemaker.CfnNotebookInstance(
            self, "AnalysisNotebook",
            instance_type="ml.t2.medium",
            role_arn=sm_role.role_arn,
            notebook_instance_name="AssessmentNotebook"
        )

        # ----------------------------
        # Outputs
        # ----------------------------
        self.add_output("BucketName", data_bucket.bucket_name)
        self.add_output("LambdaCopyBLSName", lambda_copy_bls.function_name)
        self.add_output("LambdaGetAPIName", lambda_get_api.function_name)
        self.add_output("LambdaReportsName", lambda_reports.function_name)
        self.add_output("ReportQueueUrl", report_queue.queue_url)
        self.add_output("SageMakerNotebook", sm_notebook.notebook_instance_name)

    def add_output(self, name: str, value: str):
        from aws_cdk import CfnOutput
        CfnOutput(self, name, value=value)


app = App()
AssessmentStack(app, "AssessmentStack")
app.synth()
