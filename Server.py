import socket 
from _thread import * 
import threading
import pickle
print_lock = threading.Lock()
users = []
usersData = {}

def addUserToSystem(userName, password, userObject):
    usersData[userName] = password
    users.append((userObject, userName))


def register(name):
    if name in usersData:
        return True
    else:
        return False

def recieveMessages(obj,name):
    while True:
        data = pickle.loads(obj.recv(1024)).message
        broadcast(name+": "+data)


def threaded(c):
    while True:
        Msg = c.recv(1024)
        Msg = pickle.loads(Msg)
        success = bool()
        if(Msg.type == MSGTYPE.LOGIN):
            success = login(Msg.userName, Msg.password)
            if(success):
                c.send("Logged In successfully")
            else:
                c.send("Failed ...")
        else:
            success = register(Msg.userName)
            if(success):
                c.send("Registered Successfully")
            else:
                c.send("Username is already exist")
        if(success):
            usersData[Msg.userName] = Msg.password
            users.append((Msg.userName,c))
            break
    for (username, userObj) in users:
        if userObj == obj:
            name = username

    recieveMessages(c)
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