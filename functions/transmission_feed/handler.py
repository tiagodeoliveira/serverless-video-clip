import os
import json
import requests

GRAPHQL_API = os.environ.get('GRAPHQL_API')
GRAPHQL_API_KEY = os.environ.get('GRAPHQL_API_KEY')
TRANSMISSION_ALLOWED_FIELDS = ["id", "start", "end", "state", "endpoints", "name", "description", "created_at", "stream_url"]
TRANSMISSION_GRAPHQL_FIELDS = f'{{ {" ".join(TRANSMISSION_ALLOWED_FIELDS)} }}'
CLIP_ALLOWED_FIELDS = ["id", "event_id", "start", "end", "state", "name", "description", "created_at", "stream_url"]
CLIP_GRAPHQL_FIELDS = f'{{ {" ".join(CLIP_ALLOWED_FIELDS)} }}'

headers = {
    'Content-Type': "application/graphql",
    'x-api-key': GRAPHQL_API_KEY,
    'cache-control': "no-cache",
}

def send_mutation(query):
    payload_obj = { "query": f"mutation {{ {query} }}" }
    payload = json.dumps(payload_obj)
    print("Sending", payload)
    response = requests.request("POST", GRAPHQL_API, data=payload, headers=headers)
    return response

def lambda_handler(event, context):
    for e in event['Records']:
        event_type = e['eventName']
        
        table_name = 'Clip' if 'clips' in e['eventSourceARN'] else 'Transmission'
        if table_name == 'Clip':
          allowed_fields = CLIP_ALLOWED_FIELDS
          graphql_fields = CLIP_GRAPHQL_FIELDS
        else:
          allowed_fields = TRANSMISSION_ALLOWED_FIELDS
          graphql_fields = TRANSMISSION_GRAPHQL_FIELDS          

        if event_type == 'INSERT':
            query = create(e['dynamodb']['NewImage'], table_name, allowed_fields, graphql_fields)
        elif event_type == 'MODIFY':
            print('Modifying', e['dynamodb']['NewImage'])
            query = update(e['dynamodb']['NewImage'], table_name, allowed_fields, graphql_fields)
        elif event_type == 'REMOVE':
            query = delete(e['dynamodb']['Keys'], table_name, graphql_fields)

        mutation = send_mutation(query)
        print(mutation.json())

    return True

def create(payload, tableName, allowed_fields, graphql_fields):
    params = get_params(payload, allowed_fields)
    return f'create{tableName}({params}) {graphql_fields}'

def update(payload, tableName, allowed_fields, graphql_fields):
    params = get_params(payload, allowed_fields)
    return f'update{tableName}({params}) {graphql_fields}'

def delete(payload, tableName, graphql_fields):
    id = payload['id']['S']
    return f'delete{tableName}(id: "{id}") {graphql_fields}'

def get_params(payload, allowed_fields):
    query = ''
    for key in payload:
        if key in allowed_fields:
            complex_val = payload[key]
            complex_val_key = list(complex_val)[0]
            if complex_val_key == 'L':
                list_value = complex_val[complex_val_key]
                value = [e['S'] for e in list_value]
            else:
                value = complex_val[complex_val_key]

            query += f'{key}: "{value}",'

    return query
