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
            try:
                self.sendMessageToClient(client.ClientConnection, message)
            except:
                self.logout(client)

    def logout(self,client):
        self.onlineClients.remove(client)
        self.db.updateClientStatus(client,'Offline')

    def clientThread(self, clientConnection):
        client=None
        isSucceed = False
        status = None
        while True:
            Msg = self.receiveMessageFromClient(clientConnection)
            print(Msg.msgType)
            if Msg.msgType.value == MSGTYPE.LOGIN.value:
                (isSucceed, status, client) = self.db.login(Msg.message[0],Msg.message[1],clientConnection)
            elif Msg.msgType.value == MSGTYPE.SIGN_UP.value:
                (isSucceed, status, client) = self.db.register(Msg.message,clientConnection)
            print()
            print(Msg.msgType,MSGTYPE.SIGN_UP)
            print(status)
            if isSucceed:
                self.onlineClients.append(client)
                self.sendMessageToClient(client.ClientConnection, MSG(status, MSGTYPE.SUCCESS))
                self.brodcastMessage(MSG(client.fullname + " is now online", MSGTYPE.ONLINE))
                break
            else:
                self.sendMessageToClient(clientConnection, MSG(status, MSGTYPE.FAILURE))
                #clientConnection.close() #to be commented
                #return #to be commented
        self.brodcastMessage(MSG([(client.fullname, client.username, client.status) for client in list(Client.select())],MSGTYPE.OnlineList))
        self.sendMessageToClient(client.ClientConnection, MSG([(chat.sender.fullname, chat.message, chat.time) for chat in Chat.select()],MSGTYPE.MessageList))
        while True:

            try:
                Msg = self.receiveMessageFromClient(client.ClientConnection)
                Chat(senderID=client,message=Msg.message)
            except :
                self.logout(client)
                self.brodcastMessage(MSG(client.fullname + " is now offline", MSGTYPE.OFFLINE))
                return

            if(Msg.msgType == MSGTYPE.Message):
                Msg.message = (Msg.message,client.fullname,'blue')
                self.brodcastMessage(Msg)
            elif(Msg.msgType == MSGTYPE.LOGOUT):
                break
            elif(Msg.msgType == MSGTYPE.UPDATE_STATE):
                self.db.updateClientStatus(client,Msg.message)
                Msg.message = (Msg.message,client.username)
                self.brodcastMessage(Msg)
            else:
                break
            
        try:
            self.logout(client)
            #maybe raise error later if the client deleted logged out from the brodcast then tries to logout agian here
        except:
            pass
        self.brodcastMessage(MSG(client.fullname + " is now offline", MSGTYPE.OFFLINE))
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
