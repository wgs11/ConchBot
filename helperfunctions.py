import codecs
import json
import math
import random
import re
import sys
import urllib.error
from configparser import ConfigParser
from pathlib import Path
from urllib.request import urlopen

from APIQueries import getGame, recordLookUp, printCategories
from Sock import sendMessage
from colorcommands import incrementcolor
from settings import CHANNEL
from timedmessage import start_timer, end_timer
from webCalls import doDonate


################MOD COMMANDS###################
#EACH OF THESE PERFORMS modCheck(user)
def addcom(user, words, s):
    config = ConfigParser()
    config.read('commands.ini', encoding='utf-8')
    if not modCheck(user):
        refuse(s)
    else:
        if len(words) < 3:
            sendMessage(s, "Please use format: !addcom [command] [message]")
        else:
            command = words[1]
            output = words[2]
            if not command[0] == '!':
                command = '!' + command
            if config.has_section(command):
                sendMessage(s, "Command Already Exists: Use !editcom to alter commands.")
            else:
                config.add_section(command)
                config.set(str(command), 'output_val', str(output))
                config.write(codecs.open('commands.ini', 'wb+', 'utf-8'))
                sendMessage(s, "Command Added")


def donate(user, words, s):
    if not modCheck(user):
        refuse(s)
    else:
        if len(words) < 3:
            sendMessage(s, "Make sure to format the command as !donate [amount] [category")
        else:
            amount = words[1]
            category = words[2].strip(' \t\n\r')
            incentiveCheck = ConfigParser()
            incentiveCheck.read('incentives.ini')
            if incentiveCheck.has_section(category):
                doDonate(amount, category)
                sendMessage(s, "The money has been moved to an offshore account. Don't call us, we won't call you.")
            else:
                sendMessage(s, "That's not a real incentive, guess again Pinocchio.")


def add(user, color, value, socket):
    if not modCheck(user):
        refuse(socket)
    else:
        if not helpInts(value):
            sendMessage(socket, "Please format the add command properly.")
        else:
            incrementcolor(color, value)


def deduct(user, value, socket):
    if not modCheck(user):
        refuse(socket)
    else:
        try:
            push = int(value)
            deductPush(socket, push)
        except ValueError:
            sendMessage(socket, "Please use a valid value.")


def timer(user, line, socket):
    if not modCheck(user):
        refuse(socket)
    else:
        words = line.split(maxsplit=3)
        if helpInts(words[2]):
            if len(words) > 3:
                start_timer(words[1], words[2], words[3], socket)
            else:
                print("Command needs an output message")


def stop(user, words, socket):
    if not modCheck(user):
        refuse(socket)
    else:
        if len(words) == 2:
            name = words[1]
            end_timer(name)


def addquote(user, words, socket):
    if not modCheck(user):
        refuse(socket)
    else:
        if len(words) > 1:
            quote = ""
            for word in words[1:]:
                quote = quote + word.strip() + " "
            quote = quote[:-1]
            addQuote(quote)
            sendMessage(socket, quote + " was added.")


def deletecommand(user, words, socket, config):
    if not modCheck(user):
        refuse(socket)
    else:
        if not len(words) == 2:
            sendMessage(socket, "Please use format: !delcom [command]")
        else:
            command = words[1]
            if not config.has_section(command):
                print("sigh")
            else:
                config.remove_section(command)
                with open('commands.ini', 'w') as configfile:
                    config.write(configfile)
                sendMessage(socket, "Command Deleted")


def addQuote(user, words, socket):
    if not modCheck(user):
        refuse(socket)
    else:
        quote = ""
        for word in words[1:]:
            quote = quote + word.strip() + " "
        quote = quote[:-1]
        addQuote(quote)
        sendMessage(socket, quote + " was added.")


######################################

################UTILITY FUNCTIONS###############
# These functions are part of commands that can
# be invoked by anyone.


def check(user, socket):
    userCheck = ConfigParser()
    userCheck.read('times.ini')
    section = str(user)
    if userCheck.has_section(section):
        time = userCheck.getint(section, 'time_val')
        hours, minutes = convert(time)
        sendMessage(socket, section + " has spent " + str(hours) + " hours and " + str(
            minutes) + " minutes here since Feb. 22, 2017.")
    else:
        print("problem with userCheck")


def wr(words,socket):
    game, id = getGame()
    if game:
        if len(words) > 1:
            category = ""
            for word in words[1:]:
                category = category + word.strip() + " "
            category = category[:-1]
            sendMessage(socket, recordLookUp(game, id, category))
        else:
            print(printCategories(game, id))  #
            sendMessage(socket, printCategories(game, id))


def randomQuote():
    lines = open('quotes.txt').read().splitlines()
    line = random.choice(lines)
    return line


def getRandomLine():
    lines = open('answers.txt').read().splitlines()
    line = random.choice(lines)
    return line


def convert(time):
    hours = math.floor(time / 60)
    minutes = time - (hours * 60)
    return hours,minutes


def helpInts(input):
    try:
        int(input)
        return True
    except ValueError:
        return False


def getUser(line):
    PATTERN = re.compile(r" :.+!")
    result = PATTERN.search(line).group(0)[2:-1]
    return str(result)


def getMessage(line):
    user, message = line.split(':',maxsplit=1)
    user = user.strip()[1:]
    return message


def getBits(junk):
    PATTERN = re.compile(r"bits=([1-9])([0-9])*")
    result = PATTERN.search(junk)
    if result:
        bits = result.group(0)
        return str(bits[5:])
    else:
        return 0


def addBits(bits):
    file = Path("bits.txt")
    current = 0
    if file.is_file():
        check = open(file,'r+')
        current = check.read()
        if not current:
            current = 0
        check.seek(0)
        check.truncate()
        current = int(current)+int(bits)
        pushups = math.floor(current/10)
        check.write(str(current))
        check.close()
        return pushups



def refuse(socket):
    sendMessage(socket, "Only mods can use this command.")


def modCheck(user):
    config = ConfigParser()
    config.read('mods.ini')
    if config.has_section(user):
        return True
    else:
        print("checking mods list")
        try:
            url = urlopen("http://tmi.twitch.tv/group/user/" + CHANNEL + "/chatters")
            chattersJson = json.loads(url.read())
            mods = chattersJson["chatters"]["moderators"]
            if user in mods:
                config.add_section(user)
                with open('mods.ini', 'w') as configfile:
                    config.write(configfile)
                return True
            else:
                return False
        except urllib.error.URLError as unhappy:
            print(unhappy)


def deductPush(s,push):
    file = Path("bits.txt")
    if file.is_file:
        check = open(file,'r+')
        save = current = check.read()
        if not current:
            current = 0
        else:
            check.seek(0)
            check.truncate()
            current = int(current) - (int(push) * 10)
            if current < 0:
                sendMessage(s, "That's more than he owed, guess he did extra but we're at 0 now.")
                current = 0
            else:
                sendMessage(s, "Sheppy now has "+str(math.floor(current/10))+" pushups to do.")
            check.write(str(current))
            check.close()


def getPushups():
    file = Path("bits.txt")
    if file.is_file:
        check = open(file,'r')
        pushups = check.read()
        return str(math.floor(int(pushups)/10))
    else:
        return "There has been a problem."


def exit_program():
    sys.exit(0)
