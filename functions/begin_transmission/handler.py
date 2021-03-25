import os
import sys
import json
import uuid
import boto3
import botocore
import dateutil.parser
from datetime import datetime

medialive = boto3.client('medialive')
mediapackage = boto3.client('mediapackage')
mediapackage_vod = boto3.client('mediapackage-vod')
dynamodb = boto3.client('dynamodb')

DEFAULT_HEADERS = {
    "Access-Control-Allow-Headers": '*',
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": '*'
}

madantory_keys = ["name", "start", "end", "producer_cidrs"]
content_outputs = [
        {
            'name': '416_234',
            'video': {
                'Height': 234,
                'Width': 416,
                'Bitrate': 200000,
                'GopNumBFrames': 0,
                'GopSize': 30,
                'Level': 'H264_LEVEL_3',
                "FramerateNumerator": 15000,
                'Profile': 'BASELINE',
                'RateControlMode': 'CBR'
            },
            'audio': {
                'Bitrate': 64000
            }
        }, {
            'name': '1920_1080',
            'video': {
                'Height': 1080,
                'Width': 1920,
                'Bitrate': 8000000,
                'GopNumBFrames': 1,
                'GopSize': 60,
                'Level': 'H264_LEVEL_4_1',
                "FramerateNumerator": 30000,
                'Profile': 'HIGH',
                'RateControlMode': 'CBR'
            },
            'audio': {
                'Bitrate': 128000
            }
        }
    ]

def request_proxy(data):
    request = {}
    request = data
    if data["body"]:
        request["body"] = json.loads(data["body"])
    return request


def lambda_handler(event, context):
    """
        Params:
            event.body:
                name: event name
                description: description of the event
                start: event start datetime
                end: event end datetime
    """

    request = request_proxy(event)
    request_body = request['body']

    missing_fields = list(set(madantory_keys) - set(request_body.keys()))
    if missing_fields:
        print("Missing fields", missing_fields)
        return {
            "statusCode": 400,
            "body": json.dumps({
                e: "is mandatory" for e in missing_fields
            }),
            "headers": DEFAULT_HEADERS
        }

    transmission_name = request_body.get('name')
    transmission_description = request_body.get('description', '')
    transmission_start = request_body.get('start')
    transmission_end = request_body.get('end')
    producer_cidrs = request_body.get('producer_cidrs')
    transmission_protocol = 'RTMP_PUSH'

    transmission_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    print("Creating new transmission", transmission_id, transmission_name,
          transmission_start, transmission_end, transmission_description, transmission_protocol)

    execution_error = None
    try:
        medialive_input, medialive_input_security_group = create_medialive_input(transmission_id, transmission_name, transmission_protocol, producer_cidrs, created_at)
        medialive_input_id = medialive_input['Input']['Id']
        medialive_input_security_group_id = medialive_input_security_group['SecurityGroup']['Id']

        stream_url = create_mediapackage_channel(transmission_id, transmission_name, transmission_start, transmission_end, created_at)
        
        medialive_channel = create_medialive_channel(transmission_id, transmission_name, medialive_input['Input']['Id'], created_at)         
        medialive_channel_id = medialive_channel['Channel']['Id']
        endpoints = [i['Url'] for i in medialive_input['Input']['Destinations']]
    except Exception as error:
        execution_error = error
        print("Error", error)

    create_dynamodb_item(
        transmission_id, 
        transmission_name, 
        transmission_start,
        transmission_end, 
        transmission_description, 
        transmission_protocol,
        medialive_channel_id if 'medialive_channel_id' in vars() else '',
        medialive_input_id if 'medialive_input_id' in vars() else 'error',
        medialive_input_security_group_id if 'medialive_input_security_group_id' in vars() else '',
        'creating' if endpoints else 'failed',
        created_at,
        endpoints,
        stream_url if 'stream_url' in vars() else '',
    )

    if not execution_error:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "id": transmission_id,
                "name": transmission_name,
                "protocol": transmission_protocol,
                "endpoint": endpoints
            }),
            "headers": DEFAULT_HEADERS,
        }
    else:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Transmission not started",
                "id": transmission_id
            }),
            "headers": DEFAULT_HEADERS,
        }
        
