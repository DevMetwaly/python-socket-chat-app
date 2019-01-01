from sqlobject import *


class Chat(SQLObject):
    sender = ForeignKey("Client")
    message = StringCol()
    time = DateTimeCol(default=DateTimeCol.now())