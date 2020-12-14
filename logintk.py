from tkinter import *
from steam.client import SteamClient #pip install steam
import logging
import steam.webauth as sw
from steam.enums import EResult
import requests #pip install requests
from PIL import ImageTk,Image  #pip install pillow
import urllib.parse #pip install urllib
import io

Luka = '76561198174496762'
Robin = '76561197960434622'
Joel = '76561198152182165'
Eva = '76561198803753153'
Henry = '76561198074124658'
steamkey = '7139EBA744B55B104024D221C07EFB38'
steamjson = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
client = SteamClient()
logging.basicConfig(format="%(asctime)s | %(message)s", level=logging.INFO)
LOG = logging.getLogger()
# user = sw.WebAuth('username')
#textkleuren
txt = 'white'
wrong = 'red'
maintxt = 'white'
#textfonts
sidefont = ('',15,'bold')
#achtergrondkleuren
backgroundlogin = '#1b2838'
backgroundmain = backgroundlogin
backgroundtest = 'white'
backgroundside = '#101822'
#afmetingen
sidewidth = 240
gamebreedte = 280
iconbreedte = 30
gamenamelength = 20


class login():
    def __init__(self):
        self.root = Tk()
        self.root.title('Steam login')
        # self.root.iconbitmap('steam_logo.ico')
        self.root.resizable(False, False)
        self.root.configure(bg=backgroundlogin)
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
                           bg=backgroundlogin)
        self.frame.pack(expand=True, fill=BOTH)
        usertxt = Label(self.frame,
                        text='Username:',
                        bg=backgroundlogin,
                        fg=txt)
        usertxt.place(relx=0.31, rely=0.2)
        self.username = Entry(self.frame,
                              width=30)
        self.username.place(relx=0.5, rely=0.275, anchor=CENTER)
        self.userwrong = Label(self.frame,
                               bg=backgroundlogin,
                               fg=wrong)
        self.userwrong.place(relx=0.31, rely=0.31)
        passtxt = Label(self.frame,
                        text='Password:',
                        bg=backgroundlogin,
                        fg=txt)
        passtxt.place(relx=0.31, rely=0.5)
        self.password = Entry(self.frame,
                              show="\u2022",
                              width=30)
        self.password.place(relx=0.5, rely=0.575, anchor=CENTER)
        self.passwrong = Label(self.frame,
                               bg=backgroundlogin,
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
                                   bg=backgroundlogin)
                self.frame.pack(expand=True, fill=BOTH)
                authtxt = Label(self.frame,
                                text='Enter 2FA code:',
                                bg=backgroundlogin,
                                fg=txt)
                authtxt.place(relx=0.34, rely=0.25)
                self.authcode = Entry(self.frame,
                                      font=('Helvetica', 20, 'bold'),
                                      justify='center',
                                      textvariable=self.var,
                                      width=10)
                self.authcode.place(relx=0.5, rely=0.35, anchor=CENTER)
                self.var.trace('w', self.autocap)
                self.authwrong = Label(self.frame,
                                       bg=backgroundlogin,
                                       fg=wrong)
                self.authwrong.place(relx=0.34, rely=0.4)
                authback = Button(self.frame,
                                  text='Terug',
                                  width=6,
                                  height=2,
                                  command=self.authgoback)
                authback.place(relx=0.4, rely=0.65, anchor=E)
                authresend = Button(self.frame,
                                    text='Resend',
                                    width=6,
                                    height=2,
                                    command=self.authres)
                authresend.place(relx=0.5, rely=0.65, anchor=CENTER)
                authsubmit = Button(self.frame,
                                    text='Login',
                                    width=6,
                                    height=2,
                                    command=self.authsubmit)
                authsubmit.place(relx=0.6, rely=0.65, anchor=W)
            elif result == EResult.OK:
                self.root.destroy()
                mainscreen(client.steam_id.as_64)
                #vanaf hier doorgaan naar het normale programma
            else:
                print(result)
                self.passwrong['text'] = result


    def autocap(self, *arg):
        self.var.set(self.var.get().upper())


    def authgoback(self):
        self.frame.destroy()
        self.logprompt()
        self.username.insert(0, self.usernameinp)
        self.password.insert(0, self.passwordinp)


    def authsubmit(self):
        self.authwrong['text'] = ''
        twoFAcode = self.authcode.get()
        result = client.login(username=self.usernameinp, password=self.passwordinp, two_factor_code=twoFAcode)
        # print(result)
        if result == EResult.TwoFactorCodeMismatch:
            self.authwrong['text'] = '2FA code is verkeerd'
        elif result == EResult.RateLimitExceeded:
            self.authwrong['text'] = 'Te vaak geprobeerd, probeer later opnieuw'
        elif result == EResult.OK:
            self.root.destroy()
            mainscreen(client.steam_id.as_64)
            # vanaf hier doorgaan naar het normale programma
            client.logout()
        else:
            print(result)
            self.passwrong['text'] = result


    def authres(self):
        client.login(username=self.usernameinp, password=self.passwordinp)


