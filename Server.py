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
    FAILURE = 5


def addUserToSystem(userName, password, userObject):
    usersData[userName] = password
    users.append((userObject, userName))


def register(name):
    if name in usersData:
        return (False, "Name is Already Used. Choose Other Name")
    else:
        return (True, "Registered Successfully!, Hello: "+name)


def recieveMessages(client,name):
    while True:
        Msg = getMessageFormClient(client)
        data = Msg.message
        broadcast(name+": "+data)

def sendMessageToClient(client, message):
    client.send(pickle.dumps(message))
    
def getMessageFormClient(client):
    return pickle.loads(client.recv(1024))

def login(username_sent,password_sent):	
    return (True, "Loggedin Successfully.")
	
    """
    for (username, password) in useradata.items():
        if (password == password_sent):
            return True 
        else:
            return False 
    """

def handleLoginOrRegister(Msg):
    if(Msg.msgType == MSGTYPE.LOGIN):
        return login(Msg.userName, Msg.password) + (Msg.username,)
    elif (Msg.msgType == MSGTYPE.SIGN_UP):
        return register(Msg.userName) + (Msg.username,)

    return (False,"Please Login First!!!")


def threaded(client):
    userName = str()
    while True:
        Msg = getMessageFormClient(client)
        (isSucceed, status, userName) = handleLoginOrRegister(Msg)
        if(isSucceed):
            addUserToSystem(Msg.userName,Msg.password,client)
            break
        else:
            sendMessageToClient(client,MSG(status,MSGTYPE.FAILURE))
            

    sendMessageToClient(client,MSG(status,MSGTYPE.FAILURE))
    Msg = MSG(userName + " is now online", MSGTYPE.ONLINE)

    recieveMessages(client,userName)

    Msg = MSG(userName + " is now offline", MSGTYPE.OFFLINE)
    removeUser(client)
    client.close()

def Main():
    host = ""

    port = 12345
    s = socket.socket()
    
    s.bind((host,port))
    print("Socket is bined to post", port)

    s.listen(5)
    print("Socket is listening")

    while True:
        client, addr = s.accept()

        print_lock.acquire()
        print("Connected to:", addr[0], ":", addr[1])
        print_lock.release()

        start_new_thread(threaded,(client,))
    s.close()

if __name__ == "__main__":
    Main()