from configparser import ConfigParser
from threading import Timer

from Sock import sendMessage


def start_timer(name, interval, message, socket):
    config = ConfigParser()
    config.read('timers.ini')
    if not config.has_section(name):
        config.add_section(name)
        config.set(name,"interval",str(interval))
        config.set(name,"message",str(message))
        with open('timers.ini', 'w') as configfile:
            config.write(configfile)
        t = Timer(int(interval), timed_message,[name, socket])
        t.start()
    else:
        print("Timer already exists.")

def end_timer(name):
    config = ConfigParser()
    config.read('timers.ini')
    if config.has_section(name):
        config.remove_section(name)
    with open('timers.ini', 'w') as configfile:
        config.write(configfile)

def edit_message_interval(name, interval):
    print("editing interval")
    config = ConfigParser()
    config.read('timers.ini')
    if config.has_section(name):
        print(name,interval)
        config.set(name,"interval", str(interval))
        with open('timers.ini','w') as configfile:
            config.write(configfile)


def timed_message(name, socket):
    config = ConfigParser()
    config.read('timers.ini')
    if config.has_section(name):
        message = config.get(name,"message")
        new_interval = config.get(name,"interval")
        print(message)
        #sendMessage(socket,message)
        t = Timer(int(new_interval), timed_message,[name, socket])
        t.start()
    else:
        print("Timer was previously ended.")

def start_messages(socket):
    config = ConfigParser()
    config.read('timers.ini')
    for section in config.sections():
        message = config.get(section,"message")
        interval = config.getint(section,"interval")
        t = Timer(int(interval), timed_message,[section, socket])
        t.start()