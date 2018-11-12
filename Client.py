from sqlobject import *

class Client(SQLObject):
    fullname = StringCol()
    username = StringCol(alternateID=True)
    password = StringCol()
    email = StringCol(alternateID=True)
    gender = EnumCol(enumValues=["Male", "Female"])
    status = EnumCol(enumValues=["Online", "Offline", "Busy"])
    messages = MultipleJoin(otherClass="Chat", joinColumn="sender_id")
    ClientConnection = None