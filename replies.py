import time
import random

botnick = "pikachuinuit"
master = "rahuldecoded"

def send_hi():
    return random.choice(('hi', 'hey', 'hello'))


Replies = dict()
Replies ['time'      ] = "Current time "+ time.strftime("%X")
Replies ['date'      ] = "Current date "+ time.strftime("%x") + " and today is " + time.strftime("%a")
Replies ['goodbye'  ] = "I'll miss you"
Replies ['sing'     ] = "Tra la la"
Replies ['hello'    ] = send_hi()
Replies ['hi'       ] = send_hi()
Replies ['hey'      ] = send_hi()
Replies ['master'   ] = master + " is my master"
Replies ['daddy'] = master
Replies [botnick] = "What do you want?"
def find_in_Replies(word):
    global Replies
    if word in Replies:
        return True

def reply(word):
    global Replies
    return Replies[word]