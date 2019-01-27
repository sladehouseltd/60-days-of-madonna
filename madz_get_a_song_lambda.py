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

def createSongList():

    songs = [
    "4 Minutes",
    "American Life",
    "B-Day Song",
    "Bad Girl",
    "Beat Goes On",
    "Beautiful Killer",
    "Beautiful Stranger",
    "Bedtime Story",
    "Best Friend",
    "Bitch I'm Madonna",
    "Body Shop",
    "Borderline",
    "Burning Up",
    "Candy Store",
    "Celebration",
    "Cherish",
    "Crazy For You",
    "Dance Tonight",
    "Dear Jessie",
    "Deeper and Deeper",
    "Devil Pray",
    "Devil Wouldn't Recognize You",
    "Die Another Day",
    "Don't Tell Me",
    "Dress You Up",
    "Erotica",
    "Everybody",
    "Express Yourself",
    "Falling Free",
    "Frozen",
    "Future Lovers",
    "Gang Bang",
    "Get Together",
    "Ghosttown",
    "Girl Gone Wild",
    "Give it 2 Me",
    "Give Me All Your Luvin'",
    "Holiday",
    "Holy Water",
    "Human Nature",
    "Hung Up",
    "I Don't Give A",
    "I Fu--ed Up",
    "I Love New York",
    "I'll Remember",
    "I'm a Sinner",
    "I'm Addicted",
    "Iconic",
    "Illuminati",
    "Incredible",
    "Into The Groove",
    "Joan Of Arc",
    "Justify My Love",
    "La Isla Bonita",
    "Like A Prayer",
    "Like A Virgin",
    "Live To Tell",
    "Living For Love",
    "Love Song",
    "Love Spent",
    "Lucky Star",
    "Masterpiece",
    "Material Girl",
    "Miles Away",
    "Mother and Father",
    "Music",
    "Nothing Really Matters",
    "Oh, Father",
    "One More Chance",
    "Open Your Heart",
    "Papa Don't Preach",
    "Promise To Try",
    "Rain",
    "Ray Of Light",
    "Rebel Heart",
    "Rescue Me",
    "Revolver",
    "She's Not Me",
    "Some Girls",
    "Spanish Lessons",
    "Substitute For Love",
    "Superstar",
    "Take A Bow",
    "The Power Of Goodbye",
    "This Used To Be My Playground",
    "True Blue",
    "Turn Up the Radio",
    "Unapologetic Bitch",
    "Veni Vidi Vici",
    "Vogue",
    "Voices",
    "Wash All Over Me",
    "What It Feels Like For A Girl",
    "Who's That Girl",
    "You'll See"]

    return(songs)

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

def getASong(user):

    print("Getting a song.")

    region = "eu-west-2"
    table = "previousSongs"

    endpoint = getEndpoint()

    #userID = "richardx14-1" # need to look this up in future

    dynamodb = setUpDB(region, endpoint)

    songList = createSongList()

    songSoFar = getItem(table, region, user, endpoint)['Item']['songSoFar']

    for song in songSoFar:
        songList.remove(song)

    if songList:
        foo2 = randint(0,len(songList)-1 )
        songOfTheDay = songList[foo2]
        print("Song of the day is " + songOfTheDay + ".")

        # write to db.

        addASongToSongsSoFar(user, songOfTheDay)

        #putItem("madonnaSongs", "eu-west-2", "richardx14-3", "http://localhost:8000")
        
        return(songOfTheDay)

    else:
        return ("Madonna has run out of songs!")

def addASongToSongsSoFar(user, song):

# variables

    region = "eu-west-2"
    table = "previousSongs"
    endpoint = getEndpoint()

    #userID = "richardx14-1" # need to look this up in future

    dynamodb = setUpDB(region, endpoint)

    # sort out songs

    songs = getItem(table, region, user, endpoint)['Item']['songSoFar']

    songs.append(song)

    # sort out dayCount

    dayCount = getItem(table, region, user, endpoint)['Item']['dayCount'] + 1

    # now put item back

    table = dynamodb.Table(table)

    response = table.put_item(
        Item={
            'userID': user,
            'dayCount': dayCount,
            'songSoFar': songs
            }
        )

    #print("addASong succeeded:")

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


def lambda_handler(event, context):

    print("In lambda handler")

    cookie = event['cookie']
    
    print(cookie)

    userCookie = (cookie.split('=')[1])

    print(userCookie)

    newSong = getASong(userCookie)

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": newSong,
        "userCookie": userCookie

    }
    
    return resp

testEvent = {
                'user': "richardx14-1",
                'cookie': "; Cookie=richardx14-1"
            }

resp = (lambda_handler(testEvent,context="context"))

print(resp['body'])

