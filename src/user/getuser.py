import json
import os
import boto3

TAG = "Delete Aamhi unique User"


def execute(event, context):
    try:
        if event is not None:
            userId = event["pathParameters"]["userId"]
            delete_from_dynamo(userId)
    except Exception as ex:
        print("Error in Deleting user")
        return {"statusCode": "503", "body": "Error while login"}


def delete_from_dynamo(userId):
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    response = dynamoTable.get_item(Key={userId: userId})
    return response
