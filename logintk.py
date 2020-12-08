from tkinter import *
from steam.client import SteamClient
import logging
import steam.webauth as sw
from steam.enums import EResult

client = SteamClient()
logging.basicConfig(format="%(asctime)s | %(message)s", level=logging.INFO)
LOG = logging.getLogger()
user = sw.WebAuth('username')
background = '#1b2838'
txt = 'white'
wrong = 'red'

class login():
    def __init__(self):
        self.root = Tk()
        self.root.title('Steam login')
        # self.root.iconbitmap('steam_logo.ico')
        self.root.resizable(False, False)
        self.root.configure(bg=background)
        window_height = 350
        window_width = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.usercheck = False
        self.passcheck = False
        self.logprompt()
        self.root.mainloop()


    def logprompt(self):
        self.frame = Frame(self.root,
                           bg=background)
        self.frame.pack(expand=True, fill=BOTH)
        usertxt = Label(self.frame,
                        text='Username:',
                        bg=background,
                        fg=txt)
        usertxt.place(relx=0.31, rely=0.2)
        self.username = Entry(self.frame,
                              width=30)
        self.username.place(relx=0.5, rely=0.275, anchor=CENTER)
        self.userwrong = Label(self.frame,
                               bg=background,
                               fg=wrong)
        self.userwrong.place(relx=0.31, rely=0.31)
        passtxt = Label(self.frame,
                        text='Password:',
                        bg=background,
                        fg=txt)
        passtxt.place(relx=0.31, rely=0.5)
        self.password = Entry(self.frame,
                              show="\u2022",
                              width=30)
        self.password.place(relx=0.5, rely=0.575, anchor=CENTER)
        self.passwrong = Label(self.frame,
                               bg=background,
                               fg=wrong)
        self.passwrong.place(relx=0.31, rely=0.61)
        loginbutton = Button(self.frame,
                             text='login',
                             width=10,
                             height=2,
                             command=self.logingo)
        loginbutton.place(relx=0.5, rely=0.8, anchor=CENTER)


    def logingo(self):
        self.usernameinp = self.username.get()
        self.passwordinp = self.password.get()
        self.userwrong['text'] = ''
        self.passwrong['text'] = ''
        if self.usernameinp == '':
            self.userwrong['text'] = 'Username is leeg'
        if self.passwordinp == '':
            self.passwrong['text'] = 'Password is leeg'
        if self.usernameinp != '' and self.passwordinp != '':
            result = client.login(username=self.usernameinp, password=self.passwordinp)
            if result == EResult.RateLimitExceeded:
                self.passwrong['text'] = 'Te vaak geprobeerd, probeer later opnieuw'
            elif result == EResult.InvalidPassword or result == EResult.PasswordUnset:
                self.passwrong['text'] = 'Username of password is incorrect'
            elif result == EResult.AccountLoginDeniedNeedTwoFactor:
                self.var = StringVar()
                self.frame.destroy()
                self.frame = Frame(self.root,
                                   bg=background)
                self.frame.pack(expand=True, fill=BOTH)
                authtxt = Label(self.frame,
                                text='Enter 2FA code:',
                                bg=background,
                                fg=txt)
                authtxt.place(relx=0.34, rely=0.3)
                self.authcode = Entry(self.frame,
                                      font=('Helvetica', 20, 'bold'),
                                      justify='center',
                                      textvariable=self.var,
                                      width=10)
                self.authcode.place(relx=0.5, rely=0.4, anchor=CENTER)
                self.var.trace('w', self.autocap)
                authback = Button(self.frame,
                                  text='Terug',
                                  width=6,
                                  height=2,
                                  command=self.authgoback)
                authback.place(relx=0.45, rely=0.6, anchor=E)
                authsubmit = Button(self.frame,
                                    text='Login',
                                    width=6,
                                    height=2,
                                    command=self.authsubmit)
                authsubmit.place(relx=0.55, rely=0.6, anchor=W)
            else:
                pass #vanaf hier doorgaan naar het normale programma


    def autocap(self, *arg):
        self.var.set(self.var.get().upper())


    def authgoback(self):
        self.frame.destroy()
        self.logprompt()
        self.username.insert(0, self.usernameinp)
        self.password.insert(0, self.passwordinp)


    def authsubmit(self):
        twoFAcode = self.authcode.get()
        client.login(username=self.usernameinp, password=self.passwordinp, two_factor_code=twoFAcode)
        print(client.user.name)
        print(client.steam_id.as_64)
        # vanaf hier doorgaan naar het normale programma
        client.logout()



if __name__ == "__main__":
    login()