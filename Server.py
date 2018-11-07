import socket 
from _thread import * 
import threading
import pickle
print_lock = threading.Lock()
users = []
usersData = {}

def threaded(c):
    While True:
    Msg = c.recv(1024)
    
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