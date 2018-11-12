import socket
import pickle
from Message import *
import base64

from sqlobject import *

class client:
    def __init__(self,fullname,username,password,email,gender,status):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.status = status


def Main():
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    client1 = client("Salma Hungry2","Hungry22","Hungry99","HungrySalma2@gmail.com","Female","Online")
    
    print(client1)
    Msg = MSG(client1, MSGTYPE.SIGN_UP)

    s.send(base64.b64encode(pickle.dumps(Msg)))
    data = pickle.loads(base64.b64decode(s.recv(1024)))
    print((data.message,data.msgType))
    s.close()


if __name__ == '__main__':
    Main()

