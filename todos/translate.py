import json
import logging
import os
import time
import uuid

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translateAWS = boto3.client(service_name='translate',region='us-east-1',use_ssl=True)


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    result["Item"]["text"] =  translateAWS.translate_text(Text=result["Item"]["text"], SourceLanguageCode="es", TargetLanguageCode=event['pathParameters']['lang'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
        
    }

    return response
