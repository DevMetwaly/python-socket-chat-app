import socket
import pickle
from Message import *
import base64

def Main():
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    username="abdo"
    password="1234"
    Msg= MSG((username,password),MSGTYPE.LOGIN)
    
    s.send(base64.b64encode(pickle.dumps(Msg)))
    data = s.recv(1024)
    print(data)
    s.close()

if __name__ == '__main__':
    Main()
