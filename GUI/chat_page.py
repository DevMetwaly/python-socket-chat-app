# Created with great help of PAGE.
import sys, client, socket
from threading import Thread
from PIL import Image,ImageTk
import tkinter as tk
import chat_page_support
try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

COLOR = '#bc2626'

class ChatInterface:
    def __init__(self, top=None, color="#bc2626"):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _appcolor = color #'#bc2626'
        _bgcolor = color #'#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        font10 = "-family {Segoe UI} -size 12 -weight normal -slant "  \
                 "roman -underline 0 -overstrike 0"
        font9 = "-family {Hobo Std} -size 12 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('vista')

        self.style.configure('.', background=_bgcolor, foreground=_fgcolor, font="TkDefaultFont")
        self.style.map('.', background =
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("640x480")
        top.title("GhostsChatApp")
        top.configure(background=_appcolor, highlightbackground="#efefef", highlightcolor="#646464")

        self.main_app_label = tk.Label(top)
        self.main_app_label.place(relx=0.016, rely=0.95, height=20, width=120)
        self.main_app_label.configure(
            activebackground=_appcolor,
            activeforeground="black",
            background=_appcolor,
            disabledforeground="#a3a3a3",
            font=font9,
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='''GhostsChatApp!'''
        )

        self.logout_button = tk.Button(top)
        self.logout_button.place(relx=0.8, rely=0.95, height=20, width=113)
        self.logout_button.configure(
            activebackground="#bc2626",
            activeforeground="#daa",
            background="#bc2626",
            borderwidth="0",
            cursor='hand2',
            disabledforeground="#a3a3a3",
            command=chat_page_support.logout_handler,
            foreground="#fff",
            highlightbackground="#bc2626",
            highlightcolor="#ff0",
            pady="0",
            text='''Logout'''
        )

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.chat_frame = tk.Frame(top)
        self.chat_frame.place(relx=0.016, rely=0.811, relheight=0.123, relwidth=0.664)
        self.chat_frame.configure(
            relief='groove',
            borderwidth="2",
            background="#d9d9d9",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            width=425
        )

        self.chat_send_button = tk.Button(self.chat_frame)
        self.chat_send_button.place(relx=0.835, rely=0.0, height=63, width=66)
        self.chat_send_button.configure(
            activebackground="#d9d9d9",
            activeforeground="#000000",
            background="#d9d9d9",
            borderwidth="0",
            command=lambda: chat_page_support.send_button_handler(self.get_message_text()),
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            text='''Send'''
        )

        self.chat_frame_textbox = ScrolledText(self.chat_frame)
        self.chat_frame_textbox.place(relx=0.0, rely=0.0, relheight=0.985, relwidth=0.835)
        self.chat_frame_textbox.configure(
            background="white",
            font="TkTextFont",
            foreground="black",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            insertborderwidth="3",
            selectbackground="#c4c4c4",
            selectforeground="black",
            width=10,
            wrap='none'
        )
        self.style.configure('TNotebook.Tab', background=_bgcolor, foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])

        self.chat_frame = ttk.Notebook(top)
        self.chat_frame.place(relx=0.016, rely=0.019, relheight=0.775, relwidth=0.663)
        self.chat_frame.configure(width=424, takefocus="")
        self.chat_frame_t0 = tk.Frame(self.chat_frame)
        self.chat_frame.add(self.chat_frame_t0, padding=0)
        self.chat_frame.tab(0, text="Public Room", compound="left", underline="-1")
        self.chat_frame_t0.configure(
            background="#000",
            highlightbackground="#d9d9d9",
            highlightcolor="black")

        self.chat_scrolledtext = ScrolledText(self.chat_frame_t0)
        self.chat_scrolledtext.place(relx=0.0, rely=0.0, relheight=1.011, relwidth=1.012)
        self.chat_scrolledtext.configure(
            background="white",
            font=font10,
            foreground="black",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            insertborderwidth="3",
            selectbackground="#c4c4c4",
            selectforeground="black",
            width=10,
            wrap=tk.WORD
        )

        self.side_frame = ttk.Notebook(top)
        self.side_frame.place(relx=0.688, rely=0.019, relheight=0.915, relwidth=0.288)
        self.side_frame.configure(width=184)
        self.side_frame.configure(takefocus="")
        self.side_frame_t0 = tk.Frame(self.side_frame)
        self.side_frame.add(self.side_frame_t0, padding=0)
        self.side_frame.tab(0, text="Online",compound="left",underline="-1",)
        self.side_frame_t0.configure(
            background="#d9d9d9",
            highlightbackground="#d9d9d9",
            highlightcolor="black"
        )

        self.users_list = ScrolledListBox(self.side_frame_t0)
        self.users_list.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.users_list.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font=font10,
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="#d9d9d9",
            selectbackground="#c4c4c4",
            selectforeground="black",
            width=10,
            listvariable=chat_page_support.online_users
        )

    def init_users_list(self, users):
        idx = 0
        for user in users:
            idx += 1
            self.users_list.insert(str(idx), user['username'])

    def init_chat_window(self, chat):
        idx = 0
        for message in chat:
            idx += 1
            if message['type'] == 'message':
                self.insert_message(str(idx), message['username'], message['text'], message['color'])
            elif message['type'] == 'activity':
                self.insert_status(str(idx), message['username'], message['text'])
            else:
                idx -= 1

    def insert_message(self, idx, username, msg, color):
        font_username = "-family {Segoe UI} -size 12 -weight bold -slant " \
                        "roman -underline 0 -overstrike 0"
        self.chat_scrolledtext.configure(state='normal')
        self.chat_scrolledtext.insert(tk.END, username + ': ' + msg + '\n')
        self.chat_scrolledtext.tag_config(username, foreground=color, font=font_username)
        self.chat_scrolledtext.tag_add(username, idx+".0", idx+"."+str(len(username)+1))
        self.chat_scrolledtext.configure(state='disabled')

    def insert_status(self, idx, username, msg):
        font_user_activity = "-family {Segoe UI} -size 10 -weight normal -slant " \
                            "roman -underline 0 -overstrike 0"
        self.chat_scrolledtext.configure(state='normal')
        self.msg = '-- ' + username + ' ' + msg + ' --\n'
        self.chat_scrolledtext.insert(tk.END, self.msg)
        self.chat_scrolledtext.tag_config("start", foreground="grey", font=font_user_activity, justify='center')
        self.chat_scrolledtext.tag_add("start", idx+".0", idx+"." + str(len(self.msg)))
        self.chat_scrolledtext.configure(state='disabled')

    def get_message_text(self):
        message = self.chat_frame_textbox.get('1.0', tk.END)
        self.chat_frame_textbox.delete('1.0', tk.END)
        return message

    def update_chat_window(self, s):
        while True:
            t = yield
            print(t)
            #messageObj = Message(s.recv(1024))
            #self.insert_message(idx, messageObj.username, messageObj.text)

def GUIStart(users, chat):
    global val, w, root, COLOR
    root = tk.Tk()
    root.resizable(width=False, height=False)
    chat_page_support.set_Tk_var()
    window = ChatInterface(root, COLOR)
    window.init_chat_window(chat)
    window.init_users_list(users)

    #updater = Thread(target=top.update_chat_window, args=(soc,))
    #updater.setDaemon(True)
    #updater.start()

    chat_page_support.init(root, window)
    root.mainloop()

def destroy_Main():
    global w
    w.destroy()
    w = None


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

def main():
    users = client.get_users_list()
    chat = client.get_chat_history()
    GUIStart(users, chat)

if __name__ == '__main__':
    main()