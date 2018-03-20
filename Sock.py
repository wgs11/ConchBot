import socket

from settings import *



def openSocket():
    s = socket.socket()
    s.connect((HOST,PORT))
    s.send(("PASS " + PASS + "\r\n").encode('utf-8'))
    s.send(("NICK " + IDENT + "\r\n").encode('utf-8'))
    sendServerMessage(s, server_memreq)
    sendServerMessage(s, server_tagreq)
    s.send(("JOIN #" + CHANNEL + "\r\n").encode('utf-8'))

    return s

def closeSocket(socket, channel):
    socket.send(("PART #"+channel+"\r\n").encode('utf-8'))
    socket.close()
    print("Disconnected from Chat")

def sendMessage(s, message):
    print(message)
    messageTemp = "PRIVMSG #sheppy" + " :" + message+"\r\n"
    s.send(messageTemp.encode('utf-8'))


def sendServerMessage(s, message):
    message = message+"\r\n"
    s.send(message.encode('utf-8'))

