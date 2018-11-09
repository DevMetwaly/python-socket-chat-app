import socket
from _thread import *
import threading
import pickle
from Message import *
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
        userObj.send(msg.encode('ascii'))


def recieveMessages(client, name):
    while True:
        Msg = getMessageFormClient(client)
        data = Msg.message
        broadcastMessageToAllClients(name + ": " + data)


def sendMessageToClient(client, message):
    client.send(pickle.dumps(message))


def getMessageFormClient(client):
    return pickle.loads(client.recv(1024))


def login(username_sent, password_sent):
    return (True, "Loggedin Successfully.")

    """
    for (username, password) in useradata.items():
        if (password == password_sent):
            return True 
        else:
            return False 
    """


def handleLoginOrRegister(Msg):
    if (Msg.msgType == MSGTYPE.LOGIN):
        return login(Msg.message[0], Msg.message[1]) + (Msg.message[0],)
    elif (Msg.msgType == MSGTYPE.SIGN_UP):
        return register(Msg.message[0], Msg.message[1]) + (Msg.message[0],)

    return (False, "Please Login First!!!")


def threaded(client):
    userName = str()
    while True:
        Msg = getMessageFormClient(client)
        (isSucceed, status, userName) = handleLoginOrRegister(Msg)
        if (isSucceed):
            addUserToSystem(Msg.message[0], Msg.message[1], client)
            break
        else:
            sendMessageToClient(client, MSG(status, MSGTYPE.FAILURE))
    sendMessageToClient(client, MSG(userName + " is now online", MSGTYPE.ONLINE))
    try:
        recieveMessages(client, userName)
    except EOFError:
        #removeUser(client)
        broadcastMessageToAllClients(MSG(userName + " is now offline", MSGTYPE.OFFLINE).message)
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