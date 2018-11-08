import socket 
from _thread import * 
import threading
import pickle
from enum import Enum

print_lock = threading.Lock()
users = []
usersData = {}



class MSG:
    def __init__(self, message, msgType):
        self.message = message
        self.msgType = msgType


class MSGTYPE(Enum):
    LOGIN = 1
    SIGN_UP = 2
    ONLINE = 3
    OFFLINE = 4

def addUserToSystem(userName, password, userObject):
    usersData[userName] = password
    users.append((userObject, userName))

def threaded(c):
    while True:
        Msg = c.recv(1024)
        Msg = pickle.loads(Msg)
        success = bool()
        if(Msg.msgType == MSGTYPE.LOGIN):
            success = login(Msg.userName, Msg.password)
            if(success):
                c.send("Logged In successfully")
            else:
                c.send("Failed ...")
        else:
            success = register(Msg.userName, Msg.password)
            if(success):
                c.send("Registered Successfully")
            else:
                c.send("Username is already exist")
        if(success):
            usersData[Msg.userName] = Msg.password
            users.append((c,Msg.userName))
            break
    
    Msg = MSG("Ahmed is now online", MSGTYPE.ONLINE)
    recieveMessages(c)

    Msg = MSG("Ahmed is now offline", MSGTYPE.OFFLINE)
    removeUser(c)
    c.close()

def Main():
    host = ""

    port = 12345
    s = socket.socket()
    
    s.bind((host,port))
    print("Socket is bined to post", port)

    s.listen(5)
    print("Socket is listening")

    while True:
        c, addr = s.accept()

        print_lock.acquire()
        print("Connected to:", addr[0], ":", addr[1])
        print_lock.release()

        start_new_thread(threaded,(c,))
    s.close()

if __name__ == "__main__":
    Main()