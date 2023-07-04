import json


def execuete(event, context):
    body = {
        "message": "Hello World! latest for app sync",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response