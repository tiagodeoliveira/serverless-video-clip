import os
import json
import boto3
import uuid

madantory_keys = ["name",  "description", "start", "end"]

mediapackage = boto3.client('mediapackage')
dynamodb = boto3.client('dynamodb')

DEFAULT_HEADERS = {
    "Access-Control-Allow-Headers": '*',
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": '*'
}

def lambda_handler(event, context):
    transmission_id = event['pathParameters']['id']
    
    request = request_proxy(event)
    request_body = request['body']

    missing_fields = list(set(madantory_keys) ^ set(request_body.keys()))

    if missing_fields:
        print("Missing fields", missing_fields)
        return {
            "statusCode": 400,
            "body": json.dumps({
                e: "is mandatory" for e in missing_fields
            }),
            "headers": DEFAULT_HEADERS,
        }

    clip_id = str(uuid.uuid4())
    clip_title = request_body.get('name')
    clip_description = request_body.get('description', '')
    clip_start = request_body.get('start')
    clip_end = request_body.get('end')

    print(f'Creating clip ({clip_id}) for transmission ({transmission_id}). "{clip_title}" - "{clip_description}", {clip_start} to {clip_end}')

    transmission = dynamodb.get_item(
        TableName=os.environ.get('TRANSMISSION_TABLE'),
        Key={
            'id': { 'S': transmission_id }
        }
    )

    if not 'Item' in transmission and transmission['Item']['state']['S'] != "finished":
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "transmission not found or stopped."
            }),
            "headers": DEFAULT_HEADERS,
        }        

    request_body = request['body']

    try:
        harvest_job = mediapackage.create_harvest_job(
            EndTime=clip_end,
            Id=clip_id,
            OriginEndpointId=transmission_id,
            S3Destination={
                'BucketName': os.environ.get('ASSET_BUCKET'),
                'ManifestKey': f'clips/{clip_id}/index.m3u8',
                'RoleArn': os.environ.get('MEDIAPACKAGE_JOB_ROLE')
            },
            StartTime=clip_start
        )       
        print(json.dumps(harvest_job))
    except Exception as e:
        print("Failure creating the job", e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Clip not created",
                "error": str(e),
                "id": clip_id
            }),
            "headers": DEFAULT_HEADERS,
        }

    dynamodb.put_item(
        TableName=os.environ.get('CLIP_TABLE'),
        Item={
            'id': {'S': clip_id},
            'event_id': {'S': transmission_id},
            'name': {'S': clip_title},
            'start': {'S': clip_start},
            'end': {'S': clip_end},
            'description': {'S': clip_description},
            'state': {'S': 'creating'}
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "creating",
            "id": clip_id
        }),
        "headers": DEFAULT_HEADERS,
    }

def request_proxy(data):
    request = {}
    request = data
    if data["body"]:
        request["body"] = json.loads(data["body"])
    return request