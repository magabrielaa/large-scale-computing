import boto3
import json
from boto3.dynamodb.conditions import Key

s3 = boto3.resource('s3') 
dynamodb = boto3.resource('dynamodb')

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

        table = dynamodb.Table("a5_results")
        
        # First, check if there is already an entry in the table for the user_id
        response = table.get_item(
            Key={'user_id': event["user_id"]}
            )
        # If no previous entry, then set num_submission to 0
        if "Item" not in response:
            num_submission = 0
        # Otherwise, query the previous number of submissions
        else:
            response = table.query(KeyConditionExpression=Key('user_id').eq(event["user_id"]),
            ProjectionExpression='num_submission')
            num_submission = response['Items'][0]['num_submission']

        # Insert survey entry in DynamoDb table
        table.put_item(Item= {
                            'user_id': event['user_id'],
                            'q1': event['q1'],
                            'q2': event['q2'],
                            'q3': event['q3'],
                            'q4': event['q4'],
                            'q5': event['q5'],
                            'freetext': event['freetext'],
                            'num_submission': int(num_submission) + 1
                            }
                        )
        return {
        'statusCode': 200,
        'body': 'OK. DynamoDB table updated and response uploaded to S3'
        }