import os
import re
import socket

import traceback

from replies import reply, find_in_Replies


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
    botnick = os.environ.get("NB_USER", "nutrient-bot")
    bufsize = 2048
    admin = ["rahuldecoded"]
    channel = os.environ.get("NB_CHANNEL", "#uit-foss")
    port = int(os.environ.get("NB_PORT", 6667))
    server = os.environ.get("NB_SERVER", "irc.freenode.net")
    master = "rahuldecoded"
    uname = "Nutrient Bot"
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
            request = tokens[3]
            tokenLength = len(tokens)

            # For adding someone as a admin
            if request == "::add":
                if tokenLength > 4:
                    if ircmsg.strip(":").split("!")[0] in admin:
                        admin.append(tokens[1])
                elif tokenLength == 4:
                    sendmsg(channel, "Usage: :add [nick]")

            # For removing someone from admin privilege.
            if request == "::remove" and tokenLength > 4:
                if ircmsg.strip(":").split("!")[0] in admin:
                    try:
                        admin.remove(tokens[1])
                    except ValueError:
                        return tokens[1] + "is not in admin list."
                elif tokenLength == 4:
                    sendmsg(channel, "Usage: :remove [nick]")

            # User Commands
            


            

        except Exception as e:
            tb = traceback.format_exc()
            print(tb)

main()
exit(0)
