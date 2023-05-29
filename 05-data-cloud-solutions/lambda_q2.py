import boto3
import json

s3 = boto3.resource('s3') 

def lambda_handler(event, context):

    key = event["user_id"] + event["timestamp"] + ".json"

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
        # Only upload valid survey entries to S3 bucket
        s3.Bucket('mariagabrielaa-a5').put_object(Key=key, Body=json.dumps(event))

        return {
        'statusCode': 200,
        'body': 'OK'
        }