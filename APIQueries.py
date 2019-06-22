import json
import math
import urllib.error
import urllib.parse
from configparser import ConfigParser
from datetime import datetime
from urllib.request import urlopen, Request
from settings import CLIENTID, CHANNEL


def followTime(user):
    print(user)
    alturl = 'https://api.twitch.tv/helix/users?login='+user+'&login='+CHANNEL
    r = Request(alturl)
    r.add_header('Client-ID',CLIENTID)
    try:
        a = urlopen(r)
        streamjson = json.loads(a.read())['data']
        print(streamjson)
        uid1 = streamjson[0]['id']
        uid2 = streamjson[1]['id']
        print(uid1, uid2)
        followurl = 'https://api.twitch.tv/helix/users/follows?from_id='+uid1+'&to_id='+uid2
        s = Request(followurl)
        s.add_header('Client-ID',CLIENTID)
        try:
            b = urlopen(s)
            stuff = json.loads(b.read())

            stuff = stuff['data'][0]['followed_at']
            followed_at = datetime.strptime(stuff, '%Y-%m-%dT%H:%M:%SZ')
            now = datetime.utcnow()
            timedelta = now - followed_at
            timedelta = str(timedelta)[:-7]
            return timedelta
        except urllib.error.HTTPError as error:
            data = error.read()
            print(data)
            return
    except urllib.error.HTTPError as error:
        data = error.read()
        print(data)
        print(user+" doesn't follow the channel.")
    return


def getRecord(catid):
    caturl = 'http://www.speedrun.com/api/v1/categories/'+catid+'/records'
    try:
        catRequest = Request(caturl)
        catOpen = urlopen(catRequest)
        catJson = json.loads(catOpen.read())
        thing = catJson['data'][0]
        if thing.get('runs'):
            player = catJson['data'][0]['runs'][0]['run']['players'][0]['name']
            igt = catJson['data'][0]['runs'][0]['run']['times']['ingame_t']
            if not igt == 0:
                record = translate(igt)
            else:
                time = catJson['data'][0]['runs'][0]['run']['times']['realtime_t']
                record = translate(time)
            return(record, player)
        else:
            print("No runs for that category.")
            record = ''
            player = ''
            return (record, player)
    except urllib.error.HTTPError as error:
        data = error.read()
        print(data)


def lookUpUser(id):
    userURL = 'http://www.speedrun.com/api/v1/users/'+id
    try:
        userRequest = Request(userURL)
        userOpen = urlopen(userRequest)
        userJson = json.loads(userOpen.read())
        return userJson['data']['names']['international']
    except urllib.error.HTTPError as error:
        data = error.read()
        print(data)


def translate(time):
    print(time)
    hours = math.floor(time/3600)
    minutes = math.floor((time - (hours * 3600))/60)
    seconds = "{0:.2f}".format(time - (minutes * 60) - (hours * 3600))
    print(hours,minutes,seconds)
    return "%s:%s:%s" %(hours, minutes, seconds)


def printCategories(game, id):
    config = ConfigParser()
    config.read('games.ini')
    message = "Please use !wr [category] with: "

    if config.has_section(game):
        if len(config.items(game)) == 1:
            getRecords(game,id)
            config.read('games.ini')
        for item in config.items(game)[1:]:
            message = message + item[0]+" | "
    return message


def recordLookUp(game,id,category):
    config = ConfigParser()
    config.read('games.ini')
    if config.has_option(game,category):
        cat = config.get(game,category)
        record, player = getRecord(cat)
        return "WR is " + record + " by "+ player
    else:
        getRecords(game,id)
        config.read('games.ini')
        if config.has_option(game,category):
            cat = config.get(game, category)
            record, player = getRecord(cat)
            if not record:
                return("There is no record for that category.")
            else:
                return "WR is " + record + " by " + player
        else:
            print("it really doesn't exist right now")
    return


def getRecords(game,id):
    config = ConfigParser()
    config.read('games.ini')
    stuff = config.items(game)
    try:
        surl = 'http://www.speedrun.com/api/v1/games/' + id + '/categories?miscellaneous=no'
        getsurl = Request(surl)
        opensurl = urlopen(getsurl)
        srjson = json.loads(opensurl.read())
        categories = srjson['data']
        for id in categories:
            cat = id['id']
            name = id['name']
            if not config.has_option(game,name):
                config.set(game,name,cat)
#            print(id['id'], id['name'])
        with open('games.ini', 'w') as configfile:
            config.write(configfile)
    except urllib.error.HTTPError as error:
        data = error.read()
        print(data)

def getGame():
    game = False
    id = False
    myurl = 'https://api.twitch.tv/kraken/streams/'+CHANNEL
    r = Request(myurl)
    r.add_header('Client-ID', CLIENTID)
    a = urlopen(r)
    streamjson = json.loads(a.read())
    if streamjson['stream']:
        game = streamjson['stream']['game']
        config = ConfigParser()
        config.read('games.ini')
        if config.has_section(game):
            id = config.get(game,'id')
        else:
            print("we need to load the game from the api or be lazy")
    else:
        ("Stream is offline")
    return game,id

# try:
#     for i in range(0, 10000, 1000):
#         baseurl = 'http://www.speedrun.com/api/v1/games?_bulk=yes&max=9000&offset=' + str(i)
#         sr = Request(baseurl)
#         b = urlopen(sr)
#         srjson = json.loads(b.read())
#         if not srjson['data'] is None:
#             ids = srjson['data']
#             for game in ids:
#                 section = game['names']['international']
#                 config.add_section(section)
#                 config.set(section, 'id', game['id'])
#             with open('games.ini', 'w') as configfile:
#                 config.write(configfile)
# except urllib.error.HTTPError as error:
#     data = error.read()
#     print(data)


def checkLive():
    url = 'https://api.twitch.tv/helix/streams/' + CHANNEL
    r = Request(url)
    r.add_header('Client-ID', CLIENTID)
    try:
        a = urlopen(r)
        streamjson = json.loads(a.read())
        stream = streamjson['stream']
        if stream is None:
            return False
        else:
            return True
    except urllib.error.HTTPError as error:
        data = error.read()


def upTime():
    url = 'https://api.twitch.tv/kraken/streams/'+CHANNEL
    r = Request(url)
    r.add_header('Client-ID', CLIENTID)
    message = ""
    try:
        a = urlopen(r)
        streamjson = json.loads(a.read())
        stream = streamjson['stream']
        if stream is None:
            message = "Stream is Offline."
        else:
            start = stream['created_at']
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
            now = datetime.utcnow()
            timedelta = now - start
            message = "Stream has been live for "+str(timedelta)[:-7]
    except urllib.error.HTTPError as error:
        data = error.read()
    return message

