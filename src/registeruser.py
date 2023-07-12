import json
import os
import boto3
import uuid

TAG = "Register Aamhi unique User"


def execuete(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            user = json.loads(data)
            userId = get_random_id()
            email = user["email"]
            contact = user["contact"]
            userExistsByEmail = get_user_by_email(email)
            userExistsByContact = get_user_by_contact(contact)
            if userExistsByEmail:
                return {
                    "statusCode": "201",
                    "body": f"User with email {email} already exists",
                }
            elif userExistsByContact:
                return {
                    "statusCode": "201",
                    "body": f"User with contact {contact} already exists",
                }
            else:
                userFname = user["userFname"]
                userLname = user["userLname"]
                password = user["password"]
                email = user["email"]
                contact = user["contact"]
                res = put_data_to_dynamo(
                    userId, userFname, userLname, email, contact, password
                )
                return {"statusCode": "201", "body": "User Register Successfully"}
    except Exception as ex:
        print("Error in registaring user")
        return {"statusCode": "503", "body": "Error"}


def put_data_to_dynamo(userId, userFname, userLname, email, contact, password):
    dynamoObj = get_dynamo()
    username = userFname[0:3] + userLname[0:3]
    print(username)
    dynamoObj.put_item(
        Item={
            "userId": userId,
            "userFname": userFname,
            "userLname": userLname,
            "username": username,
            "email": email,
            "password": password,
            "active": 0,
            "contact": contact,
        }
    )
    return "Success"


def get_random_id():
    id = str(uuid.uuid4())
    return id


def get_dynamo():
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    return dynamoTable


def get_user_by_email(email):
    dynamodb = boto3.client("dynamodb")
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression="email= :email",
            ExpressionAttributeValues={":email": {"S": email}},
        )
        return len(response["Items"]) > 0
    except Exception as e:
        print(f"Error searching DynamoDB table: {e}")
        return False


def get_user_by_contact(contact):
    dynamodb = boto3.client("dynamodb")
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression="contact= :contact",
            ExpressionAttributeValues={":contact": {"S": contact}},
        )
        return len(response["Items"]) > 0
    except Exception as e:
        print(f"Error searching DynamoDB table: {e}")
        return False
