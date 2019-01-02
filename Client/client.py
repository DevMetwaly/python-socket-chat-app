import base64, socket, time, pickle
from Classes.Message import *


STATUS_SUCCESS = {'color': '#0f0', 'text': 'ONLINE'}
STATUS_FAIL = {'color': '#f74', 'text': 'OFFLINE'}


def receiveMessageFromServer(serverConnection):
    return pickle.loads(base64.b64decode(serverConnection.recv(8000)))


def sendMessageToServer(server, message):
    server.send(base64.b64encode(pickle.dumps(message)))


def connect(host='127.0.0.1', port=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print('Connection succeeded.')
        return s, STATUS_SUCCESS
    except:
        print('Connection failed.')
        return 0, STATUS_FAIL


def login_request(data, soc):
    data = (data['username'], data['password'])
    sendMessageToServer(soc, MSG(data, MSGTYPE.LOGIN))
    Msg = receiveMessageFromServer(soc)
    print(Msg.msgType)
    if Msg.msgType.value == MSGTYPE.SUCCESS.value:
        return True, Msg.message
    return False, Msg.message


def register_request(data, soc):
    sendMessageToServer(soc, MSG(data, MSGTYPE.SIGN_UP))
    Msg = receiveMessageFromServer(soc)
    if Msg.msgType.value == MSGTYPE.SUCCESS.value:
        return True, Msg.message
    return False, Msg.message


def post_message(message,soc):
    sendMessageToServer(soc, MSG(message, MSGTYPE.Message))
    return message


def accept_message():
    return {
        'name': 'Tarek',
        'text': 'Hello world',
        'date': '13/11/18 10:28PM',
        'color': 'blue'
    }


def get_users_list(soc):
    Msg = receiveMessageFromServer(soc)
    return [{'fullname': x[1], 'username': x[0], 'color': 'blue'} for x in
            Msg.message] if Msg.msgType.value == MSGTYPE.OnlineList.value else []

