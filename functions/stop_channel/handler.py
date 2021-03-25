import os
import sys
import json
import uuid
import time
import boto3

medialive = boto3.client('medialive')
dynamodb = boto3.client('dynamodb')
dynamodb_r = boto3.resource('dynamodb')
table = dynamodb_r.Table(os.environ.get('TRANSMISSION_TABLE'))

def lambda_handler(event, context):    
    if 'pathParameters' in event:
        transmission_id = event['pathParameters']['id']
    else:
        transmission_id = event['id']

    print('Finishing transmission', transmission_id)
    
    transmission = dynamodb.get_item(
        TableName=os.environ.get('TRANSMISSION_TABLE'),
        Key={
            'id': { 'S': transmission_id }
        }
    )
    
    if not 'Item' in transmission or transmission['Item']['state']['S'] == "finished":
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "transmission not found or already finished."
            })
        }        

    transmission_name = transmission['Item']['name']['S']
    medialive_channel_id = transmission['Item']['medialive_channel_id']['S']

    try:
        if medialive_channel_id:
            table.update_item(
                Key={
                    'id': transmission_id
                },
                UpdateExpression="SET #s = :s",
                ExpressionAttributeNames={
                    "#s": "state"
                },
                ExpressionAttributeValues={
                    ':s': 'stopping'
                }
            )       
            medialive.stop_channel(ChannelId=medialive_channel_id)
    except medialive.exceptions.NotFoundException:
        print('Channel was already stopped.', medialive_channel_id)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "stopping",
            "id": transmission_id,
            "name": transmission_name
        })
    }