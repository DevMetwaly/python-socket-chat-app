import os
from sqlobject import *
from time import *
from Classes.Client import *
from Classes.Chat import *

DATABASE_PATH = 'Database/'

class DataModel:
    def __init__(self, Name = "data"):
        sqlhub.processConnection = connectionForURI('sqlite:' + os.path.abspath(DATABASE_PATH + Name + ".db"))
        Client.createTable(True)
        Chat.createTable(True)

    
    def register(self, client, clientConnection):    
        
        try:
            client = Client(fullname = client['fullname'], username=client['username'], password=client['password'], color=client['color'], email=client['email'], gender=client['gender'], status=client['status'])
            client.ClientConnection = clientConnection
            return (True, "Registered Successfully!, Hello: " + client.username, client)
        
        except dberrors.DuplicateEntryError:
            return (False, "Usernaame or Email is Already exist.", None)
        
    def login(self,username,password,clientConnection):
        client = Client.select(AND(Client.q.username==username,Client.q.password==password))
        if (client.count()==1):
            client = list(client)[0]
            self.updateClientStatus(client,"Online")
            client.ClientConnection = clientConnection
            print(client)
            return (True, "Loggedin Successfully.",client)

        return (False, "Wrong username or Password", None)

    def updateClientStatus(self,client,state):
        client.status = state
        
    def message(self,client,message):pass





#ahmed=Client(fullname="Ahmed Bally",username="Bally",password="123456",email="ahmed@bally.cu.cc",gender="Male",status="Online")
#Chat(sender=ahmed,message="Hello !")
#print(Client.get(1).messages)
#print(list(Chat.select()))

