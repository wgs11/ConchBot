from Sock import openSocket, sendServerMessage, sendMessage
from helperfunctions import getBits, addBits, getUser, getMessage
from initialize import joinRoom, checkSettings
from lineParser import commandCheck


def functionloop():
    checkSettings()
    doChat()


def doChat():
    s = openSocket()
    joinRoom(s)
    readbuffer = ""
    while True:
        readbuffer = readbuffer + s.recv(1024).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if "PING :tmi.twitch.tv" in line:
                sendServerMessage(s, line.replace("PING", "PONG"))
                print(line)
                print(line.replace("PING", "PONG"))
            if "PRIVMSG" in line:
                junk, msg = line.split('PRIVMSG', maxsplit=1)
                if 'bits=' in junk:
                    bits = getBits(junk)
                    pushups = addBits(bits)
                    sendMessage(s, "Sheppy now owes " + str(
                        pushups) + " pushups to the stream. Check https://goo.gl/IVhdnK for an incentive to put your bits towards.")
                user = getUser(junk)
                message = getMessage(msg)
                print(user + ": "+message)
                if message[0] == '!':
                    commandCheck(user, message, s)
