from Sock import sendMessage


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