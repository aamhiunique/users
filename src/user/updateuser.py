import json
import os
import uuid
import boto3

TAG = "Register Aamhi unique User"


def execute(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            user = json.loads(data)
            userId = user["userId"]
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
                dob = user["dob"]
                gender = user["gender"]
                martialstatus = user["martialstatus"]
                status = user["status"]
                res = update_data_to_dynamo(
                    userId,
                    userFname,
                    userLname,
                    email,
                    contact,
                    password,
                    dob,
                    gender,
                    martialstatus,
                    status,
                )
                return {"statusCode": "201", "body": "User Register Successfully"}
    except Exception as ex:
        print("Error in registaring user")
        return {"statusCode": "503", "body": "Error"}


def update_data_to_dynamo(
    userId,
    userFname,
    userLname,
    email,
    contact,
    password,
    dob,
    gender,
    martialstatus,
    status,
):
    dynamoObj = get_dynamo()
    username = userFname[0:3] + userLname[0:3]
    expression = "SET "
    expressionValues = {}
    updatedFields = {
        "userId": userId,
        "userFname": userFname,
        "userLname": userLname,
        "username": username,
        "email": email,
        "password": password,
        "active": status,
        "contact": contact,
        "dob": dob,
        "gender": gender,
        "martialstatus": martialstatus,
    }

    for key, value in updatedFields.items():
        expression += f"{key} = :{key}, "
        expressionValues[f":{key}"] = value
        expression = expression.rstrip(", ")

    dynamoObj.update_item(
        Key={"userId": userId},
        UpdateExpression=expression,
        ExpressionAttributeValues=expressionValues,
    )
    return "Success"


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
