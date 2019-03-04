from __future__ import print_function # Python 2/3 compatibility
from random import randint
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import string, random
import os

maxDayCount = 60

globalRegion = "eu-west-2"
globalTable = "previousSongs"
globalUserItem = {}
globalDynamodb = {}

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

def setUpDB(region, endpoint=''):

    global globalDynamodb

    global globalEndpoint_url

    endpoint = os.getenv("ENV")

    if endpoint == "aws":
        globalEndpoint_url = ''
        print("Running in AWS")
    else:
        globalEndpoint_url = "http://127.0.0.1:8000"
        print("Running locally")

    if(globalEndpoint_url):
        globalDynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=globalEndpoint_url)
    else:
        globalDynamodb = boto3.resource('dynamodb', region_name=region)


def createSongList():

    songs = [
    "4 Minutes",
    "Act of Contrition",
    "The Actress Hasn't Learned the Lines (You'd Like to Hear)",
    "Addicted",
    "Ain't No Big Deal",
    "Amazing",
    "American Life",
    "American Pie",
    "Angel",
    "Another Suitcase in Another Hall",
    "Auto-Tune Baby",
    "B-Day Song",
    "Back in Business",
    "Bad Girl",
    "Be Careful (Cuidado Con Mi Corazn)",
    "The Beast Within",
    "Beat Goes On",
    "Beautiful Killer",
    "Beautiful Scars",
    "Beautiful Stranger",
    "Bedtime Story",
    "Best Friend",
    "Best Night",
    "Bitch I'm Madonna",
    "Bittersweet",
    "Body Shop",
    "Borderline",
    "Born to Be Alive",
    "Borrowed Time",
    "Broken",
    "Buenos Aires",
    "Burning Up",
    "Bye Bye Baby",
    "Candy Perfume Girl",
    "Candy Shop",
    "Can't Stop",
    "Causing a Commotion",
    "Celebration",
    "Champagne Rose",
    "Charity Concert / The Art of the Possible",
    "Cherish",
    "Crazy for You",
    "Crimes of Passion",
    "Cry Baby",
    "Cyber-Raga",
    "Dance 2Night",
    "Dear Jessie",
    "Deeper and Deeper",
    "Devil Pray",
    "Devil Wouldn't Recognise You",
    "Did You Do It?",
    "Die Another Day",
    "Don't Cry for Me Argentina",
    "Don't Stop",
    "Don't Tell Me",
    "Don't You Know",
    "Dress You Up",
    "Drowned World/Substitute for Love",
    "Each Time You Break My Heart",
    "Easy Ride",
    "Erotica",
    "Eva and Magaldi / Eva Beware of the City",
    "Eva's Final Broadcast",
    "Everybody",
    "Express Yourself",
    "Falling Free",
    "Fever",
    "Fighting Spirit",
    "Forbidden Love",
    "Freedom",
    "Frozen",
    "Future Lovers",
    "Gambler",
    "Gang Bang",
    "Get Together",
    "Get Over",
    "Ghosttown",
    "Girl Gone Wild",
    "Give It 2 Me",
    "Give Me All Your Luvin'",
    "Gone",
    "Goodbye to Innocence",
    "Goodnight and Thank You",
    "Graffiti Heart",
    "Guilty by Association",
    "Hanky Panky",
    "Has to Be",
    "Heartbeat",
    "HeartBreakCity",
    "He's a Man",
    "Hello and Goodbye",
    "Hey You",
    "High Flying, Adored",
    "History",
    "Hold Tight",
    "Holiday",
    "Hollywood",
    "Holy Water",
    "How High",
    "Human Nature",
    "Hung Up",
    "I Deserve It",
    "I Don't Give A",
    "I Fucked Up",
    "I Know It",
    "I Love New York",
    "I Want You",
    "I'd Be Surprisingly Good for You",
    "I'd Rather Be Your Lover",
    "I'll Remember",
    "I'm a Sinner",
    "I'm Addicted",
    "I'm Going Bananas",
    "I'm So Stupid",
    "Iconic",
    "If You Forget Me",
    "Illuminati",
    "Imagine",
    "Impressive Instant",
    "In This Life",
    "Incredible",
    "Inside of Me",
    "Inside Out",
    "Intervention",
    "Into the Groove",
    "Into the Hollywood Groove",
    "Isaac",
    "It's So Cool",
    "Jimmy Jimmy",
    "Joan of Arc",
    "Jump",
    "Just a Dream",
    "Justify My Love",
    "Keep It Together",
    "La Isla Bonita",
    "La Vie en rose",
    "Lament",
    "Laugh to Keep from Crying",
    "Let Down Your Guard",
    "Let It Will Be",
    "Like a Prayer",
    "Like a Virgin",
    "Like It or Not",
    "Little Star",
    "Live to Tell",
    "Living for Love",
    "Lo Que Siente La Mujer",
    "The Look of Love",
    "Love Don't Live Here Anymore",
    "Love Makes the World Go Round",
    "Love Profusion",
    "Love Song",
    "Love Spent",
    "Love Tried to Welcome Me",
    "Lucky Star",
    "Masterpiece",
    "Material Girl",
    "Me Against the Music",
    "Mer Girl",
    "Messiah",
    "Miles Away",
    "More",
    "Mother and Father",
    "Music",
    "A New Argentina",
    "Nobody Knows Me",
    "Nobody's Perfect",
    "Nothing Fails",
    "Nothing Really Matters",
    "Now I'm Following You",
    "Oh Father",
    "Oh What a Circus",
    "On the Balcony of the Casa Rosada (Part 2)",
    "One More Chance",
    "Open Your Heart",
    "Over and Over",
    "Papa Don't Preach",
    "Paradise (Not for Me)",
    "Partido Feminista",
    "Peron's Latest Flame",
    "Physical Attraction",
    "The Power of Good-Bye",
    "Pretender",
    "Promise to Try",
    "Promises, Promises",
    "Push",
    "Rain",
    "Rainbow High",
    "Rainbow Tour",
    "Ray of Light",
    "Rebel Heart",
    "Rescue Me",
    "Revolver",
    "Ring My Bell",
    "Runaway Lover",
    "S.E.X.",
    "Sanctuary",
    "Santa Baby",
    "Secret",
    "Secret Garden",
    "Shanti/Ashtangi",
    "She's Not Me",
    "Shoo-Bee-Doo",
    "Sidewalk Talk",
    "Sing",
    "Skin",
    "Sky Fits Heaven",
    "Some Girls",
    "Something to Remember",
    "Sooner or Later",
    "Sorry",
    "Spanish Eyes",
    "Spanish Lesson",
    "Spotlight",
    "Stay",
    "Supernatural",
    "Superstar",
    "Super Pop",
    "Survival",
    "Swim",
    "Take a Bow",
    "Tell Me",
    "Thief of Hearts",
    "Think of Me",
    "This Used to Be My Playground",
    "Till Death Do Us Part",
    "Time Stood Still",
    "To Have and Not to Hold",
    "True Blue",
    "Turn Up the Radio",
    "Unapologetic Bitch",
    "Up Down Suite",
    "Veni Vidi Vici",
    "Veras",
    "Voices",
    "Vogue",
    "Waiting",
    "Waltz for Eva and Che",
    "Wash All Over Me",
    "What Can You Lose",
    "What It Feels Like for a Girl",
    "Where Life Begins",
    "Where's the Party?",
    "White Heat",
    "Who's That Girl",
    "Why's It So Hard",
    "Words",
    "X-Static Process",
    "You Must Love Me",
    "You'll See",
    "Your Honesty",
    "Your Little Body's Slowly Breaking Down"]

    return(songs)




