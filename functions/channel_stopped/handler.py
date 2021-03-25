import os
import re
import boto3
import time
import datetime

mediapackage = boto3.client('mediapackage')
medialive = boto3.client('medialive')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TRANSMISSION_TABLE'))

p = re.compile(r'arn:aws:medialive:(?P<region>.*):(?P<account>.*):channel:(?P<channel>.*)')

def lambda_handler(event, context):
    channel_arn = event['detail']['channel_arn']
    m = p.search(channel_arn)
    channelId = m.group('channel')
    print(channelId)
    transmission = table.query(
        IndexName=os.environ.get('TRANSMISSION_INDEX_NAME'),
        KeyConditionExpression="medialive_channel_id = :i",
        Limit=1,
        ExpressionAttributeValues={
            ":i": channelId
        }
    )['Items'][0]
    print(transmission)
    transmission_id = transmission['id']
    medialive_channel_id = transmission['medialive_channel_id']
    medialive_input_id = transmission['medialive_input_id']
    medialive_input_security_group_id = transmission['medialive_input_security_group_id']

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
                    ':s': 'deleting'
                }
            )       
            medialive.delete_channel(ChannelId=medialive_channel_id)
            time.sleep(30)
    except medialive.exceptions.NotFoundException:
        print('Channel is already delete.', medialive_channel_id)

    try:
        if medialive_input_id:
            medialive.delete_input(
                InputId=medialive_input_id
            )
    except medialive.exceptions.NotFoundException:
        print('Input is already delete.', medialive_input_id)

    try:
        if medialive_input_security_group_id:
            medialive.delete_input_security_group(InputSecurityGroupId=medialive_input_security_group_id)
    except medialive.exceptions.NotFoundException:
        print('Security Group is already delete.', medialive_input_security_group_id)

    try:
        mediapackage.delete_origin_endpoint(
            Id=transmission_id  
        )
    except mediapackage.exceptions.NotFoundException:
        print('Origin endpoint is already delete.', transmission_id)

    try:
        mediapackage.delete_channel(
            Id=transmission_id  
        )
    except mediapackage.exceptions.NotFoundException:
        print('Mediapackage channel is already delete.', transmission_id)        


    table.update_item(
        Key={
            'id': transmission_id
        },
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={
            "#s": "state"
        },
        ExpressionAttributeValues={
            ':s': 'finished'
        }
    )       

    return "deleting"