import json
import os
import boto3
import uuid

TAG = "Login Aamhi unique User"


def execute(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            user = json.loads(data)
            email = user["eœmail"]
            password = user["password"]
            userExists = get_user_by_email_password(email, password)
            if userExists:
                return {"statusCode": "200", "body": f"Welcome user {email}"}
            else:
                return {
                    "statusCode": "401",
                    "body": f"Invalid User email or passsword for {email} ",
                }
    except Exception as ex:
        print("Error in Login user")
        return {"statusCode": "503", "body": "Error while login"}


def get_user_by_email_password(email, password):
    dynamodb = boto3.client("dynamodb")
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression="email= :email and password= :password",
            ExpressionAttributeValues={
                ":email": {"S": email},
                ":password": {"S": password},
            },
        )
        print(response)
        return len(response["Items"]) > 0
    except Exception as e:
        print(f"Error searching DynamoDB table: {e}")
        return False
