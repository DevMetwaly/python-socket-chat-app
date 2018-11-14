# Created with great help of PAGE.

import sys, login_page, client
import tkinter as tk

def set_Tk_var():
    global chat_log
    chat_log = tk.StringVar()
    global online_users
    online_users = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def send_button_handler(message,soc):
    if len(message) > 1:
        client.post_message(message,soc)

def logout_handler():
    destroy_window()
    login_page.main()
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import chat_page
    chat_page.GUIStart()




