import socket
from _thread import *
import threading
import pickle
from Message import *
import base64
print_lock = threading.Lock()
users = []
usersData = {}

def addUserToSystem(userName, password, userObject):
    usersData[userName] = password
    users.append((userObject, userName))


def register(name):
    if name in usersData:
        return (False, "Name is Already Used. Choose Other Name")

    return (True, "Registered Successfully!, Hello: " + name)


def broadcastMessageToAllClients(msg):
    for (userObj, _) in users:
        userObj.send(msg)


def recieveMessages(client, name):
    while True:
        print("Taking user name and password.")
        Msg = getMessageFormClient(client)
        data = Msg.message
        broadcastMessageToAllClients(name + ": " + data)


def sendMessageToClient(client, message):
    client.send(base64.b64encode(pickle.dumps(message)))
    


def getMessageFormClient(client):    
    return pickle.loads(base64.b64decode(client.recv(1024)))



<<<<<<< HEAD
    """
    for (username, password) in usersdata.items():
        if (password == password_sent):
            return True 
        else:
            return False 
    """
=======

def login(username_sent, password_sent):
    for username in usersData:
        if (password_sent == usersData[username]):
            return (True, "Loggedin Successfully.")
        
    return (False, "UnSuccessfulg Logging in")
>>>>>>> ccbe4be81dc926c79472f604e2af33de4108efce

<<<<<<< HEAD
#list_of_onlineusers = [("mona" ,1),("tarek",4),("metwaly" ,5),("salma",9)]
list_of_onlineusers = dict(list_of_onlineusers)
def removeuser(client):
	
	
	print (list_of_onlineusers)
	del list_of_onlineusers[client]
	print (list_of_onlineusers)
=======
>>>>>>> 507a91afc6627228ad7ddafdd31dd6ae17e99696

def handleLoginOrRegister(Msg):
    if (Msg.msgType == MSGTYPE.LOGIN):
        return login(Msg.message[0], Msg.message[1]) + (Msg.message[0],)
    elif (Msg.msgType == MSGTYPE.SIGN_UP):
        return register(Msg.message[0]) + (Msg.message[0],)

    return (False, "Please Login First!!!")


def threaded(client):
    print("NEW CLIENT")
    userName = str()
    while True:
        Msg = getMessageFormClient(client)
        
        (isSucceed, status, userName) = handleLoginOrRegister(Msg)
        print((isSucceed, status, userName))
        if (isSucceed):
            addUserToSystem(Msg.message[0], Msg.message[1], client)
            break
        else:
            sendMessageToClient(client, MSG(status, MSGTYPE.FAILURE))
            #client.close()
            #return

    sendMessageToClient(client, MSG(status, MSGTYPE.FAILURE))
    Msg = MSG(userName + " is now online", MSGTYPE.ONLINE)

    #recieveMessages(client, userName)

    Msg = MSG(userName + " is now offline", MSGTYPE.OFFLINE)
    #removeUser(client)
    client.close()


def Main():
    host = ""

    port = 12345
    s = socket.socket()

    s.bind((host, port))
    print("Socket is bined to post", port)

    s.listen(5)
    print("Socket is listening")

    while True:
        client, addr = s.accept()

        print_lock.acquire()
        print("Connected to:", addr[0], ":", addr[1])
        print_lock.release()

        start_new_thread(threaded, (client,))
    s.close()


if __name__ == "__main__":
    Main()