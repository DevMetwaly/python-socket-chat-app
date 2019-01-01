from sqlobject import *

STATUS_OFFLINE = 'Offline'
STATUS_ONLINE  = 'Online'
STATUS_BUSY = 'Busy'

GENDER_M = 'Male'
GENDER_F = 'Female'

class Client(SQLObject):
    fullname = StringCol()
    username = StringCol(alternateID = True)
    password = StringCol()
    email = StringCol(alternateID = True)
    color = EnumCol(enumValues = ['blue', 'green', 'red', 'black', 'pink', 'navy'])
    gender = EnumCol(enumValues = [GENDER_M, GENDER_F])
    status = EnumCol(enumValues = [STATUS_ONLINE, STATUS_OFFLINE, STATUS_BUSY])
    messages = MultipleJoin(otherClass = "Chat", joinColumn = "sender_id")
    ClientConnection = None
    