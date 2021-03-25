import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ.get('TRANSMISSION_TABLE'))

    scan_filter = {
        'state': {
            'AttributeValueList': [
                'finished',
            ],
            'ComparisonOperator': 'NE'
        }
    }
    
    response = table.scan(ScanFilter=scan_filter)
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], ScanFilter=scan_filter)
        data.extend(response['Items'])

    transmissions = [{
        'name': i['name'],
        'description': i['description'],
        'id': i['id'],
        'start': i['start'],
        'end': i['end'],
        'state': i['state'],
        'endpoints': i['endpoints']
    } for i in data]
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "transmissions": transmissions
        })
    }    