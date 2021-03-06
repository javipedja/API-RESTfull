import json
import logging
import os
import time
import uuid

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translateAWS = boto3.client(service_name='translate',region_name='us-east-1',use_ssl=True)
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    # Detectamos idioma
    idiomasDetectados = comprehend.detect_dominant_language(Text = result['Item']['text'])
    idioma = sorted(idiomasDetectados['Languages'], key=lambda k: k['LanguageCode'])[0]['LanguageCode']
    
    # Traducimos
    translateText =  translateAWS.translate_text(Text=result['Item']['text'], SourceLanguageCode=idioma, TargetLanguageCode=event['pathParameters']['lang'])

    item = {
        'id': result['Item']['id'],
        'text': translateText.get('TranslatedText'),
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
