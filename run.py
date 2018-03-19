from Sock import *
from helperfunctions import getBits, addBits, getUser, getMessage
from initialize import joinRoom
from lineParser import commandCheck


def doChat():
    s = openSocket()
    joinRoom(s)
    readbuffer = ""
    while True:
        readbuffer = readbuffer + s.recv(1024).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            print(line)
            if "PING :tmi.twitch.tv" in line:
                sendServerMessage(s, "PONG :tmi.twitch.tv")
            if "PRIVMSG" in line:
                junk, msg = line.split('PRIVMSG', maxsplit=1)
                if 'bits=' in junk:
                    bits = getBits(junk)
                    pushups = addBits(bits)
                    sendMessage(s, "Sheppy now owes " + str(
                        pushups) + " pushups to the stream. Check https://goo.gl/IVhdnK for an incentive to put your bits towards.")
                user = getUser(junk)
                message = getMessage(msg)
                if message[0] == '!':
                    commandCheck(user, message, s)


if __name__ == '__main__':
    doChat()
