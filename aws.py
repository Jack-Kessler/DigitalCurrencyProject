from sre_constants import SUCCESS
import boto3
import json
from custom_encoder import CustomEncoder
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'crypto_prices'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'

healthPath = '/health'
currencyPath = '/currency'
currenciesPath = '/currencies'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == currencyPath:
        response = getCurrency(event['queryStringParameters']['currencyId'])
    elif httpMethod == getMethod and path == currenciesPath:
        response = getCurrencies()
    elif httpMethod == postMethod and path == currencyPath:
        response = saveCurrency(json.loads(event['body']))
    else:
        response = buildResponse(404, 'Not Found')
    return response

def getCurrency(currencyId):
    try:
        response = table.get_item(
            Key={
                'currencyId' : currencyId
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'CurrencyId: %s not found' % currencyId})
    except:
        logger.exception('Error in get currency')

def getCurrencies():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'currencies': response           
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error in get all currencies')

def saveCurrency(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation' : 'SAVE',
            'Message': 'SUCCESS',
            'ITEM': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error with saving currency')

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' #Allows cross-region access
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
        #Since object we get from Dynamodb is in decimals and not supported by default JSON decoder, we need to explicitly cast this to float (which is supported)
    return response
