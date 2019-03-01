from __future__ import print_function # Python 2/3 compatibility
from random import randint
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import string, random


globalRegion = "eu-west-2"
globalTable = "previousSongs"

globalEndpoint_url = ''
globalEndpoint_url = "http://127.0.0.1:8000"

#global_user_item

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
    endpoint_url = "http://127.0.0.1:8000"

    return(endpoint_url)

def setUpDB(region, endpoint=''):

    #endpoint = getEndpoint()

    if(globalEndpoint_url):
        dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=globalEndpoint_url)
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

        #print(json.dumps(item, indent=4, cls=DecimalEncoder))

    return(response)


def getAllSongsForUser(user):
    
    dynamodb = setUpDB(globalRegion, globalEndpoint_url)

    allSongsForUser = getItem(globalTable, globalRegion, user, globalEndpoint_url)['Item']['songSoFar']

    allSongsForUserString = ""
    
    for song in allSongsForUser:
        allSongsForUserString = allSongsForUserString + song + ", "

    allSongsForUserString = allSongsForUserString[:-2] # strip off final comma and space

    print("get all my songs succeeded:")

    return(allSongsForUserString)




def lambda_handler(event, context):

    print("In lambda handler")
    
    receivedUserCookie = event['cookie']

    print("received user cookie: " + receivedUserCookie)

    if receivedUserCookie == '':

        receivedUserCookie = "No cookie received, creating cookie and user"
        userCookie = id_generator().lower()
        createNewUser(userCookie)
        userCookieString = "madzCookie=" + userCookie +"; domain=60daysofmadonna.com; expires=Wed, 19 Apr 2020 20:41:27 GMT;"
    
    else:

        userCookie = receivedUserCookie.replace('=',';')
        userCookie = userCookie.split(';')[1]
        userCookie = userCookie.lstrip()
        userCookieString = "madzCookie=" + userCookie +"; domain=60daysofmadonna.com; expires=Wed, 19 Apr 2020 20:41:27 GMT;"
        print(userCookie)

    allSongsForUser = getAllSongsForUser(userCookie)

    dynamodb = setUpDB(globalRegion, globalEndpoint_url)

    user_item = getItem(globalTable, globalRegion, userCookie, globalEndpoint_url)

    table = dynamodb.Table(globalTable)

    try:
        response = table.get_item(
            Key={
                'userID': userCookie
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']


    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "allSongsForUser": allSongsForUser,
        "droppedUserCookie": userCookie,
        "receivedUserCookie": receivedUserCookie,
        "Cookie": userCookieString,
        "user_item": user_item,
        "response": response
    }
    
    return resp

####################

testEvent = {
                'user': "richardx14-1",
                'cookie': "; p9m5ptd1dr5"
            }

resp = (lambda_handler(testEvent,context="context"))


print(resp['allSongsForUser'])

print(resp['response'])


