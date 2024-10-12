import tkinter

import webbrowser
from tkinter import *
from chat import get_response, bot_name


def makeopen(url):
    webbrowser.open_new(url)


# bg_gray = "#00FFFF"
# bg_color = "#00FFFF"
txt_color = "#EAECEE"

font = "Helvetica 14"
font_bold = "Helvetica 15 bold"


class chatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.dark_mode = False
    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("NP.01")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg='white')
        self.menu = tkinter.Menu(self.window)
        self.window.config(menu=self.menu)
        self.submenu = tkinter.Menu(self.menu, tearoff=0)
        self.submenu.add_command(label='New chat', command=self.open_new_chat)
        self.menu.add_cascade(label='File', menu=self.submenu)



        # head label
        self.head_label = tkinter.Label(self.window, bg='white', fg='black', text="THE 19TH CLAN", font=font_bold,
                                        pady=5, justify='center')

        self.head_label.pack(side='top', fill='both',padx=5,pady=5)

        # tiny divider
        line = Label(self.window, width=450)
        line.place(relwidth=1, rely=0.007, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=3, bg='white', fg='black', font=font, padx=5, pady=5)
        # self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        self.text_widget.pack(fill="both", expand=True)

        #SCROLL BAR
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg= "white", height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="white", fg='black',font=font)
        # self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.pack(fill='x', side='left',padx=5,pady=5, expand= True)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        self.send_button = Button(bottom_label, text="send", font=('Comic sans', 20), width=20, bg='white',fg='black',
                             command=lambda: self._on_enter_pressed(None))
        self.send_button.pack(fill='y', side='left',padx=5,pady=5)
        # send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.toggle_button = tkinter.Button(self.window, text="Dark mode", command=self.toggle_dark_mode)
        self.toggle_button.pack(side='top', anchor='nw', padx=5,pady=5)
    #     self.dark_mode = False
    #
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
          self.window.config(bg='#333333')
          self.head_label.config(bg='#333333', fg='#FFFFFF')
          self.toggle_button.config(text='Light Mode', bg='#666666',fg='#FFFFFF')
          self.text_widget.config(bg='#333333', fg='#FFFFFF')
          self.msg_entry.config(bg='#333333', fg='#FFFFFF')
          self.send_button.config(bg='#333333', fg='#FFFFFF')
          # self.window.title('THE 19TH CLAN')
          # self.window.config(font=font_bold, pady=20)
        else:
           self.window.config(bg='#00FFFF')
           self.head_label.config(bg='#00FFFF', fg='black')
           self.toggle_button.config(text='Dark Mode', bg='lightgray',fg='black')
           self.text_widget.config(bg='#00FFFF', fg='black')
           self.msg_entry.config(bg='#00FFFF', fg='black')
           self.send_button.config(bg='#00FFFF', fg='black')

           # just chang d bakgroun bg to white
           # self.window.title('THE 19TH CLAN')

    def open_new_chat(self):

        new_app = chatApplication()

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        link = 'https://wa.me/message/FD4BVE5BDTMKM1'
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n "
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        rsp1 = get_response(msg)[0]
        rsp2 = get_response(msg)[1]

        msg2 = f"{bot_name}: {rsp1}\n\n "
        self.text_widget.configure(state=NORMAL)

        if rsp2 == 'recommendations':
            self.text_widget.insert(END, msg2)
            # self.text_widget.tag_configure("link", foreground="blue",)
            self.text_widget.bind('<Button-1>', lambda e:makeopen('https://wa.me/message/FD4BVE5BDTMKM1'))
        else:
            self.text_widget.insert(END, msg2)

        self.text_widget.bind(lambda e:makeopen({link}))

        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    chat_app = chatApplication()
    chat_app.run()
