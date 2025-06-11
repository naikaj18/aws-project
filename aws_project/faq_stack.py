from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct

class FaqStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, stage: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)


        bucket = s3.Bucket(self, f"FaqBucket{stage.capitalize()}")

    
        faq_key = f"faq-{stage}.json"

        
        get_faq = _lambda.Function(
            self, "GetFaqFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("GetFAQHandler"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "FAQ_FILE": faq_key
            }
        )
        bucket.grant_read(get_faq)

        
        post_faq = _lambda.Function(
            self, "PostFaqFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("AddFAQHandler"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "FAQ_FILE": faq_key
            }
        )
        bucket.grant_read_write(post_faq)

        
        api = apigateway.RestApi(
            self, "FaqApi",
            rest_api_name="FAQ Service",
            deploy_options=apigateway.StageOptions(stage_name=stage)
        )
        faq = api.root.add_resource("faq")
        faq.add_method("GET", apigateway.LambdaIntegration(get_faq))
        faq.add_method("POST", apigateway.LambdaIntegration(post_faq))