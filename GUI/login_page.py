# Created with great help of PAGE.
import sys, client, time
import tkinter as tk
from threading import Thread
try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True
import login_page_support

COLOR = '#bc2626'

class LoginInterface:
    def __init__(self, top=None, color = 'navy'):
        global soc, connection_status

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font10 = "-family {Hobo Std} -size 28 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        font9 = "-family Tahoma -size 11 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        self.background_color = color #'#bc2626'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('vista')

        self.style.configure('.', background=_bgcolor, foreground=_fgcolor, font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active',_ana2color)])

        top.geometry("640x480")
        top.title("GhostsChatApp")
        top.configure(background=self.background_color, highlightbackground="#efefef", highlightcolor="#646464")

        self.main_app_label = tk.Label(top)
        self.main_app_label.place(relx=0.23, rely=0.113, height=73, width=349)
        self.main_app_label.configure(
            activebackground=self.background_color,
            activeforeground="white",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            font=font10,
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='GhostsChatApp!'
        )

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Login_Page = tk.Frame(top)
        self.Login_Page.place(relx=0.0, rely=0.283, relheight=0.65, relwidth=1.08)
        self.Login_Page.configure(
            relief='groove',
            borderwidth="0",
            background=self.background_color,
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            width=645
        )

        self.login_form = tk.LabelFrame(self.Login_Page)
        self.login_form.place(relx=0.17, rely=0.0, relheight=0.803, relwidth=0.582)
        self.login_form.configure(
            relief='groove',
            foreground="#fff",
            text='''Login''',
            background=self.background_color,
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            width=370
        )

        self.user_textbox = tk.Entry(self.login_form)
        self.user_textbox.place(relx=0.054, rely=0.286, height=24, relwidth=0.903, bordermode='ignore')
        self.user_textbox.configure(
            background="#fff",
            borderwidth="2",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectforeground="black"
        )

        self.pass_textbox = tk.Entry(self.login_form)
        self.pass_textbox.place(relx=0.054, rely=0.571, height=24, relwidth=0.903, bordermode='ignore')
        self.pass_textbox.configure(
            background="white",
            borderwidth="2",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="#c4c4c4",
            selectforeground="black",
            show="*"
        )

        self.login_button = tk.Button(self.login_form)
        self.login_button.place(relx=0.37, rely=0.776, height=33, width=116, bordermode='ignore')
        self.login_button.configure(
            activebackground="#d9d9d9",
            activeforeground="#000000",
            background="#c68747",
            borderwidth="1",
            command = lambda: login_page_support.login_handler(self.get_login_data(), soc),
            disabledforeground="#a3a3a3",
            font=font9,
            foreground="#000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            text='''Login'''
        )

        self.login_user_label = tk.Label(self.login_form)
        self.login_user_label.place(relx=0.044, rely=0.19, height=25, width=72, bordermode='ignore')
        self.login_user_label.configure(
            activebackground="#f9f9f9",
            activeforeground="black",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='''Username'''
        )

        self.login_pass_label = tk.Label(self.login_form)
        self.login_pass_label.place(relx=0.044, rely=0.472, height=25, width=68, bordermode='ignore')
        self.login_pass_label.configure(
            activebackground="#f9f9f9",
            activeforeground="black",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='''Password'''
        )

        self.register_switch_btn = tk.Button(self.Login_Page)
        self.register_switch_btn.place(relx=0.543, rely=0.82, height=29, width=162)
        self.register_switch_btn.configure(
            activebackground=self.background_color,
            activeforeground="white",
            background=self.background_color,
            borderwidth="0", cursor='hand2',
            command = lambda: login_page_support.switch_register(self.Register_Page),
            disabledforeground="#a3a3a3",
            foreground="#ffa6a6",
            highlightbackground="#114",
            highlightcolor="black",
            pady="0",
            text='''Register a New Account'''
        )

        self.connection_status_label = tk.Label(top)
        self.connection_status_label.place(relx=0.87, rely=0.94, height=30, width=80)
        self.connection_status_label.configure(
            activebackground=self.background_color,
            activeforeground="white",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            font=font9,
            foreground=connection_status['color'],
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text=connection_status['text']
        )


        self.Register_Page = tk.Frame(top)
        self.Register_Page.lower()
        self.Register_Page.place(relx=0.0, rely=0.283, relheight=0.65, relwidth=1.08)
        self.Register_Page.configure(
            relief='groove',
            borderwidth="0",
            background=self.background_color,
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            width=645
        )

        self.register_form = tk.LabelFrame(self.Register_Page)
        self.register_form.place(relx=0.17, rely=0.0, relheight=0.913, relwidth=0.582)
        self.register_form.configure(
            relief='groove',
            foreground="#fff",
            text='''Signup''',
            background=self.background_color,
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            width=370
        )

        self.reguser_textbox = tk.Entry(self.register_form)
        self.reguser_textbox.place(relx=0.054, rely=0.222, height=24, relwidth=0.903, bordermode='ignore')
        self.reguser_textbox.configure(
            background="#fff",
            borderwidth="2",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="#c4c4c4",
            selectforeground="black"
        )

        self.regpass_textbox = tk.Entry(self.register_form)
        self.regpass_textbox.place(relx=0.054, rely=0.444, height=24, relwidth=0.903, bordermode='ignore')
        self.regpass_textbox.configure(
            background="white",
            borderwidth="2",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="#c4c4c4",
            selectforeground="black",
            show="*"
        )

        self.signup_button = tk.Button(self.register_form)
        self.signup_button.place(relx=0.37, rely=0.825, height=33, width=116, bordermode='ignore')
        self.signup_button.configure(
            activebackground="#d9d9d9",
            activeforeground="#000000",
            background="#e5cadb",
            borderwidth="1",
            command = lambda: login_page_support.register_handler(self.get_registeration_data()),
            disabledforeground="#a3a3a3",
            font=font9,
            foreground="#000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            text='''Signup'''
        )

        self.reg_user_label = tk.Label(self.register_form)
        self.reg_user_label.place(relx=0.044, rely=0.138, height=25, width=72, bordermode='ignore')
        self.reg_user_label.configure(
            activebackground="#f9f9f9",
            activeforeground="black",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='''Username'''
        )

        self.reg_pass_label = tk.Label(self.register_form)
        self.reg_pass_label.place(relx=0.044, rely=0.360, height=25, width=68, bordermode='ignore')
        self.reg_pass_label.configure(
            activebackground="#f9f9f9",
            activeforeground="black",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='''Password'''
        )

        self.reg_age_label = tk.Label(self.register_form)
        self.reg_age_label.place(relx=0.045, rely=0.58, height=25, width=38, bordermode='ignore')
        self.reg_age_label.configure(
            activebackground="#f9f9f9",
            activeforeground="black",
            background=self.background_color,
            disabledforeground="#a3a3a3",
            foreground="#fff",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            text='''Age'''
        )

        self.reg_agebox = ttk.Combobox(self.register_form)
        self.reg_agebox.place(relx=0.054, rely=0.667, relheight=0.083, relwidth=0.911, bordermode='ignore')
        self.value_list = [i for i in range(15,60)]
        self.reg_agebox.configure(
            values=self.value_list,
            textvariable=login_page_support.combobox,
            takefocus=""
        )

        self.login_switch_btn = tk.Button(self.Register_Page)
        self.login_switch_btn.place(relx=0.543, rely=0.928, height=29, width=162)

        self.login_switch_btn.configure(
            activebackground=self.background_color,
            activeforeground="white",
            background=self.background_color,
            borderwidth="0", cursor='hand2',
            command = lambda: login_page_support.switch_login(self.Login_Page),
            disabledforeground="#a3a3a3",
            foreground="#ffa6a6",
            highlightbackground="#114",
            highlightcolor="black",
            pady="0",
            text='''Login Existing Account'''
        )

    def get_login_data(self):
        return {'username':self.user_textbox.get(), 'password':self.pass_textbox.get()}

    def get_registeration_data(self):
        return {'username':self.reguser_textbox.get(), 'password':self.regpass_textbox.get(), 'age':self.reg_agebox.get()}


def GUIStart():
    global val, w, root

    root = tk.Tk()
    root.resizable(width=False, height=False)
    login_page_support.set_Tk_var()

    window = LoginInterface(root, COLOR)
    login_page_support.init(root, window)
    root.mainloop()

def destroy_Main():
    global w
    w.destroy()
    w = None


def main():
    global soc, connection_status
    host, port = '127.0.0.1', 20220
    soc, connection_status = client.connect(host, port)
    GUIStart()

if __name__ == '__main__':
    main()