def create_dynamodb_item(transmission_id, transmission_name, transmission_start, transmission_end, transmission_description, transmission_protocol,  medialive_channel_id, medialive_input_id, medialive_input_security_group_id, transmission_state, created_at, endpoints, stream_url):
    dynamodb.put_item(
        TableName=os.environ.get('TRANSMISSION_TABLE'),
        Item={
            'id': {'S': transmission_id},
            'name': {'S': transmission_name},
            'start': {'S': transmission_start},
            'end': {'S': transmission_end},
            'description': {'S': transmission_description},
            'protocol': {'S': transmission_protocol},
            'medialive_channel_id': { 'S': medialive_channel_id }, 
            'medialive_input_id': { 'S': medialive_input_id },
            'medialive_input_security_group_id': { 'S': medialive_input_security_group_id },
            'state': { 'S': transmission_state },
            'created_at': { 'S': created_at },
            'endpoints': { 'L': [ { 'S': i } for i in endpoints ] },
            'stream_url': { 'S': stream_url }
        }
    )

def create_medialive_input(transmission_id, transmission_name, transmission_protocol, producer_cidrs, created_at):
    input_security_group = medialive.create_input_security_group(
        Tags={
            'created_at': created_at,
            'transmission': transmission_id,
            'Name': transmission_name,
        },
        WhitelistRules=[
            {'Cidr': i} for i in producer_cidrs
        ]
    )

    input_security_group_id = input_security_group['SecurityGroup']['Id']

    medialive_input = medialive.create_input(
        Tags={
            'created_at': created_at,
            'transmission': transmission_id,
            'Name': transmission_name
        },
        Destinations=[
            {'StreamName': f'a/{transmission_id}'},
            {'StreamName': f'b/{transmission_id}'},
        ],
        InputSecurityGroups=[input_security_group_id],
        Name=transmission_name,
        Type=transmission_protocol,
    )

    print('input_security_group', input_security_group)
    print('medialive_input', medialive_input)

    return medialive_input, input_security_group


def create_mediapackage_channel(transmission_id, transmission_name, transmission_start, transmission_end, created_at):
    channel = mediapackage.create_channel(
        Id=transmission_id,
        Description=transmission_name,
        Tags={
            'created_at': created_at,
            'transmission': transmission_id,
            'Name': transmission_name
        }
    )

    delta = dateutil.parser.isoparse(transmission_end) - dateutil.parser.isoparse(transmission_start)
    buffer_time_in_secs = max(300, delta.seconds)

    endpoint = mediapackage.create_origin_endpoint(
        # Authorization={
        #     'CdnIdentifierSecret': 'string',
        #     'SecretsRoleArn': 'string'
        # },
        ChannelId=transmission_id,
        HlsPackage={
            'AdMarkers': 'NONE',
            'AdTriggers': [
                "SPLICE_INSERT",
                "PROVIDER_ADVERTISEMENT",
                "DISTRIBUTOR_ADVERTISEMENT",
                "PROVIDER_PLACEMENT_OPPORTUNITY",
                "DISTRIBUTOR_PLACEMENT_OPPORTUNITY"
            ],
            'AdsOnDeliveryRestrictions': 'RESTRICTED',
            'IncludeIframeOnlyStream': False,
            'PlaylistType': 'EVENT',
            'PlaylistWindowSeconds': 30,
            'ProgramDateTimeIntervalSeconds': 0,
            'SegmentDurationSeconds': 1,
            'StreamSelection': {
                'MaxVideoBitsPerSecond': 2147483647,
                'MinVideoBitsPerSecond': 0,
                'StreamOrder': 'ORIGINAL'
            },
            'UseAudioRenditionGroup': False
        },
        Id=transmission_id,
        ManifestName='index',
        Origination='ALLOW',
        Description=transmission_name,
        StartoverWindowSeconds=buffer_time_in_secs,
        Tags={
            'created_at': created_at,
            'transmission': transmission_id,
            'Name': transmission_name
        },
        TimeDelaySeconds=0
    )
    print('mediapackage_channel', channel)
    print('mediapackage_endpoint', endpoint)
    return endpoint['Url']

