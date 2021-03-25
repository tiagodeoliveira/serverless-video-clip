import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('CLIP_TABLE'))
client = boto3.client('mediapackage-vod')

def lambda_handler(event, context):

    clip_id = event['detail']['harvest_job']['id']
    status = event['detail']['harvest_job']['status']

    table.update_item(
        Key={
            'id': clip_id
        },
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={
            "#s": "state"
        },
        ExpressionAttributeValues={
            ':s': status.lower()
        }        
    )

    if status == "SUCCEEDED":
        table.update_item(
            Key={
                'id': clip_id
            },
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={
                "#s": "state"
            },
            ExpressionAttributeValues={
                ':s': 'publishing'
            }        
        )

        bucket_name = event['detail']['harvest_job']['s3_destination']['bucket_name']
        manifest_key = event['detail']['harvest_job']['s3_destination']['manifest_key']

        source_arn = f"arn:aws:s3:::{bucket_name}/{manifest_key}"

        asset = client.create_asset(
            Id=clip_id,
            PackagingGroupId='video-clip-packaging',
            SourceArn=source_arn,
            SourceRoleArn=os.environ.get('INGESTION_ROLE')
        )       

        table.update_item(
            Key={
                'id': clip_id
            },
            UpdateExpression="SET #s = :s, stream_url = :p",
            ExpressionAttributeNames={
                "#s": "state"
            },
            ExpressionAttributeValues={
                ':s': 'published',
                ':p': asset['EgressEndpoints'][0]['Url'],
            }        
        )

    return event
