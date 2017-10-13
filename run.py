import re
import socket
from replies import reply, find_in_Replies
from Queue import Queue
import traceback
from weather import weather
from bs4 import BeautifulSoup
from joke import joke
from google import get_urls
import wiki

user_queue = Queue()
'''
alg = algebra()
# For sending messages to a specified channel
'''


def sendmsg(chan, msg):
    global irc
    irc.send("PRIVMSG ".encode() + chan.encode() +" :".encode() + msg.encode() + "\n".encode())


# This is a subroutine which help to join a specified channel
def JoinChan(chan):
    global irc
    irc.send("JOIN ".encode() + chan.encode() + "\n".encode())


# This is a subroutine which responds to server pings
def ping():
    global irc
    irc.send("PONG :pingis\n".encode())


# This is a main routine
def main():
    global irc, user_queue
    botnick = "pikachu_"
    bufsize = 2048
    admin = ["rahuldecoded"]
    channel = "#uit-foss"
    port = 6667
    server = "irc.freenode.net"
    master = "rahuldecoded"
    uname = "Pikachu - Test Bot"
    realname = "I'm a Test Bot!"
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    irc.send("USER ".encode() + botnick.encode() + " ".encode() + botnick.encode() + " ".encode()
             + botnick.encode() + " :Hello! I am a test bot!\r\n".encode())
    irc.send("NICK ".encode() + botnick.encode() + "\n".encode())
    JoinChan(channel)

    pattern1 = '.*:(\w+)\W*%s\W*$' % botnick
    pattern2 = '.*:%s\W*(\w+)\W*$' % botnick

    while 1:
        try:
            msg = irc.recv(bufsize)
            ircmsg = msg.decode()
            ircmsg = ircmsg.strip('\n\r')

            print(ircmsg)
            m1 = re.match(pattern1, ircmsg, re.I)
            m2 = re.match(pattern2, ircmsg, re.I)
            if (m1 == None) and (m2 != None):
                m1 = m2
            if (m1 != None):  # Yes
                word = m1.group(1)  # Word found
                word = word.lower()  # Make word lower case
                # Print a reply
                if find_in_Replies(word):
                    sendmsg(channel, reply(word))

        except Exception:
            pass

    # Admin Commands
        # For showing the length of the queue.
        tokens = ircmsg.split(" ")
        if tokens[0] == "PING":
            ping()
            continue
        if tokens[1] != "PRIVMSG":
            continue
        try:
            if tokens[3] == "::show":
                if ircmsg.strip(":").split("!")[0] in admin:
                    sendmsg(channel, str(user_queue.in_queue()) + " \n")

            # For getting to the next user in the queue.
            if tokens[3] == "::next":
                if ircmsg.strip(":").split("!")[0] in admin:
                    sendmsg(channel, str(user_queue.next_nick()) + " \n")
                    user_queue.pop_next()

            # For clearing the queue.
            if tokens[3] == "::clearqueue":
                if ircmsg.strip(":").split("!")[0] in admin:
                    user_queue.clear()
                    sendmsg(channel, "Queue cleared")

            # For adding someone as a admin
            if tokens[3] == "::add" and len(tokens) > 4:
                if ircmsg.strip(":").split("!")[0] in admin:
                    admin.append(tokens[1])
            elif tokens[3] == "::add" and len(tokens) == 4:
                sendmsg(channel, "Usage: :add [nick]")

            # For removing someone from admin privilege.
            if tokens[3] == "::remove" and len(tokens) > 4:
                if ircmsg.strip(":").split("!")[0] in admin:
                    try:
                        admin.remove(tokens[1])
                    except ValueError:
                        return tokens[1] + "is not in admin list."
            elif tokens[3] == "::remove" and len(tokens) == 4:
                sendmsg(channel, "Usage: :remove [nick]")

            # User Commands
            if tokens[3] == ":!":
                user_name = ircmsg.strip(":").split("!")
                sendmsg(channel, str(user_name[0]) + " , you have added in queue. Wait for your turn.\n")
                user_queue.enqueue(user_name[0])

            # Command for temperature
            # Syntax: ":temp kolkata"

            if tokens[3] == "::temp" and len(tokens) > 4:
                sendmsg(channel, weather(tokens[1]))
            elif tokens[3] == "::temp" and len(tokens) == 4:
                sendmsg(channel, "Usage: :temp [city name]")

            # Command for joke
            # Syntax: ":joke"

            if tokens[3] == "::joke":
                sendmsg(channel, joke())

            # Command for google
            # Syntax: ":google"

            if tokens[3] == "::google" and len(tokens) > 4:
                sendmsg(channel, get_urls(' '.join(tokens[4:])))
            elif tokens[3] == "::google" and len(tokens) == 4:
                sendmsg(channel, "Usage: :google [query]")
            
            # Command for wiki
            # Syntax: ":wiki"
            if tokens[3] == "::wiki" and len(tokens) > 4:
                sendmsg(channel, wiki.summary(' '.join(tokens[4:])))
            elif tokens[3] == "::wiki" and len(tokens) == 4:
                sendmsg(channel, "Usage: :wiki [query]")

        except Exception as e:
            tb = traceback.format_exc()
            print(tb)


main()
exit(0)