def getASong(user):

    print("Getting a song.")

    songSoFar = globalUserItem['Item']['songSoFar']

    dayCount = globalUserItem['Item']['dayCount']

    songList = createSongList()

    for song in songSoFar:
        songList.remove(song)

    foo2 = randint(0,len(songList)-1 )
    songOfTheDay = songList[foo2]
    print("Song of the day is " + songOfTheDay + ".")

    dayCount = globalUserItem['Item']['dayCount'] + 1

    globalUserItem['Item']['dayCount'] +=1

    songSoFar.append(songOfTheDay)

    table = globalDynamodb.Table(globalTable)

    response = table.put_item(
        Item={
            'userID': user,
            'dayCount': globalUserItem['Item']['dayCount'],
            'songSoFar': songSoFar
            }
        )
        
    return(songOfTheDay)

def getItem(table, region, userID, endpoint = ''):

    table = globalDynamodb.Table(globalTable)

    try:
        response = table.get_item(
            Key={
                'userID': userID
            }
        )
    except ClientError as e:
        print("Cookie supplied but not found.")
        print(e.response['Error']['Message'])

    else:
        item = response['Item']

        #print(json.dumps(item, indent=4, cls=DecimalEncoder))

    return(response)


def createNewUser(user):

    print("Creating new user " + user + " in get_a_song")

    table = globalDynamodb.Table(globalTable)

    response = table.put_item(
        Item={
            'userID': user,
            'dayCount': 0,
            'songSoFar': []
            }
        )

