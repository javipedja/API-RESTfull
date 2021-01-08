import json
import logging
import os
import time
import uuid

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translateAWS = boto3.client(service_name='translate',region_name='us-east-1',use_ssl=True)


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    translateText =  translateAWS.translate_text(Text=result['Item']['text'], SourceLanguageCode='auto', TargetLanguageCode=event['pathParameters']['lang'])

    item = {
        'id': result['Item']['id'],
        'text': result.get('TranslatedText'),
        'checked': result['Item']['checked'],
        'createdAt': result['Item']['createdAt'],
        'updatedAt': result['Item']['updatedAt'],
    }

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=decimalencoder.DecimalEncoder)
        
    }

    return response
