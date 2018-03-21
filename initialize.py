from Sock import sendMessage
from testsettings import *

# This checks whether the settings have been initialized yet
# If not it performs a loop to get valid settings parameters
# from the user.

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


#Reads data from the chat channel until finished with initial information

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

#Check to see if end of loading info reached for room
#If not, "loading" is not complete

def loadingComplete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True