def formatAllSongsForUserString():

    allSongsForUser = globalUserItem['Item']['songSoFar']

    allSongsForUserString = ""
    
    for song in allSongsForUser:
        allSongsForUserString = allSongsForUserString + song + ", "

    allSongsForUserString = allSongsForUserString[:-2] # strip off final comma and space

    print("get all my songs succeeded:")

    return(allSongsForUserString)


def lambda_handler(event, context):

    print("In lambda handler")

    if maxDayCount != 60:
        print("WARNING!!! maxDayCount is set to " + str(maxDayCount) )

    setUpDB(globalRegion)

    receivedUserCookie = event['cookie']

    print("received user cookie: " + receivedUserCookie)

    if receivedUserCookie == '':

        receivedUserCookie = "No cookie received, creating cookie and user"
        userCookie = id_generator().lower()
        createNewUser(userCookie)
    
    else:

        userCookie = receivedUserCookie.replace('=',';')
        userCookie = userCookie.split(';')[1]
        userCookie = userCookie.lstrip()
        #print(userCookie)

    userCookieString = "madzCookie=" + userCookie +"; domain=60daysofmadonna.com; expires=Wed, 19 Apr 2020 20:41:27 GMT;"

    global globalUserItem

    try:
        globalUserItem = getItem(globalTable, globalRegion, userCookie, globalEndpoint_url)
    except:
        print("Received cookie, but user not found.  Creating new user with received cookie.")
        createNewUser(userCookie)
        globalUserItem = getItem(globalTable, globalRegion, userCookie, globalEndpoint_url)

    allSongsForUser = formatAllSongsForUserString()

    if globalUserItem['Item']['dayCount'] < maxDayCount:

        newSong = getASong(userCookie)

    else:

        newSong = "You now have all " + str(maxDayCount) + " songs!"

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "song": newSong,
        "allSongsForUser": allSongsForUser,
        "dayCount": globalUserItem['Item']['dayCount'], 
        "droppedUserCookie": userCookie,
        "receivedUserCookie": receivedUserCookie,
        "Cookie": userCookieString
    }
    
    return resp

####################

testEvent = {
                'user': "richardx14-1",
                'cookie': "; kx1q0n64ytq2"
            }

resp = (lambda_handler(testEvent,context="context"))


print(resp['song'])

print(resp['allSongsForUser'])

print(resp['dayCount'])

#                'cookie': "; p9m5ptd1dr5"

