import socket
from _thread import *
import threading
import pickle
from Message import *
import base64
from DataModel import *
print_lock = threading.Lock()

class Server:
    def __init__(self,host="",port=12345,dbName="data"):
        self.db = DataModel(dbName)
        self.print_lock = threading.Lock()
        self.onlineClients = []
        self.s = socket.socket()
        self.s.bind((host, port))
        print("Socket is bined to post", port)

        self.s.listen(5)
        print("Socket is listening")

    def receiveMessageFromClient(self,clientConnection):
        return pickle.loads(base64.b64decode(clientConnection.recv(8000)))

    def sendMessageToClient(self,client, message):
        client.send(base64.b64encode(pickle.dumps(message)))

    def brodcastMessage(self,message):
        for client in self.onlineClients:
            self.sendMessageToClient(client.ClientConnection, message)

    def clientThread(self, clientConnection):
        client=None
        isSucceed = False
        while True:
            Msg = self.receiveMessageFromClient(clientConnection)

            if(Msg.msgType == MSGTYPE.LOGIN):
                (isSucceed, status, client) = self.db.login(Msg.message[0],Msg.message[1],clientConnection)
            elif(Msg.msgType == MSGTYPE.SIGN_UP):
                (isSucceed, status, client) = self.db.register(Msg.message,clientConnection)
                
            if(isSucceed):
                self.onlineClients.append(client)
                self.sendMessageToClient(client.ClientConnection, MSG(status, MSGTYPE.SUCCESS))
                self.brodcastMessage(MSG(client.username + " is now online", MSGTYPE.ONLINE))
                break
            else:
                self.sendMessageToClient(clientConnection, MSG(status, MSGTYPE.FAILURE))
                clientConnection.close() #to be commented
                return #to be commented

        client.ClientConnection.close()
        return

    def run(self):
        while True:
            clientConnection, addr = self.s.accept()

            print_lock.acquire()
            print("Connected to:", addr[0], ":", addr[1])
            print_lock.release()

            start_new_thread(self.clientThread, (clientConnection,))
        self.s.close()


if __name__=="__main__":
    server = Server()
    server.run()
