from __future__ import print_function # Python 2/3 compatibility
from random import randint
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# https://faragta.com/aws-api-gateway/pass-cookie-values-from-api-gateway.html

def lambda_handler(event, context):

    print("In lambda handler")

    #cookieString = "myCookie=t81e70kke29; domain=my.domain; expires=Wed, 19 Apr 2017 20:41:27 GMT;"
    
    receivedUserCookie = event['cookie']

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },

        "body": receivedUserCookie
    }
    
    return resp



testEvent = {
				'user': "richardx14-20190101-2v4",
				'cookie': "cookie string"
			}

resp = (lambda_handler(testEvent,context="context"))

print(resp['body'])

