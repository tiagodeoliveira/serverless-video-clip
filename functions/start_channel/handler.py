import os
import boto3

medialive = boto3.client('medialive')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TRANSMISSION_TABLE'))

def lambda_handler(event, context):
    channel_id = event['medialive_channel_id']
    transmission_id = event['id']
    medialive.start_channel(ChannelId=channel_id)

    table.update_item(
        Key={
            'id': transmission_id
        },
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={
            "#s": "state"
        },
        ExpressionAttributeValues={
            ':s': 'starting'
        }
    )
        
    print('Starting done.', event)
    return event