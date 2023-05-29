import json

def lambda_handler(event, context):

    if event["time_elapsed"] <= 3:
        return {
        'statusCode': 400,
        'body': 'Invalid entry. Not enough time elapsed.'
        }
    elif event["freetext"] == "":
        return {
        'statusCode': 400,
        'body':'Invalid entry. No text response'
        }
    else:
        return {
        'statusCode': 200,
        'body': 'OK'
        }