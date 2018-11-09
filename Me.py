usersData={
    "Salma": 1234,
    "Mona": 123
}

# def register(name):
#     if name in usersData:
#         return True
#     else:
#         return False
#
# register("Ahmed")

#######

users=[]



class User():
    def __init__(self, Age, Depart):
        self.Age = Age
        self.Depart = Depart


Salma=User(21,'ay7aga1')
Mona=User(22,'ay7aga2')
Ahmed=User(23,'ay7aga3')

users.append(("Salma",Salma))
users.append(("Mona",Mona))
users.append(("Ahmed",Ahmed))



usersData={
    "salma": 123,
    "mostafa": 15
}
def login(username_sent, password_sent):
    for username in usersData:
            if (password_sent == usersData[username]):
                return (True, "Loggedin Successfully.")

    return (False, "UnSuccessfulg Logging in")


print(login("mostafa",15))
#recieveMessage(users[2][1])