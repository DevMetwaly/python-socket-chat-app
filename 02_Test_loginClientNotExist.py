import socket
import pickle
from Message import *
import base64

def Main():
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    username="Hungry"
    password="Hungry99"
    Msg= MSG((username,password),MSGTYPE.LOGIN)

    
    s.send(base64.b64encode(pickle.dumps(Msg)))
    data = pickle.loads(base64.b64decode(s.recv(1024)))

    print((data.message, data.msgType))
    """data = pickle.loads(s.recv(1024))
    print(data.message)
    while True:
        s.send(pickle.dumps(MSG(input(""),MSGTYPE.Message)))
        print(str(s.recv(1024)))
    """
    s.close()

if __name__ == '__main__':
    Main()
