from aws_cdk import App, Environment
import os
from aws_project.faq_stack import FaqStack

app = App()
env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                  region=os.getenv('CDK_DEFAULT_REGION'))

FaqStack(app, "FaqDev",  env=env, stage="dev")
FaqStack(app, "FaqProd", env=env, stage="prod")

app.synth()