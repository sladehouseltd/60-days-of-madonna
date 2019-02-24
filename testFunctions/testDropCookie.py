from __future__ import print_function # Python 2/3 compatibility
from random import randint
import boto3
import json
import decimal
import string, random
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# https://aws.amazon.com/blogs/compute/simply-serverless-using-aws-lambda-to-expose-custom-cookies-with-api-gateway/

def id_generator(size=11, chars=string.ascii_uppercase + string.digits):
    
    return ''.join(random.choice(chars) for _ in range(size))

def lambda_handler(event, context):

    print("In lambda handler")

    cookie = id_generator().lower()

    print(cookie)

    #cookieString = "myCookie=t81e70kke29; domain=my.domain; expires=Wed, 01 Jan 2020 20:41:27 GMT;"

    # REALLY IMPORTANT - CHANGE DOMAIN NAME BELOW BEFORE USING

    cookieString = "myCookie=" + cookie + "; domain=8wb6c682uc.execute-api.eu-west-2.amazonaws.com; expires=Wed, 01 Jan 2020 20:41:27 GMT;"

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
				'user': "richardx14-20190101-2v4",
				'cookie': "cookie string"
			}

resp = (lambda_handler(testEvent,context="context"))

print(resp['body'])

