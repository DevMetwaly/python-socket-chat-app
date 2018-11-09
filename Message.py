from enum import Enum


class MSG:
    def __init__(self, message, msgType):
        self.message = message
        self.msgType = msgType


class MSGTYPE(Enum):
    LOGIN = 1
    SIGN_UP = 2
    ONLINE = 3
    OFFLINE = 4
    FAILURE = 5
    Message = 6
