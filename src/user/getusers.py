import json
import os
import boto3

TAG = "Get all users of Aamhi unique "


def execute(event, context):
    try:
        res = get_all_from_dynamo()
        return {"statusCode": "200", "body": json.dumps(res)}
    except Exception as ex:
        print("Error while getting all user")
        return {"statusCode": "503", "body": "Error while login"}


def get_all_from_dynamo():
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    response = dynamoTable.scan()
    return response
