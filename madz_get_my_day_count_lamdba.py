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
        #print("GetItem succeeded:")
        #print(json.dumps(item, indent=4, cls=DecimalEncoder))

    return(response)

def getMyDayCount(user):

# variables

	region = "eu-west-2"
	table = "previousSongs"
	endpoint = getEndpoint()

	dynamodb = setUpDB(region, endpoint)

	dayCount = getItem(table, region, user, endpoint)['Item']['dayCount']

	print("get my day count succeeded:")

	return(str(dayCount))

def lambda_handler(event, context):

    print("In lambda handler")

    dayCount = getMyDayCount(event['user'])
    
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": dayCount
    }
    
    return resp

# print(getMyDayCount("richardx14-20181226v1"))

#testEvent = {
#				'user': "richardx14-20181226v1"
#			}

#resp = (lambda_handler(testEvent,context="context"))

#print(resp['body'])
