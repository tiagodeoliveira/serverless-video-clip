import os
import re
import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TRANSMISSION_TABLE'))

p = re.compile(r'arn:aws:medialive:(?P<region>.*):(?P<account>.*):channel:(?P<channel>.*)')

def lambda_handler(event, context):

    channel_arn = event['detail']['channel_arn']
    m = p.search(channel_arn)
    channelId = m.group('channel')

    transmission = table.query(
        IndexName=os.environ.get('TRANSMISSION_INDEX_NAME'),
        KeyConditionExpression="medialive_channel_id = :i",
        Limit=1,
        ExpressionAttributeValues={
            ":i": channelId
        }
    )['Items'][0]

    table.update_item(
        Key={
            'id': transmission['id']
        },
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={
            "#s": "state"
        },
        ExpressionAttributeValues={
            ':s': 'running'
        }        
    )    

    print('State changed.', transmission)
    return event