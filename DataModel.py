import os
from sqlobject import *
from time import *


class Client(SQLObject):
    fullname = StringCol()
    username = StringCol(alternateID=True)
    password = StringCol()
    email = StringCol(alternateID=True)
    gender = EnumCol(enumValues=["Male", "Female"])
    status = EnumCol(enumValues=["Online", "Offline", "Busy"])
    messages = MultipleJoin(otherClass="Chat", joinColumn="sender_id")
    ClientConnection = None

class Chat(SQLObject):
    sender = ForeignKey("Client")
    message = StringCol()
    time = DateTimeCol(default=DateTimeCol.now())


class DataModel:
    def __init__(self,Name = "data"):
        sqlhub.processConnection = connectionForURI('sqlite:' + os.path.abspath(Name+".db"))
        Client.createTable(True)
        Chat.createTable(True)

    
    def register(self,client,clientConnection):    
        try:
            client = Client(fullname = client.fullname, username=client.username, password=client.password, email=client.email, gender=client.gender, status=client.status)
            client.ClientConnection = clientConnection
            return (True, "Registered Successfully!, Hello: " + client.username, client)
        except dberrors.DuplicateEntryError:
            return (False, "Usernaame or Email is Already exist.", None)
        
    def login(self,username,password,clientConnection):
        client = Client.select(AND(Client.q.username==username,Client.q.password==password))
        if (client.count()==1):
            client = list(client)[0]
            client.clientConnection = clientConnection
            return (True, "Loggedin Successfully.",client)

        return (False, "Wrong username or Password", None)
    def message(self,client,message):pass





#ahmed=Client(fullname="Ahmed Bally",username="Bally",password="123456",email="ahmed@bally.cu.cc",gender="Male",status="Online")
#Chat(sender=ahmed,message="Hello !")
#print(Client.get(1).messages)
#print(list(Chat.select()))

