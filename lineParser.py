from APIQueries import followTime, upTime
from helperfunctions import *  # (modCheck, helpInts, randomQuote, getPushups, addQuote, deductPush, convert, getRandomLine, addcom, add, deduct, timer, stop, addquote, delete


def commandCheck(user, line, s):
    config = ConfigParser()
    config.read('commands.ini', encoding='utf-8')
    words = line.split(maxsplit=2)
    command = words[0]
    if command == "!addcom":
        addcom(user, words, s)
    elif command == "!add":
        if len(words) == 3:
            color = words[1]
            value = words[2]
            add(user, color, value, s)
    elif command == "!donate":
        donate(user, words, s)
    elif command == "!deduct":
        if len(words) == 2:
            value = int(words[1])
            deduct(user, value, s)
    elif command == "!pushups":
        sendMessage(s, "Sheppy owes " + getPushups() + " pushups.")
    elif command == "!quote":
        quote = randomQuote()
        sendMessage(s, quote)
    elif command == "!timer":
        timer(user, line, s)
    elif command == "!stop":
        stop(user, words, s)
    elif command == "!addquote":
        addquote(user, words, s)
    elif command == "!delcom":
        deletecommand(user, words, s, config)
    elif command == "!check":
        check(user, s)
    elif command == "!uptime":
        time = upTime()
        sendMessage(s, time)
    elif command == "!wr":
        wr(words, s)
    elif command == "!conch":
        if len(words) == 1:
            sendMessage(s, "You gonna ask me something or just say my name cus you like how it sounds?")
        else:
            line = getRandomLine()
            sendMessage(s, line)
    elif command == "!following":
        time = str(followTime(user))
        time = time[:-7]
        if len(time) < 1:
            sendMessage(s, user + " doesn't follow the channel.")
        else:
            sendMessage(s, user + " has been following for " + str(time))
    elif command == "!commands":
        output = "Channel Commands: "
        for command in config.sections():
            output = output + str(command) + " "
        sendMessage(s, output)
    else:
        command = str(words[0])
        if config.has_section(command):
            output = config.get(command, 'output_val')
            sendMessage(s, str(output))
        else:
            print("Command does not exist.")
    return