class mainscreen():
    def gamesget(self):
        res = requests.get(steamjson)
        games = res.json()
        self.gamephoto = []
        for i in range(9):
            game = str(games[i]['appid'])
            gameurl = 'https://store.steampowered.com/api/appdetails?appids={}'.format(game)
            resgame = requests.get(gameurl)
            gamejson = resgame.json()
            gamepic = gamejson[game]['data']['header_image']
            raw_data = urllib.request.urlopen(gamepic).read()
            image = Image.open(io.BytesIO(raw_data))
            imagevolgame = ImageTk.PhotoImage(image)
            gameratio = imagevolgame.height() / imagevolgame.width()
            image = image.resize((gamebreedte, int(gamebreedte * gameratio)), Image.ANTIALIAS)
            imagevolgame = ImageTk.PhotoImage(image)
            self.gamephoto.append({'image':imagevolgame, 'appid':game})


    def __init__(self, steamid):
        self.root = Tk()
        self.gamesget()
        self.root.attributes('-fullscreen', True)
        self.root.bind('<F8>', lambda sluiten:self.root.destroy())
        self.root.configure(bg=backgroundmain)
        self.framel = Frame(self.root,
                            bg=backgroundside,
                            width=sidewidth)
        self.framel.pack(side=LEFT, fill=Y)
        self.framer = Frame(self.root,
                            bg=backgroundside,
                            width=sidewidth)
        self.framer.pack(side=RIGHT, fill=Y)
        self.framec = Frame(self.root,
                            bg=backgroundmain)
        self.framec.pack()
        self.gameshow()
        self.getownedgames(steamid)
        self.root.mainloop()


    def gameshow(self):
        self.gamerows = []
        gtext1 = Label(self.framec,
                       text='Games you might like',
                       font=sidefont,
                       fg=maintxt,
                       bg=backgroundmain)
        gtext1.pack(anchor='w', padx=(60,0), pady=(150,0))
        self.framec1 = Frame(self.framec,
                             bg=backgroundmain)
        self.framec1.pack(pady=(10,0))
        self.gamerows.append(self.framec1)
        gtext2 = Label(self.framec,
                       text='What your friends play',
                       font=sidefont,
                       fg=maintxt,
                       bg=backgroundmain)
        gtext2.pack(anchor='w', padx=(60,0), pady=(50,0))
        self.framec2 = Frame(self.framec,
                             bg=backgroundmain)
        self.framec2.pack(pady=(10,0))
        self.gamerows.append(self.framec2)
        gtext3 = Label(self.framec,
                       text='Popular games',
                       font=sidefont,
                       fg=maintxt,
                       bg=backgroundmain)
        gtext3.pack(anchor='w', padx=(60,0), pady=(50,0))
        self.framec3 = Frame(self.framec,
                             bg=backgroundmain)
        self.framec3.pack(pady=(10,0))
        self.gamerows.append(self.framec3)
        for k in self.gamerows:
            self.gameshift(k, 0)


    def gameklik(self, gameid):
        print(gameid)


    def gameleft(self, object, numb):
        numb -= 3
        if numb < 0:
            numb = 6
        self.gameshift(object, numb)


    def gameright(self, object, numb):
        numb += 3
        if numb > 6:
            numb = 0
        self.gameshift(object, numb)


    def gameshift(self, object, numb):
        self.gamepageshow = lambda x: (lambda y: self.gameklik(x))
        gamegoleft = lambda x: (lambda y: self.gameleft(x, numb))
        gamegoright = lambda x: (lambda y: self.gameright(x, numb))
        for j in range(3):
            ind = numb + j
            gamepiccont = self.gamephoto[ind]['image']
            gamepic = Label(object,
                            bg=backgroundmain)
            gamepic.image = gamepiccont
            gamepic.config(image=gamepiccont)
            gamepic.bind('<1>', self.gamepageshow(self.gamephoto[ind]['appid']))
            gamepic.grid(row=1, column=1 + j, padx=15)
        left = Label(object,
                     text='<',
                     bg=backgroundmain,
                     fg='white',
                     font=('', 50))
        left.grid(row=1, column=0)
        left.bind('<1>', gamegoleft(object))
        right = Label(object,
                      text='>',
                      bg=backgroundmain,
                      fg='white',
                      font=('', 50))
        right.grid(row=1, column=4)
        right.bind('<1>', gamegoright(object))


    def getownedgames(self, steamid):
        gamelib = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json&include_appinfo=true'.format(steamkey, steamid)
        res = requests.get(gamelib)
        gamesjson = res.json()
        # print(gamesjson)
        games = gamesjson['response']['games']
        gametitle = Label(self.framel,
                          text='Owned Games:',
                          font=sidefont,
                          fg=maintxt,
                          bg=backgroundside)
        gametitle.place(relx=0.1, rely=0.5, anchor='w')
        ind = 0
        for game in games[:8]:
            gameicurl = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(game['appid'], game['img_icon_url'])
            raw_data1 = urllib.request.urlopen(gameicurl).read()
            image = Image.open(io.BytesIO(raw_data1))
            image = image.resize((iconbreedte, iconbreedte), Image.ANTIALIAS)
            imagevol = ImageTk.PhotoImage(image)
            gamenamevar = game['name']
            if len(gamenamevar) > gamenamelength:
                gamenamevar = '{}...'.format(gamenamevar[:gamenamelength-3])
            gamepic = Label(self.framel,
                            bg=backgroundside)
            gamepic.image = imagevol
            gamepic.configure(image=imagevol)
            gamepic.bind('<1>', self.gamepageshow(game['appid']))
            gamepic.place(relx=0.1, rely=0.53+ind*0.05)
            gamename = Label(self.framel,
                             text=gamenamevar,
                             fg=maintxt,
                             bg=backgroundside)
            gamename.bind('<1>', self.gamepageshow(game['appid']))
            gamename.place(relx=0.25, rely=0.55+ind*0.05, anchor='w')
            ind += 1
        gameplus = Label(self.framel,
                         text='+{} more'.format(gamesjson['response']['game_count']-8),
                         font=sidefont,
                         fg=maintxt,
                         bg=backgroundside)
        gameplus.place(relx=0.1, rely=0.95, anchor='w')



if __name__ == "__main__":
    login()
