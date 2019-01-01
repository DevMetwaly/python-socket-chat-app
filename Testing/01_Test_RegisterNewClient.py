import socket, pickle, base64
from Classes.Message import *
from sqlobject import *


def Main():
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))


    
    client = {
                'fullname':'1',
                'username':'1',
                'password':'1',
                'email':'1',
                'gender':'Male',
                'status':'Online'
            }
    
    
    print(client)
    Msg = MSG(client, MSGTYPE.SIGN_UP)

    s.send(base64.b64encode(pickle.dumps(Msg)))
    data = pickle.loads(base64.b64decode(s.recv(1024)))
    print((data.message,data.msgType))
    s.close()


if __name__ == '__main__':
    Main()

