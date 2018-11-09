##recive 
def boardcast(msg)
for (user, name) in users:
	user.send(msg)
	
	
	
#login 
def login(username_sent,password_sent):	
	for username, password in useradata.items():
    if password == password_sent:
        return True 
	else:
		return 	False 
		