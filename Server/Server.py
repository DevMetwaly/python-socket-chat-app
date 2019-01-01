import socket, base64, threading, pickle
from _thread import *
from time import sleep
from Classes.Message import *
from Classes.DataModel import *

print_lock = threading.Lock()

class Server:
    def __init__(self,host="", port=12345, dbName = "data"):
        self.db = DataModel(dbName)
        self.print_lock = threading.Lock()
        self.onlineClients = []
        self.s = socket.socket()
        self.s.bind((host, port))
        print("Socket is binded to port", port)

        self.s.listen(5)
        print("Socket is listening..")

    def receiveMessageFromClient(self, clientConnection):
        return pickle.loads(base64.b64decode(clientConnection.recv(8000)))

    def sendMessageToClient(self, clientConnection, message):
        clientConnection.send(base64.b64encode(pickle.dumps(message)))

    def brodcastMessage(self, message):
        for client in self.onlineClients:
            try:
                self.sendMessageToClient(client.ClientConnection, message)
            except:
                self.logout(client)

    def logout(self, client):
        self.onlineClients.remove(client)
        self.db.updateClientStatus(client, STATUS_OFFLINE)

    def clientThread(self, clientConnection):
        client = None
        isSucceed = False
        status = None
        while True:
            Msg = self.receiveMessageFromClient(clientConnection)

            if Msg.msgType.value == MSGTYPE.LOGIN.value:
                (isSucceed, status, client) = self.db.login(Msg.message[0], Msg.message[1], clientConnection)

            elif Msg.msgType.value == MSGTYPE.SIGN_UP.value:
                (isSucceed, status, client) = self.db.register(Msg.message, clientConnection)

            if isSucceed:
                self.onlineClients.append(client)
                self.sendMessageToClient(client.ClientConnection, MSG(status, MSGTYPE.SUCCESS))
                self.brodcastMessage(MSG(client.fullname, MSGTYPE.ONLINE))
                break

            else:
                self.sendMessageToClient(clientConnection, MSG(status, MSGTYPE.FAILURE))
                
        sleep(.5)


        self.brodcastMessage(MSG(
        	[(client.fullname, client.username, client.status) for client in list(Client.selectBy(status = STATUS_ONLINE))],
        	MSGTYPE.OnlineList))

        self.sendMessageToClient(
        	client.ClientConnection,
        	MSG([(chat.message, chat.sender.fullname, chat.sender.color) for chat in Chat.select()], MSGTYPE.MessageList))

        while True:

            try:
                Msg = self.receiveMessageFromClient(client.ClientConnection)
                Chat(senderID = client, message = Msg.message)

            except:
                self.logout(client)
                self.brodcastMessage(MSG(client.fullname, MSGTYPE.OFFLINE))
                return

            if Msg.msgType.value == MSGTYPE.Message.value:
                Msg.message = (Msg.message, client.fullname, client.color)
                self.brodcastMessage(Msg)

            elif Msg.msgType.value == MSGTYPE.LOGOUT.value:
                break
            
            elif Msg.msgType.value == MSGTYPE.UPDATE_STATE.value:
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

        self.brodcastMessage(MSG(client.fullname, MSGTYPE.OFFLINE))
        client.ClientConnection.close()
        return

    def run(self):

        while True:
            clientConnection, [clientIP, clientPort] = self.s.accept()
            print_lock.acquire()
            print("Connected to:", clientIP, ":", clientPort)
            print_lock.release()
            start_new_thread(self.clientThread, (clientConnection,))
            
        self.s.close()


if __name__=="__main__":
    server = Server()
    server.run()
