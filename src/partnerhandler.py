import json


def execuete(event, context):
    body = {
        "message": "This is partner Handler",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response