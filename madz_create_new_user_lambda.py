from __future__ import print_function # Python 2/3 compatibility
from random import randint
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import string, random

# https://aws.amazon.com/blogs/compute/simply-serverless-using-aws-lambda-to-expose-custom-cookies-with-api-gateway/

def id_generator(size=11, chars=string.ascii_uppercase + string.digits):
    
    return ''.join(random.choice(chars) for _ in range(size))

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def getEndpoint():

	endpoint_url = ''
	#endpoint_url = "http://localhost:8000"
	endpoint_url = "http://127.0.0.1:8000"

	return(endpoint_url)

def setUpDB(region, endpoint=''):

	endpoint = getEndpoint()

	if(endpoint):
		dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint)
	else:
		dynamodb = boto3.resource('dynamodb', region_name=region)

	return(dynamodb)

def getItem(table, region, userID, endpoint = ''):

    if(endpoint):
        dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint)
    else:
        dynamodb = boto3.resource('dynamodb', region_name=region)

    table = dynamodb.Table(table)

    try:
        response = table.get_item(
            Key={
                'userID': userID
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']

    return(response)

def createNewUser (user):

	region = "eu-west-2"
	table = "previousSongs"
	endpoint = getEndpoint()

	dynamodb = setUpDB(region, endpoint)

	table = dynamodb.Table(table)

	response = table.put_item(
		Item={
			'userID': user,
			'dayCount': 0,
			'songSoFar': []
			}
		)

	print("Create user " + user + " succeeded.")

	return(response)


def lambda_handler(event, context):

    print("In lambda handler")

    cookie = id_generator().lower()

    print(cookie)

    newUser = createNewUser(cookie)
    
    cookieString = "madzCookie=" + cookie + "; domain=8wb6c682uc.execute-api.eu-west-2.amazonaws.com; expires=Wed, 01 Jan 2020 20:41:27 GMT;"

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "Cookie": cookieString,
        "body": cookieString
    }
    
    return resp


testEvent = {
				'user': "richardx14-1",
                'cookie': "; Cookie=richardx14-1"
			}

resp = (lambda_handler(testEvent,context="context"))

print(resp['body'])
