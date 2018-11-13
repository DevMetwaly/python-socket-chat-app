import socket

STATUS_SUCCESS = {'color': '#0f0', 'text': 'ONLINE'}
STATUS_FAIL = {'color': '#f74', 'text': 'OFFLINE'}

def connect(host = '127.0.0.1', port = 20220):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print('Connect Success')
        return s, STATUS_SUCCESS
    except:
        print('Connect Fail')
        return 0, STATUS_FAIL

def login_request(data):
    print('Login attempt:', data)
    return data['username']

def register_request(data):
    print('Register attempt:', data)
    return 1

def post_message(message):
    print('Sending message to server', message, end='')
    return message

def accept_message():
    return {
        'name': 'Tarek',
        'text': 'Hello world',
        'date': '13/11/18 10:28PM',
        'color': 'blue'
    }

def get_users_list():
    return [
        {'username':'Tarek', 'color':'blue'},
        {'username':'Metwally', 'color':'red'},
        {'username':'Salma', 'color':'purple'},
        {'username':'Bally', 'color':'grey'},
        {'username':'Mona', 'color':'green'}
    ]

def get_chat_history():
    return [
        {
            'type': 'message',
            'username': 'Tarek',
            'text': 'My first message',
            'date': '12/11/18 11:58PM',
            'color': 'blue'
        },
        {
            'type': 'activity',
            'username': 'Tarek',
            'text': 'has logged out.',
            'date': '12/11/18 11:59PM',
        },
        {
            'type': 'message',
            'username': 'Salma',
            'text': 'Second message!',
            'date': '13/11/18 01:30AM',
            'color': 'purple'
        },
    ]