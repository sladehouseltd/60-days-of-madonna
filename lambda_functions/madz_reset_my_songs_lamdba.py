
from __future__ import print_function # Python 2/3 compatibility
from random import randint
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

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
	endpoint_url = "http://127.0.0.1:8000"

	return(endpoint_url)

def setUpDB(region, endpoint=''):

	endpoint = getEndpoint()

	if(endpoint):
		dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint)
	else:
		dynamodb = boto3.resource('dynamodb', region_name=region)

	return(dynamodb)


def resetMySongs(user):

# variables

	region = "eu-west-2"
	table = "previousSongs"
	endpoint = getEndpoint()

	dynamodb = setUpDB(region, endpoint)

	table = dynamodb.Table(table)

	response = table.delete_item(
		Key={
			'userID': user,
		}
	)

	print(json.dumps(response, indent=4, cls=DecimalEncoder))

	print("Reset my songs succeeded:")

def lambda_handler(event, context):

    print("In lambda handler")

    resetMySongs(event['user'])
    
    respMessage = "User " + event['user'] + " reset"

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "https://60daysofmadonna.com",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Credentials": "true"
        },
        "body": respMessage
    }
    
    return resp

# print(getMyDayCount("richardx14-20181226v1"))

testEvent = {
				'user': "richardx14-20190101sdasda"
			}

resp = (lambda_handler(testEvent,context="context"))

print(resp['body'])
