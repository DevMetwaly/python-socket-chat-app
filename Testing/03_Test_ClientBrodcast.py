import socket, base64, pickle
from _thread import start_new_thread
from Classes.Message import *


def Recive(s):
    while True:
        data = pickle.loads(base64.b64decode(s.recv(1024)))
        print((data.message, data.msgType))


def Main():
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))



    username="1"
    password="1"
    Msg= MSG((username,password),MSGTYPE.LOGIN)
    s.send(base64.b64encode(pickle.dumps(Msg)))
    data = pickle.loads(base64.b64decode(s.recv(1024)))
    print((data.message, data.msgType))

    data = pickle.loads(base64.b64decode(s.recv(1024)))
    print((data.message, data.msgType))

    start_new_thread(Recive,(s,))
    while True:
        message = input('message: ')
        Msg = MSG(message, MSGTYPE.Message)
        s.send(base64.b64encode(pickle.dumps(Msg)))
    s.close()

if __name__ == '__main__':
    Main()
