from APIQueries import followTime, upTime
from helperfunctions import *


# commandCheck parses the message portion of each line
# Each command here is not a simple text response, but
# instead requires either calculation, data fetching
# or file manipulation. The check at the end handles
# commands that *are* simple text responses, these can
# be added/removed with the !addcom/!delcom commands
# and will be included in the !commands list

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
    elif command == "!songrequest":
        print("do nothing")
    elif command == "!sr":
        print("do nothing")
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
            sendMessage(s,  getRandomLine())
    elif command == "!following":
        time = str(followTime(user))
        if len(time) < 1:
            sendMessage(s, user + " doesn't follow the channel.")
        else:
            sendMessage(s, user + " has been following for " + str(time))
    elif command == "!commands":
        output = "Channel Commands: "
        for command in config.sections():
            output = output + str(command) + " "
        sendMessage(s, output)
    elif config.has_section(command):
        output = config.get(command, 'output_val')
        sendMessage(s, str(output))
    else:
        sendMessage(s, "Command does not exist.")
    return
