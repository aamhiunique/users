import json
import os
import boto3
import uuid

TAG="Register Aamhi unique User"

def execuete(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            user = json.loads(data)
            userId = get_random_id()
            email = user["email"]
            contact = user["contact"]
            get_user_by_contact(contact)
            get_user_by_email(email)
            userFname = user["userFname"]
            userLname = user["userLname"]
            aadhar = user["aadhar"]
            pan = user["pan"]
            print(pan)
            res = put_data_to_dynamo(userId,userFname,userLname,email,contact,aadhar,pan);
        return {
        "statusCode": "200",
        "body": res
        }
    except Exception as ex:
        print("Error in registaring user")
    return {
            "statusCode": "503",
            "body": "Error"
    }
    
def put_data_to_dynamo(userId, userFname, userLname, email, contact, aadhar, pan):
    dynamoObj = get_dynamo()
    username = userFname[1:3] + userLname[1:3]
    dynamoObj.put_item(
        Item={
            "userId":userId,
            "userFname":userFname,
            "userLname":userLname,
            "username": username,
            "email":email,
            "contact":contact,
            "aadhar":aadhar,
            "pan":pan
        }
    )
    return "Success"

def get_random_id():
    id = str(uuid.uuid4())
    return id


def get_user_by_email(email):
    dynamoObj = get_dynamo()
    response = dynamoObj.query(
        KeyConditionExpression=Attr('email').eq(email)
    )
    print(response)
    return "User with email already exists"

def get_user_by_contact(contact):
    dynamoObj = get_dynamo()
    response = dynamoObj.query(
        KeyConditionExpression=Attr('contact').eq(contact)
    )
    print(response)
    return "User with contact already exists"

def get_dynamo():
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    return dynamoTable