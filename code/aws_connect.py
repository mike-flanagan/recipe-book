import sagemaker
from sagemaker import get_execution_role
from sagemaker.predictor import csv_serializer

# Define IAM role
role = get_execution_role()
prefix = 'sagemaker/knn'
containers = {'us-west-2': '174872318107.dkr.ecr.us-west-2.amazonaws.com/knn:1',
              'us-east-1': '382416733822.dkr.ecr.us-east-1.amazonaws.com/knn:1',
              'us-east-2': '404615174143.dkr.ecr.us-east-2.amazonaws.com/knn:1',
              'eu-west-1': '438346466558.dkr.ecr.eu-west-1.amazonaws.com/knn:1',
              'ap-northeast-1': '351501993468.dkr.ecr.ap-northeast-1.amazonaws.com/knn:1',
              'ap-northeast-2': '835164637446.dkr.ecr.ap-northeast-2.amazonaws.com/knn:1',
              'ap-southeast-2': '712309505854.dkr.ecr.ap-southeast-2.amazonaws.com/knn:1'}

my_region = boto3.session.Session().region_name # set the region of the instance
print("Success - the MySageMakerInstance is in the " + my_region + " region. You will use the " + containers[my_region] + " container for your SageMaker endpoint.")