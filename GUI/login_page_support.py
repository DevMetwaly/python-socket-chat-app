# Created with great help of PAGE.
import sys
import chat_page, client
import tkinter as tk

def set_Tk_var():
    global combobox
    combobox = tk.StringVar()

def login_handler(data, soc):
    if client.login_request(data) != 0:
        destroy_window()
        chat_page.main()
    else:
        print('Invalid username or password. (', data, ')')
    sys.stdout.flush()

def register_handler(data):
    if client.register_request(data):
        #print('Registering: ', data)
        pass
    else:
        print('Error with registeration.')
    sys.stdout.flush()

def switch_login(page):
    page.lift()
    print('Switching to Login page')
    sys.stdout.flush()

def switch_register(page):
    page.lift()
    print('Switching to Register page')
    sys.stdout.flush()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import login_page
    login_page.GUIStart()




