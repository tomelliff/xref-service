import json
import os

import boto3

import xref_service

dynamodb = boto3.resource('dynamodb')

table_name=os.environ['DYNAMODB_TABLE']

table = dynamodb.Table(table_name)

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def get_ids(event, context):
    path_parameters = event['pathParameters']
    system = path_parameters['system']
    system_id = path_parameters['system_id']
    system_object = {'system': system, 'id': system_id}

    ids = xref_service.get_ids(table, system_object)

    response = {
        "statusCode": 200,
        "body": json.dumps(ids)
    }

    return response

# event = json.loads("""{
#     "body": null,
#     "resource": "\/xref-service\/{system}\/{system_id}",
#     "requestContext": {
#       "resourceId": "erc1sw",
#       "apiId": "jn6nxk2tw9",
#       "resourcePath": "\/xref-service\/{system}\/{system_id}",
#       "httpMethod": "GET",
#       "requestId": "a6528c1b-2066-11e7-8887-8f1bd1f9950b",
#       "accountId": "423845407043",
#       "identity": {
#         "apiKey": null,
#         "userArn": null,
#         "cognitoAuthenticationType": null,
#         "accessKey": null,
#         "caller": null,
#         "userAgent": "curl\/7.47.0",
#         "user": null,
#         "cognitoIdentityPoolId": null,
#         "cognitoIdentityId": null,
#         "cognitoAuthenticationProvider": null,
#         "sourceIp": "52.212.137.235",
#         "accountId": null
#       },
#       "stage": "dev"
#     },
#     "queryStringParameters": null,
#     "httpMethod": "GET",
#     "pathParameters": {
#       "system_id": "123456",
#       "system": "global"
#     },
#     "headers": {
#       "Via": "1.1 479d3d8cfdf8d35634b50f89a5beaa9e.cloudfront.net (CloudFront)",
#       "CloudFront-Is-Desktop-Viewer": "true",
#       "CloudFront-Is-SmartTV-Viewer": "false",
#       "CloudFront-Forwarded-Proto": "https",
#       "X-Forwarded-For": "52.212.137.235, 216.137.56.78",
#       "CloudFront-Viewer-Country": "IE",
#       "Accept": "*\/*",
#       "User-Agent": "curl\/7.47.0",
#       "X-Amzn-Trace-Id": "Root=1-58efa7e2-59fbd7a83bc77f795d937d39",
#       "Host": "jn6nxk2tw9.execute-api.eu-west-1.amazonaws.com",
#       "X-Forwarded-Proto": "https",
#       "X-Amz-Cf-Id": "zNanlXNzfK07ePqPkCZIUhs1pbbxWA6Im36VPD9BHPlRw-tWlBSeIQ==",
#       "CloudFront-Is-Tablet-Viewer": "false",
#       "X-Forwarded-Port": "443",
#       "CloudFront-Is-Mobile-Viewer": "false"
#     },
#     "stageVariables": null,
#     "path": "\/xref-service\/global\/123456",
#     "isBase64Encoded": false
#   }
# """)
#
# get_ids(event, 'context')
