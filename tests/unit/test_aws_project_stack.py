import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_project.aws_project_stack import AwsProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_project/aws_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsProjectStack(app, "aws-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
