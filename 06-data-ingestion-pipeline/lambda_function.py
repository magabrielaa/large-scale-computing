import boto3
import json
from boto3.dynamodb.conditions import Key

s3 = boto3.resource('s3') 
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    # Read in data from SQS queue
    data = json.loads(event['Records'][0]['body'])
    
    key = data["user_id"] + data["timestamp"] + ".json"

    if data["time_elapsed"] <= 3:
        return {
        'statusCode': 400,
        'body': 'Invalid entry. Not enough time elapsed.'
        }
    elif data["freetext"] == "":
        return {
        'statusCode': 400,
        'body':'Invalid entry. No text response'
        }
    else:
        # Only upload valid survey entries to S3 bucket
        s3.Bucket('mariagabrielaa-a6').put_object(Key=key, Body=json.dumps(data))

        table = dynamodb.Table("a6_results")
        
        # First, check if there is already an entry in the table for the user_id
        response = table.get_item(
            Key={'user_id': data["user_id"]}
            )
        # If no previous entry, then set num_submission to 0
        if "Item" not in response:
            num_submission = 0
        # Otherwise, query the previous number of submissions
        else:
            response = table.query(KeyConditionExpression=Key('user_id').eq(data["user_id"]),
            ProjectionExpression='num_submission')
            num_submission = response['Items'][0]['num_submission']

        # Insert survey entry in DynamoDb table
        table.put_item(Item= {
                            'user_id': data['user_id'],
                            'q1': data['q1'],
                            'q2': data['q2'],
                            'q3': data['q3'],
                            'q4': data['q4'],
                            'q5': data['q5'],
                            'freetext': data['freetext'],
                            'num_submission': int(num_submission) + 1
                            }
                        )
        return {
        'statusCode': 200,
        'body': 'OK. DynamoDB table updated and response uploaded to S3'
        }