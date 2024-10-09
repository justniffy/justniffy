import tkinter

import webbrowser
from tkinter import *
from chat import get_response, bot_name


def makeopen(url):
    webbrowser.open_new(url)


bg_gray = "#00FFFF"
bg_color = "#00FFFF"
txt_color = "#EAECEE"

font = "Helvetica 14"
font_bold = "Helvetica 15 bold"


class chatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("NP.01")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=bg_color)
        self.menu = tkinter.Menu(self.window)
        self.window.config(menu=self.menu)
        self.submenu = tkinter.Menu(self.menu, tearoff=0)
        self.submenu.add_command(label='New chat', command=self.open_new_chat)
        self.menu.add_cascade(label='File', menu=self.submenu)

        # head label
        head_label = Label(self.window, bg=bg_color, fg='black', text="THE 19TH CLAN", font=font_bold, pady=20,)

        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=bg_gray)
        line.place(relwidth=1, rely=0.007, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=3, bg=bg_color, fg='black', font=font, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        #SCROLL BAR
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg= bg_gray, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#B0E0E6", fg='black',font=font)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="send", font=('Comic sans', 20), width=20, bg="#FFFFFF",
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

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