def create_medialive_channel(transmission_id, transmission_name, input_id, created_at):
    channel = medialive.create_channel(
        ChannelClass='STANDARD',
        Destinations=[{
            'Id': transmission_id,
            'MediaPackageSettings': [{'ChannelId': transmission_id}],
            'Settings': []
        }],
        EncoderSettings=get_encoder_settings(transmission_id),
        InputAttachments=[{
            'InputAttachmentName': transmission_id,
            'InputId': input_id,
            'InputSettings': {
                'AudioSelectors': [],
                'CaptionSelectors': [],
                'DeblockFilter': 'DISABLED',
                'DenoiseFilter': 'DISABLED',
                'FilterStrength': 1,
                'InputFilter': 'AUTO',
                'Smpte2038DataPreference': 'IGNORE',
                'SourceEndBehavior': 'CONTINUE'
            }
        }],
        InputSpecification={
            'Codec': 'AVC',
            'MaximumBitrate': 'MAX_10_MBPS',
            'Resolution': 'HD'
        },
        LogLevel='DISABLED',
        Name=transmission_name,
        RequestId=transmission_id,
        RoleArn=os.environ.get('MEDIALIVE_MEDIAPACKAGE_ROLE'),
        Tags={
            'created_at': created_at,
            'transmission': transmission_id,
            'Name': transmission_name
        }
    )

    print('medialive_channel', channel)
    return channel

def get_encoder_settings(transmission_id):
    return {
        'AudioDescriptions': [{
            'AudioSelectorName': 'default',
            'AudioTypeControl': 'FOLLOW_INPUT',
            'CodecSettings': {
                'AacSettings': {
                    'Bitrate': e['audio']['Bitrate'],
                    'RawFormat': 'NONE',
                    'Spec': 'MPEG4'
                }
            },
            'LanguageCodeControl': 'FOLLOW_INPUT',
            'Name': f'audio_{e["name"]}'
        } for e in content_outputs],
        'VideoDescriptions': [{
            'CodecSettings': {
                'H264Settings': { 
                    'AdaptiveQuantization': 'HIGH',
                    'Bitrate': e['video']['Bitrate'],
                    'ColorMetadata': 'INSERT',
                    'EntropyEncoding': 'CAVLC',
                    'FlickerAq': 'ENABLED',
                    'FramerateControl': 'SPECIFIED',
                    'FramerateDenominator': 1001,
                    'FramerateNumerator': e['video']['FramerateNumerator'],
                    'GopBReference': 'DISABLED',
                    'GopNumBFrames': e['video']['GopNumBFrames'],
                    'GopSize': e['video']['GopSize'],
                    'GopSizeUnits': 'FRAMES',
                    'Level': e['video']['Level'],
                    'LookAheadRateControl': 'HIGH',
                    'ParControl': 'SPECIFIED',
                    'Profile': e['video']['Profile'],
                    'RateControlMode': 'CBR',
                    'SceneChangeDetect': 'ENABLED',
                    'SpatialAq': 'ENABLED',
                    'Syntax': 'DEFAULT',
                    'TemporalAq': 'ENABLED'
                }
            },
            'Height': e['video']['Height'],
            'Name': f'video_{e["name"]}',
            'ScalingBehavior': 'DEFAULT',
            'Width': e['video']['Width']
        } for e in content_outputs],
        'CaptionDescriptions': [],
        'OutputGroups': [{
            'OutputGroupSettings': {
                'MediaPackageGroupSettings': {
                    'Destination': {'DestinationRefId': transmission_id}
                }
            },
            'Outputs': [{   
                'AudioDescriptionNames': [f'audio_{e["name"]}'],
                'CaptionDescriptionNames': [],
                'OutputName': f'{e["name"]}',
                'OutputSettings': { 'MediaPackageOutputSettings': {} },
                'VideoDescriptionName': f'video_{e["name"]}'
            } for e in content_outputs]
        }],
        'TimecodeConfig': {'Source': 'SYSTEMCLOCK'},
    }