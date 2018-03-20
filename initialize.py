from Sock import sendMessage
from testsettings import *


def checkSettings():
    if not OAUTH:
        f = open("testsettings.py","w+")
        f.write("HOST = \"irc.twitch.tv\"\n")
        f.write("PORT = 6667\n")
        f.write("IDENT = \"" + input("Bot Twitch Account: ") + "\"\n")
        f.write("PASS = \""+input("Bot Oauth Token: ")+"\"\n")
        f.write("CHANNEL = \"" + input("Twitch Channel: ") + "\"\n")
        f.write("CLIENTID = \"" + input("Bot Client ID: ") + "\"\n")
        f.write("OAUTH = \"" + input("Channel Oauth Token: ") + "\"\n")
        f.write("server_memreq = \"CAP REQ :twitch.tv/membership\"\n")
        f.write("server_tagreq = \"CAP REQ :twitch.tv/tags\"")


def joinRoom(s):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + s.recv(1024).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            Loading = loadingComplete(line)
    sendMessage(s, "Successfully joined Chat")


def loadingComplete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True