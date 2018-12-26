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

	#endpoint_url = ''
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

def createNewUser (user):

# variables

	region = "eu-west-2"
	table = "previousSongs"
	endpoint = getEndpoint()

	#user = "richardx14-2" # need to look this up in future

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

createNewUser("user as input")
