from tkinter import *
from tkinter import ttk
from steam.client import SteamClient #pip install steam
#pip install google-cloud
#pip install google-cloud-
#pip install steam[client]
from steam.enums import EResult
import requests #pip install requests
from PIL import ImageTk,Image  #pip install pillow
import urllib.parse #pip install urllib
import io
import atexit
from bs4 import BeautifulSoup #pip install lxml
import random
import math
from datetime import datetime
import matplotlib.pyplot as plt #pip install matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from textwrap import wrap

Luka = '76561198174496762'
Luka2 = '76561198371592493'
Robin = '76561197960434622'
Joel = '76561198152182165'
Eva = '76561198803753153'
Henry = '76561198074124658'
# steamkey = '7139EBA744B55B104024D221C07EFB38'
steamkey = '783790D02B11E668DE41726C35D66B15'
steamjson = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
steamlogo = 'https://www.eaolthof.nl/wp-content/uploads/2021/01/steam3.png'
steamlogostart = 'https://www.eaolthof.nl/wp-content/uploads/2021/01/steam2.png'
client = SteamClient()
language = 'en'
#textkleuren
txt = 'white'
wrong = 'red'
maintxt = 'white'
#textfonts
sidefont = ('',15,'bold')
gamepagetitlefont = ('',20,'bold')
searchbarfont = ('',16)
profilefont = ('',12,'bold')
logoutfont = ('',11,'bold')
gamepagefont = ('',16)
discountfont = ('',12,'overstrike')
discountpercentfont = ('',30,'bold')
fulldescriptionfont = ('',12)
searchgamefont = ('',13,'bold')
tagfont = ('',10,'bold')
personpagefont = ('',20)
#achtergrondkleuren
backgroundlogin = '#1b2838'
backgroundmain = backgroundlogin
backgroundtest = 'white'
backgroundside = '#101822'
backgroundsearchgame = '#2c3e52'
# backgroundprofile = '#171e29'
backgroundprofile = '#1f2e3e'
onlinecolor = '#57cbde'
gameplaycolor = '#a3cf06'
#afmetingen
sidewidth = 240
gamebreedte = 260
gamepagebreedte = 300
iconbreedte = 30
iconbreedtemore = 50
profilepicbreedte = 60
personprofilebreedte = 200
screenshotbreedte = 300
gamenamelength = 20
namelength = gamenamelength
steamlogowidth = 150
loginglogowidth = 250
gameratio = 215/460  #height/width
screenshotratio = 338/600
#algemene variabelen


class general():
    def getjson(self, link):
        res = requests.get(link)
        info = res.json()
        return info


    def getimage(self, link, width, height, rotation):
        raw_data = urllib.request.urlopen(link).read()
        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((width, height), Image.ANTIALIAS)
        image = image.rotate(rotation)
        return ImageTk.PhotoImage(image)


    def QuickSort(self, lst, key, ascending=True, disregardtype=False):
        if not lst:
            return []
        else:
            pivot = (len(lst) // 2)
            pivot_value = lst[pivot]
            if type(pivot_value[key]) is str and disregardtype is False:
                lesser = self.QuickSort(self, [l for i, l in enumerate(lst)
                                               if l[key].lower() < pivot_value[key].lower() and i != pivot], key.lower())
                greater = self.QuickSort(self, [l for l in lst if l[key].lower() > pivot_value[key].lower()], key.lower())
                equal = [l for l in lst if l[key].lower() == pivot_value[key].lower()]
            else:
                lesser = self.QuickSort(self, [l for i, l in enumerate(lst)
                                               if l[key] < pivot_value[key] and i != pivot], key)
                greater = self.QuickSort(self, [l for l in lst if l[key] > pivot_value[key]], key)
                equal = [l for l in lst if l[key] == pivot_value[key]]
            newlst = lesser + equal + greater
            if not ascending:
                newlst.reverse()
            return newlst


    def binarysearch(self, lst, key, target):
        new_lst = lst.copy()
        aver = int((len(lst) - 1) / 2)
        if new_lst != []:
            if target == new_lst[aver][key]:
                return new_lst[aver]
            elif aver >= len(lst) - 1:
                return False
            elif target > new_lst[aver][key]:
                return self.binarysearch(self, new_lst[aver + 1:], key, target)
            else:
                return self.binarysearch(self, new_lst[:aver], key, target)
        return False


    def average(self, lst):
        '''Telt alle items van de list bij elkaar op en deelt die door het aantal items'''
        aver = sum(lst)/len(lst)
        return aver


    def median(self, lst):
        '''Berekent de middelste waarde'''
        sortlst = sorted(lst)
        if len(lst)%2 == 0:
            outcome = (sortlst[len(sortlst)//2]+sortlst[len(sortlst)//2+1])/2
        else:
            outcome = sortlst[len(sortlst)//2+1]
        return float(outcome)


    def var(self, lst):
        '''De variantie wordt berekent voor elke waarneming het verschil met het gemiddelde te nemen. Vervolgens
        kwadrateer je die en tel je de verschillen bij elkaar op. Dit deel je dan door het aantal waarnemingen.'''
        gemiddelde = self.average(self, lst)
        sum = 0
        for num in lst:
            dif = abs(num - gemiddelde)
            sum += dif ** 2
        return float(sum / len(lst))


    def std(self, lst):
        '''De standaardafwijking is de wortel van de variantie'''
        return float(self.var(self, lst) ** 0.5)


class login():
    remember = 0
    username = ''
    loginkey = None
    def __init__(self):
        with open('session.txt', 'r') as sessioncheck:
            session = sessioncheck.read()
        self.sessiondata = session.split('\n')
        try:
            login.remember = self.sessiondata[0]
            login.username = self.sessiondata[1]
            login.loginkey = self.sessiondata[2]
        except:
            pass
        if self.sessiondata[0] == '1':
            result = client.login(username=self.sessiondata[1], login_key=self.sessiondata[2])
            if result != EResult.OK:
                self.logscreen()
            else:
                self.loginfinal()
        else:
            self.logscreen()


    def logscreen(self):
        self.root = Tk()
        self.root.title('Steam login')
        # self.root.iconbitmap('steam_logo.ico')
        self.root.resizable(False, False)
        self.root.configure(bg=backgroundlogin)
        window_height = 500
        window_width = 750
        self.loginscreenlogo = general.getimage(general, steamlogostart, loginglogowidth, int(loginglogowidth*69/191), 0)
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
        loginlogo = Label(self.frame,
                          bg=backgroundlogin)
        loginlogo.image = self.loginscreenlogo
        loginlogo.configure(image=self.loginscreenlogo)
        loginlogo.place(relx=0.5, rely=0.2, anchor='center')
        usertxt = Label(self.frame,
                        text='Username:',
                        font=profilefont,
                        bg=backgroundlogin,
                        fg=txt)
        usertxt.place(relx=0.255, rely=0.32)
        self.username = Entry(self.frame,
                              font=gamepagefont,
                              width=30)
        self.username.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.userwrong = Label(self.frame,
                               font=profilefont,
                               bg=backgroundlogin,
                               fg=wrong)
        self.userwrong.place(relx=0.255, rely=0.43)
        passtxt = Label(self.frame,
                        text='Password:',
                        font=profilefont,
                        bg=backgroundlogin,
                        fg=txt)
        passtxt.place(relx=0.255, rely=0.52)
        self.password = Entry(self.frame,
                              font=gamepagefont,
                              show="\u2022",
                              width=30)
        self.password.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.passwrong = Label(self.frame,
                               font=profilefont,
                               bg=backgroundlogin,
                               fg=wrong)
        self.passwrong.place(relx=0.255, rely=0.63)
        self.rem = IntVar()
        remember = Checkbutton(self.frame,
                               font=gamepagetitlefont,
                               bg=backgroundlogin,
                               activebackground=backgroundlogin,
                               bd=0,
                               variable=self.rem)
        remember.place(relx=0.255, rely=0.7)
        remembertxt = Label(self.frame,
                            text='Stay logged in',
                            font=profilefont,
                            fg=txt,
                            bg=backgroundlogin)
        remembertxt.place(relx=0.28, rely=0.72)
        loginbutton = Label(self.frame,
                            text='Login',
                            font=sidefont,
                            fg=maintxt,
                            bg=backgroundside,
                            width=7,
                            height=2)
        loginbutton.place(relx=0.74, rely=0.8, anchor='e')
        loginbutton.bind('<1>', lambda x:self.logingo())


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
                loginlogo = Label(self.frame,
                                  bg=backgroundlogin)
                loginlogo.image = self.loginscreenlogo
                loginlogo.configure(image=self.loginscreenlogo)
                loginlogo.place(relx=0.5, rely=0.2, anchor='center')
                authtxt = Label(self.frame,
                                text='Enter 2FA code:',
                                font=profilefont,
                                bg=backgroundlogin,
                                fg=txt)
                authtxt.place(relx=0.335, rely=0.39)
                self.authcode = Entry(self.frame,
                                      font=('Helvetica', 32, 'bold'),
                                      justify='center',
                                      textvariable=self.var,
                                      width=10)
                self.authcode.place(relx=0.5, rely=0.5, anchor=CENTER)
                self.var.trace('w', self.autocap)
                self.authwrong = Label(self.frame,
                                       font=profilefont,
                                       bg=backgroundlogin,
                                       fg=wrong)
                self.authwrong.place(relx=0.335, rely=0.57)
                authback = Label(self.frame,
                                 text='Terug',
                                 font=sidefont,
                                 fg=maintxt,
                                 bg=backgroundside,
                                 width=7,
                                 height=2)
                authback.place(relx=0.26, rely=0.75, anchor='w')
                authback.bind('<1>', lambda x:self.authgoback())
                authresend = Label(self.frame,
                                   text='Resend',
                                   font=sidefont,
                                   fg=maintxt,
                                   bg=backgroundside,
                                   width=7,
                                   height=2)
                authresend.place(relx=0.5, rely=0.75, anchor='center')
                authresend.bind('<1>', lambda x:self.authres())
                authsubmit = Label(self.frame,
                                   text='Login',
                                   font=sidefont,
                                   fg=maintxt,
                                   bg=backgroundside,
                                   width=7,
                                   height=2)
                authsubmit.place(relx=0.74, rely=0.75, anchor='e')
                authsubmit.bind('<1>', lambda x:self.authsubmit())
            elif result == EResult.OK:
                self.root.destroy()
                self.loginfinal()
            else:
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
        if result == EResult.TwoFactorCodeMismatch:
            self.authwrong['text'] = '2FA code is verkeerd'
        elif result == EResult.RateLimitExceeded:
            self.authwrong['text'] = 'Te vaak geprobeerd, probeer later opnieuw'
        elif result == EResult.OK:
            self.root.destroy()
            self.loginfinal()
        else:
            self.passwrong['text'] = result


    def authres(self):
        client.login(username=self.usernameinp, password=self.passwordinp)


    def loginfinal(self):
        try:
            login.remember = self.rem.get()
        except:
            login.remember = '1'
        mainscreen(client.steam_id.as_64)


class mainscreen():
    gamesjson = {}
    arrowpicture = 'https://www.eaolthof.nl/wp-content/uploads/2021/01/pijl.jpg'
    gamelist = []
    friendlist = []
    def gamesget(self):
        games = general.getjson(general, steamjson)
        mainscreen.gamesjson = games
        allgamelist = []
        popsort = general.QuickSort(general, games, 'positive_ratings', ascending=False)
        games = self.gamesjson['response']['games']
        popgamesnotinlib = []
        added = []
        for game in games:
            mainscreen.gamelist.append(game['appid'])
        for game in popsort:
            if game['appid'] not in mainscreen.gamelist:
                gameurl = 'https://store.steampowered.com/api/appdetails?appids={}&language={}'.format(game['appid'],
                                                                                                       language)
                gamejson = general.getjson(general, gameurl)
                gamepic = gamejson[str(game['appid'])]['data']['header_image']
                imagevolgame = general.getimage(general, gamepic, gamebreedte, int(gamebreedte * gameratio), 0)
                popgamesnotinlib.append({'image': imagevolgame, 'appid': game['appid']})
                added.append(game['appid'])
            if len(popgamesnotinlib) >= 9:
                break
        friendplays = []
        breakout = False
        for friend in mainscreen.friendlist:
            friendrecentgameurl = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={}&steamid={}&format=json'.format(
                steamkey, friend)
            recentgames = general.getjson(general, friendrecentgameurl)
            if recentgames['response'] != {}:
                for item in recentgames['response']['games']:
                    if item['appid'] not in mainscreen.gamelist:
                        gameurl = 'https://store.steampowered.com/api/appdetails?appids={}&language={}'.format(
                            item['appid'],
                            language)
                        gamejson = general.getjson(general, gameurl)
                        gamepic = gamejson[str(item['appid'])]['data']['header_image']
                        imagevolgame = general.getimage(general, gamepic, gamebreedte, int(gamebreedte * gameratio), 0)
                        friendplays.append({'image': imagevolgame, 'appid': item['appid']})
                    if len(friendplays) >= 9:
                        breakout = True
                        break
            if breakout:
                break
        suggested = []
        tobreak = False
        for game in self.favorgames:
            gameinfile = general.binarysearch(general, mainscreen.gamesjson, 'appid', game['appid'])
            tagtosearch = random.choice(gameinfile['steamspy_tags'].split(';'))
            currentlength = len(suggested)
            for item in popsort:
                if tagtosearch in item['steamspy_tags']:
                    if item['appid'] not in mainscreen.gamelist and item['appid'] not in added:
                            gameurl = 'https://store.steampowered.com/api/appdetails?appids={}&language={}'.format(
                                item['appid'],
                                language)
                            gamejson = general.getjson(general, gameurl)
                            gamepic = gamejson[str(item['appid'])]['data']['header_image']
                            imagevolgame = general.getimage(general, gamepic, gamebreedte, int(gamebreedte * gameratio), 0)
                            suggested.append({'image': imagevolgame, 'appid': item['appid']})
                            added.append(item['appid'])
                if len(suggested) >= currentlength + 3:
                    if len(suggested) >= 9:
                        tobreak = True
                    break
            if tobreak:
                break
        allgamelist.append(suggested)
        allgamelist.append(friendplays)
        allgamelist.append(popgamesnotinlib)
        return allgamelist


    def __init__(self, steamid):
        self.root = Tk()
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
        imagevol = general.getimage(general, steamlogo, steamlogowidth, int(steamlogowidth*69/191), 0)
        self.steamlog = Label(self.framel,
                              bg=backgroundside)
        self.steamlog.image = imagevol
        self.steamlog.configure(image=imagevol)
        self.steamlog.place(relx=0.5, rely=0.075, anchor='center')
        self.steamlog.bind('<1>', lambda x:self.gameshow())
        self.arrowleft = general.getimage(general, mainscreen.arrowpicture, 80, 80, 180)
        self.arrowright = general.getimage(general, mainscreen.arrowpicture, 80, 80, 0)
        self.gamesidetitleshow(steamid)
        self.friendtitleshow(steamid)
        self.gamephoto = self.gamesget()
        self.gameshow()
        self.root.mainloop()


    def cleanscreen(self):
        self.framecunder.destroy()
        self.framecunder = Frame(self.root,
                            bg=backgroundmain)
        self.framecunder.pack(expand=1, fill=BOTH)


    def gameshow(self):
        self.gamerows = []
        try:
            self.framecunder.destroy()
        except:
            pass
        self.framecunder = Frame(self.root,
                            bg=backgroundmain)
        self.framecunder.pack(expand=1, fill=BOTH)
        self.framec = Frame(self.framecunder,
                            bg=backgroundmain)
        self.framec.pack()
        self.framesearch = Frame(self.framec,
                                 bg=backgroundmain)
        self.framesearch.pack(fill=X, expand=1)
        gtext1 = Label(self.framesearch,
                       text='Games you might like',
                       font=sidefont,
                       fg=maintxt,
                       bg=backgroundmain)
        gtext1.grid(row=0, column=0, padx=(100,0), pady=(150,10), sticky='w')
        searchbar = Entry(self.framesearch,
                          font=searchbarfont,
                          width=19,
                          borderwidth=0,
                          insertbackground=maintxt,
                          fg=maintxt,
                          bg=backgroundside)
        searchbar.grid(row=0, column=1, padx=(380,0), pady=(150,10), sticky='e')
        searchbar.bind('<Return>', lambda x: searchscreen(self.framec, self.framecunder, searchbar.get()))
        searchicon = 'https://www.eaolthof.nl/wp-content/uploads/2021/01/zoek2.png'
        searchimage = general.getimage(general, searchicon, 35, 35, 0)
        searchic = Label(self.framesearch,
                         bg=backgroundmain)
        searchic.image = searchimage
        searchic.configure(image=searchimage)
        searchic.grid(row=0, column=2, pady=(140,0), sticky='w')
        searchic.bind('<1>', lambda x:searchscreen(self.framec, self.framecunder, searchbar.get()))
        self.framec1 = Frame(self.framec,
                             bg=backgroundmain)
        self.framec1.pack()
        self.gamerows.append(self.framec1)
        gtext2 = Label(self.framec,
                       text='What your friends play',
                       font=sidefont,
                       fg=maintxt,
                       bg=backgroundmain)
        gtext2.pack(anchor='w', padx=(100,0), pady=(50,0))
        self.framec2 = Frame(self.framec,
                             bg=backgroundmain)
        self.framec2.pack(pady=(10,0))
        self.gamerows.append(self.framec2)
        gtext3 = Label(self.framec,
                       text='Popular games',
                       font=sidefont,
                       fg=maintxt,
                       bg=backgroundmain)
        gtext3.pack(anchor='w', padx=(100,0), pady=(50,0))
        self.framec3 = Frame(self.framec,
                             bg=backgroundmain)
        self.framec3.pack(pady=(10,0))
        self.gamerows.append(self.framec3)
        for x in range(3):
            self.gameshift(self.gamerows[x], 0, self.gamephoto[x])


    def gameclick(self, gameid):
        self.cleanscreen()
        gamescreen(self.framec, self.framecunder, gameid)


    def gameleft(self, object, numb, gamelist):
        numb -= 3
        if numb < 0:
            numb = 6
        self.gameshift(object, numb, gamelist)


    def gameright(self, object, numb, gamelist):
        numb += 3
        if numb > 6:
            numb = 0
        self.gameshift(object, numb, gamelist)


    def gameshift(self, object, numb, gamelist):
        gamegoleft = lambda x: (lambda y: self.gameleft(x, numb, gamelist))
        gamegoright = lambda x: (lambda y: self.gameright(x, numb, gamelist))
        for j in range(3):
            ind = numb + j
            gamepiccont = gamelist[ind]['image']
            gamepic = Label(object,
                            bg=backgroundmain)
            gamepic.image = gamepiccont
            gamepic.configure(image=gamepiccont)
            gamepic.bind('<1>', self.gamepageshow(gamelist[ind]['appid']))
            gamepic.grid(row=1, column=1 + j, padx=15)
        left = Label(object,
                     bg=backgroundmain)
        left.image = self.arrowleft
        left.configure(image=self.arrowleft)
        left.grid(row=1, column=0)
        left.bind('<1>', gamegoleft(object))
        right = Label(object,
                      bg=backgroundmain)
        right.image = self.arrowright
        right.configure(image=self.arrowright)
        right.grid(row=1, column=4)
        right.bind('<1>', gamegoright(object))


    def getownedgames(self, steamid):
        gamelib = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json&include_appinfo=true&include_played_free_games=true'.format(steamkey, steamid)
        gamesjson = general.getjson(general, gamelib)
        return gamesjson


    def gamesidetitleshow(self, steamid):
        self.gamepageshow = lambda x: (lambda y: self.gameclick(x))
        self.ownedgamepage = lambda x: (lambda y: self.ownedgameclick(x))
        self.gamesjson = self.getownedgames(steamid)
        self.sortedgames = general.QuickSort(general, self.gamesjson['response']['games'], 'appid')
        games = self.gamesjson['response']['games']
        gametitle = Label(self.framel,
                          text='Owned Games',
                          font=sidefont,
                          fg=maintxt,
                          bg=backgroundside)
        gametitle.place(relx=0.1, rely=0.5, anchor='w')
        if self.gamesjson['response']['game_count'] > 8:
            gameplus = Label(self.framel,
                             text='+{} more'.format(self.gamesjson['response']['game_count']-8),
                             font=sidefont,
                             fg=maintxt,
                             bg=backgroundside)
            gameplus.place(relx=0.1, rely=0.95, anchor='w')
            gameplus.bind('<1>', lambda x:self.gamemoreclick())
        self.gamesideshow(games[:8], 0.53)
        self.gamefavorites()


    def gamesideshow(self, games, y):
        ind=0
        for game in games:
            gameicurl = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(game['appid'], game['img_icon_url'])
            imagevol = general.getimage(general, gameicurl, iconbreedte, iconbreedte, 0)
            gamenamevar = game['name']
            if len(gamenamevar) > gamenamelength:
                gamenamevar = '{}...'.format(gamenamevar[:gamenamelength-3])
            gamepic = Label(self.framel,
                            bg=backgroundside)
            gamepic.image = imagevol
            gamepic.configure(image=imagevol)
            gamepic.bind('<1>', self.ownedgamepage(game['appid']))
            gamepic.place(relx=0.1, rely=y+ind*0.05)
            gamename = Label(self.framel,
                             text=gamenamevar,
                             fg=maintxt,
                             bg=backgroundside)
            gamename.bind('<1>', self.ownedgamepage(game['appid']))
            gamename.place(relx=0.25, rely=y+0.02+ind*0.05, anchor='w')
            ind += 1


    def gamemoreclick(self):
        self.cleanscreen()
        showfulllist(self.framec, self.framecunder, self.gamesjson, 'games', 'Your library')


    def gamefavorites(self):
        games = self.gamesjson['response']['games']
        fav_games = general.QuickSort(general, games, 'playtime_forever', ascending=False)
        self.favorgames = fav_games[:3]
        favortitle = Label(self.framel,
                           text='Favorite games',
                           font=sidefont,
                           bg=backgroundside,
                           fg=maintxt)
        favortitle.place(relx=0.1, rely=0.2, anchor='w')
        self.gamesideshow(self.favorgames, 0.23)


    def getfriends(self, steamid):
        friendurl = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend'.format(steamkey, steamid)
        friendjson = general.getjson(general, friendurl)
        for friend in friendjson['friendslist']['friends']:
            mainscreen.friendlist.append(friend['steamid'])
        return friendjson


    def friendtitleshow(self, steamid):
        friends = self.getfriends(steamid)['friendslist']['friends']
        personpagesurl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids='.format(steamkey)
        for friend in friends:
            personpagesurl += '{},'.format(friend['steamid'])
        personsjson = general.getjson(general, personpagesurl)
        persons = personsjson['response']['players']
        persons = general.QuickSort(general, persons, 'personastate', ascending=False)
        self.new_personlst = []
        for person in persons:
            if 'gameextrainfo' in person.keys():
                gameplaying = person['gameextrainfo']
                self.new_personlst.insert(0, {'id':person['steamid'],
                                              'name':person['personaname'],
                                              'picture':person['avatar'],
                                              'dict':person,
                                              'personastate':person['personastate'],
                                              'gameplaying':gameplaying,
                                              'gameplayingid':person['gameid']})
            else:
                gameplaying = ''
                self.new_personlst.append({'id':person['steamid'],
                                           'name':person['personaname'],
                                           'picture':person['avatar'],
                                           'dict': person,
                                           'personastate':person['personastate'],
                                           'gameplaying':gameplaying})
        friendtitle = Label(self.framer,
                          text='Friends',
                          font=sidefont,
                          fg=maintxt,
                          bg=backgroundside)
        friendtitle.place(relx=0.1, rely=0.1, anchor='w')
        if len(self.new_personlst) > 8:
            friendplus = Label(self.framer,
                             text='+{} more'.format(len(self.new_personlst)-8),
                             font=sidefont,
                             fg=maintxt,
                             bg=backgroundside)
            friendplus.place(relx=0.1, rely=0.55, anchor='w')
            friendplus.bind('<1>', lambda x:self.friendmoreclick())
        userurl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(steamkey, client.steam_id.as_64)
        userjson = general.getjson(general, userurl)
        userinfo = userjson['response']['players'][0]
        ownname = userinfo['personaname']
        if len(ownname) > 12:
            ownname = '{}...'.format(ownname[:9])
        username = Label(self.framer,
                         text=ownname,
                         font=profilefont,
                         fg=maintxt,
                         bg=backgroundside)
        username.place(relx=0.575, rely=0.925, anchor='e')
        username.bind('<1>', lambda x:self.friendclick(userinfo['steamid']))
        userlogout = Label(self.framer,
                           text='Logout',
                           font=logoutfont,
                           fg='gray',
                           bg=backgroundside)
        userlogout.place(relx=0.575, rely=0.95, anchor='e')
        userlogout.bind('<1>', lambda x:self.logout())
        userquit = Label(self.framer,
                           text='Quit',
                           font=logoutfont,
                           fg='gray',
                           bg=backgroundside)
        userquit.place(relx=0.95, rely=0.02, anchor='e')
        userquit.bind('<1>', lambda x:self.root.destroy())
        minimize = Label(self.framer,
                           text='Minimize',
                           font=logoutfont,
                           fg='gray',
                           bg=backgroundside)
        minimize.place(relx=0.05, rely=0.02, anchor='w')
        minimize.bind('<1>', lambda x:self.root.iconify())
        image = general.getimage(general, userinfo['avatar'], profilepicbreedte, profilepicbreedte, 0)
        userpicture = Label(self.framer,
                            bg=backgroundmain)
        userpicture.image = image
        userpicture.configure(image=image)
        userpicture.place(relx=0.6, rely=0.9)
        userpicture.bind('<1>', lambda x: self.friendclick(userinfo['steamid']))
        self.showfriends(self.new_personlst[:8], 0.13)


    def showfriends(self, friends, y):
        self.friendpageshow = lambda x: (lambda y: self.friendclick(x))
        ind = 0
        for person in friends:
            profilepicurl = person['picture']
            imagevol = general.getimage(general, profilepicurl, iconbreedte, iconbreedte, 0)
            profilename = person['name']
            if len(profilename) > namelength:
                profilename = '{}...'.format(profilename[:namelength-3])
            if person['personastate'] > 0:
                if person['gameplaying'] =='':
                    bordercolor = '#57cbde'
                else:
                    bordercolor = '#a3cf06'
                    game = person['gameplaying']
                    if len(game) > 20:
                        game = '{}...'.format(game[:17])
                    playinggame = Label(self.framer,
                                        text=game,
                                        font=('',7),
                                        fg=bordercolor,
                                        bg=backgroundside)
                    playinggame.place(relx=0.25, rely=y+0.0275+ind*0.05)
                    playinggame.bind('<1>', self.gamepageshow(person['gameplayingid']))
                friendborder = Label(self.framer,
                                     font=('',20),
                                     bg=bordercolor,
                                     width=2,
                                     height=1)
                friendborder.place(relx=0.09, rely=y-0.002+ind*0.05)
            else:
                bordercolor = maintxt
            friendpic = Label(self.framer,
                            bg=backgroundside)
            friendpic.image = imagevol
            friendpic.configure(image=imagevol)
            friendpic.bind('<1>', self.friendpageshow(person['id']))
            friendpic.place(relx=0.1, rely=y+ind*0.05)
            friendname = Label(self.framer,
                             text=profilename,
                             fg=bordercolor,
                             bg=backgroundside)
            friendname.bind('<1>', self.friendpageshow(person['id']))
            friendname.place(relx=0.25, rely=y+0.02+ind*0.05, anchor='w')
            ind += 1


    def friendmoreclick(self):
        self.cleanscreen()
        list = self.new_personlst.copy()
        for friend in list:
            friend['dict'] = friend['id']
        showfulllist(self.framec, self.framecunder, self.new_personlst, 'friends', 'Your friends')


    def friendclick(self, steamid):
        self.cleanscreen()
        personscreen(self.framec, self.framecunder, steamid)


    def ownedgameclick(self, gameid):
        self.cleanscreen()
        librarygame(self.framec, self.framecunder, general.binarysearch(general, self.sortedgames, 'appid', gameid))


    def logout(self):
        client.logout()
        self.root.destroy()
        with open('session.txt', 'w') as sessionfile:
            sessionfile.write('0\nNone\nNone')
        login()


class showfulllist():
    def __init__(self, frame, root, dict, mode, title):
        frame.destroy()
        self.root = root
        self.cleanscreen()
        if mode == 'games':
            self.showgames(dict, title)
        elif mode == 'friends':
            self.showfriends(dict, title)


    def showgames(self, dict, title):
        gamelist = dict['response']['games']
        self.clickaction = lambda x: (lambda y: librarygame(self.framec, self.root, x))
        self.gamepictures = []
        for game in gamelist:
            gameicurl = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(
                game['appid'], game['img_icon_url'])
            imagevol = general.getimage(general, gameicurl, iconbreedtemore, iconbreedtemore, 0)
            self.gamepictures.append({'id':str(game['appid']),
                                      'name':game['name'],
                                      'picture':imagevol,
                                      'dict':game})
        self.startindex = 0
        self.displayinfo(self.gamepictures, self.startindex, title)


    def showfriends(self, dict, title):
        self.clickaction = lambda x: (lambda y: personscreen(self.framec, self.root, x))
        for friend in dict:
            if type(friend['picture']) == str:
                profilepicurl = friend['picture']
                imagevol = general.getimage(general, profilepicurl, iconbreedtemore, iconbreedtemore, 0)
                friend['picture'] = imagevol
            else:
                break
        self.startindex = 0
        self.displayinfo(dict, self.startindex, title)


    def displayinfo(self, dict, startindex, title):
        arrowup = False
        arrowdown = True
        self.arrowupimage = general.getimage(general, mainscreen.arrowpicture, 80, 80, 90)
        self.arrowdownimage = general.getimage(general, mainscreen.arrowpicture, 80, 80, 270)
        pagetitle = Label(self.framec,
                              text=title,
                              font=gamepagetitlefont,
                              fg=maintxt,
                              bg=backgroundmain)
        pagetitle.place(relx=0.05, rely=0.1)
        for x in range(5):
            for y in range(3):
                index = startindex + 3 * x + y
                if index >= len(dict):
                    arrowdown = False
                    break
                image = dict[index]['picture']
                gamename = dict[index]['name']
                if len(gamename) > gamenamelength:
                    gamename = '{}...'.format(gamename[:gamenamelength-3])
                bordercolor = maintxt
                if 'personastate' in dict[index].keys():
                    if dict[index]['personastate'] > 0:
                        if dict[index]['gameplaying'] == '':
                            bordercolor = '#57cbde'
                        else:
                            bordercolor = '#a3cf06'
                        friendborder = Label(self.framec,
                                             font=('', 35),
                                             bg=bordercolor,
                                             width=2,
                                             height=1)
                        friendborder.place(relx=0.047+y*0.32, rely=0.2475+x*0.12)
                        game = dict[index]['gameplaying']
                        if len(game) > 20:
                            game = '{}...'.format(game[:17])
                        playinggame = Label(self.framec,
                                            text=game,
                                            font=('',11),
                                            fg=bordercolor,
                                            bg=backgroundmain)
                        playinggame.place(relx=0.11+y*0.32, rely=0.295+x*0.12)
                gameicon = Label(self.framec,
                                 bg=backgroundmain)
                gameicon.image = image
                gameicon.configure(image=image)
                gameicon.place(relx=0.05+y*0.32, rely=0.25+x*0.12)
                gameicon.bind('<1>', self.clickaction(dict[index]['dict']))
                gamenamedisplay = Label(self.framec,
                                        text=gamename,
                                        font=gamepagefont,
                                        fg=bordercolor,
                                        bg=backgroundmain)
                gamenamedisplay.place(relx=0.11+y*0.32, rely=0.265+x*0.12)
                gamenamedisplay.bind('<1>', self.clickaction(dict[index]['dict']))
        if dict[:index+1] != dict[startindex:index+1]:
            arrowup = True
        if arrowup:
            arrowpageup = Label(self.framec,
                                bg=backgroundmain)
            arrowpageup.image = self.arrowupimage
            arrowpageup.configure(image=self.arrowupimage)
            arrowpageup.bind('<1>', lambda a:self.dictup(dict, title))
            arrowpageup.place(relx=0.5, rely=0.18, anchor='center')
        if arrowdown:
            arrowpagedown = Label(self.framec,
                                bg=backgroundmain)
            arrowpagedown.image = self.arrowdownimage
            arrowpagedown.configure(image=self.arrowdownimage)
            arrowpagedown.bind('<1>', lambda a:self.dictdown(dict, title))
            arrowpagedown.place(relx=0.5, rely=0.86, anchor='center')


    def dictup(self, dict, title):
        self.startindex -= 15
        self.cleanscreen()
        self.displayinfo(dict, self.startindex, title)


    def dictdown(self, dict, title):
        self.startindex += 15
        self.cleanscreen()
        self.displayinfo(dict, self.startindex, title)


    def cleanscreen(self):
        try:
            self.framec.destroy()
        except:
            pass
        self.framec = Frame(self.root,
                            bg=backgroundmain)
        self.framec.pack(fill=BOTH, expand=1)


class gamescreen():
    def __init__(self, frame, root, appid):
        frame.destroy()
        self.root = root
        try:
            self.framec.destroy()
        except:
            pass
        self.framec = Frame(self.root,
                            bg=backgroundmain)
        self.framec.pack(fill=BOTH, expand=1)
        self.framedesc = Frame(self.root,
                               bg=backgroundmain)
        self.framedesc.forget()
        self.displaygameinfo(appid)
        self.showfulldescription(appid)


    def getgameinfo(self, appid):
        gameurl = 'https://store.steampowered.com/api/appdetails?appids={}&language={}'.format(appid, language)
        return general.getjson(general, gameurl)


    def displaygameinfo(self, appid):
        self.gameinfo = self.getgameinfo(appid)
        steamjson = general.binarysearch(general, mainscreen.gamesjson, 'appid', int(appid))
        gamedesc = BeautifulSoup(self.gameinfo[str(appid)]['data']['detailed_description'].replace('\t', ''), 'html.parser')
        gamepic = self.gameinfo[str(appid)]['data']['header_image']
        self.gamedes = gamedesc.get_text('\n')
        imagevol = general.getimage(general, gamepic, gamepagebreedte, int(gamepagebreedte * gameratio), 0)
        gamepicture = Label(self.framec,
                          bg=backgroundmain)
        gamepicture.image = imagevol
        gamepicture.configure(image=imagevol)
        gamepicture.place(relx=0.05, rely=0.15)
        gamename = Label(self.framec,
                         text=self.gameinfo[str(appid)]['data']['name'],
                         font=gamepagetitlefont,
                         justify=LEFT,
                         fg=maintxt,
                         bg=backgroundmain)
        gamename.place(relx=0.05, rely=0.38)
        if steamjson != False:
            release = Label(self.framec,
                              text='Release date: {}'.format(steamjson['release_date']),
                              font=gamepagefont,
                              fg=maintxt,
                              bg=backgroundmain)
            release.place(relx=0.85, rely=0.2, anchor='e')
        else:
            release = 0
        gamedescription = Label(self.framec,
                                text=self.gamedes,
                                font=gamepagefont,
                                wraplength=900,
                                justify=LEFT,
                                anchor=NW,
                                height=5,
                                fg=maintxt,
                                bg=backgroundmain)
        gamedescription.place(relx=0.05, rely=0.45)
        seefulldescription = Label(self.framec,
                                   text='See full description',
                                   font=gamepagefont,
                                   fg=maintxt,
                                   bg=backgroundside,
                                   width=25,
                                   height=2)
        seefulldescription.place(relx=0.5, rely=0.63, anchor='center')
        seefulldescription.bind('<1>', lambda x:self.gotofulldescription())
        if self.gameinfo[str(appid)]['data']['is_free']:
            price = 'Free'
            discount = 0
        else:
            priceinfo = self.gameinfo[str(appid)]['data']['price_overview']
            price = priceinfo['final_formatted']
            discount = priceinfo['discount_percent']
        gameprice = Label(self.framec,
                          text='Price: {}'.format(price),
                          font=gamepagefont,
                          fg=maintxt,
                          bg=backgroundmain)
        gameprice.place(relx=0.85, rely=0.28, anchor='e')
        if discount != 0:
            gamepriceinitial = Label(self.framec,
                                     text=priceinfo['initial_formatted'],
                                     font=discountfont,
                                     fg=maintxt,
                                     bg=backgroundmain)
            gamepriceinitial.place(relx=0.85, rely=0.25, anchor='e')
            gamepricediscount = Label(self.framec,
                                      text='{}%'.format(discount),
                                      font=discountpercentfont,
                                      fg=maintxt,
                                      bg=backgroundmain)
            gamepricediscount.place(relx=0.85, rely=0.265, anchor='w')
        curplayers = Label(self.framec,
                           text='Current playercount: {}'.format(client.get_player_count(int(appid))),
                           font=gamepagefont,
                           fg=maintxt,
                           bg=backgroundmain)
        curplayers.place(relx=0.85, rely=0.31, anchor='e')
        screenshottxt = Label(self.framec,
                              text='Screenshots:',
                              font=gamepagefont,
                              fg=maintxt,
                              bg=backgroundmain)
        screenshottxt.place(relx=0.05, rely=0.7)
        screenshots = self.gameinfo[str(appid)]['data']['screenshots']
        place = 0
        for screenshot in screenshots[:3]:
            image = general.getimage(general, screenshot['path_thumbnail'], screenshotbreedte,
                                     int(screenshotbreedte * screenshotratio), 0)
            screenphoto = Label(self.framec,
                                bg=backgroundmain)
            screenphoto.image = image
            screenphoto.configure(image=image)
            screenphoto.place(relx=0.2+place*0.3, rely=0.85, anchor='center')
            place += 1


    def showfulldescription(self, appid):
        gobackbutton = Label(self.framedesc,
                                   text='Go Back',
                                   font=gamepagefont,
                                   fg=maintxt,
                                   bg=backgroundside,
                                   width=25,
                                   height=2)
        gobackbutton.place(relx=0.5, rely=0.1, anchor='center')
        gobackbutton.bind('<1>', lambda x:self.goback())
        descriptiontitle = Label(self.framedesc,
                                 text='The full description for {}'.format(self.gameinfo[str(appid)]['data']['name']),
                                 font=gamepagetitlefont,
                                 fg=maintxt,
                                 bg=backgroundmain)
        descriptiontitle.place(relx=0.05, rely=0.16)
        description = Label(self.framedesc,
                            text=self.gamedes,
                            wraplength=900,
                            font=fulldescriptionfont,
                            justify=LEFT,
                            height=36,
                            anchor=NW,
                            fg=maintxt,
                            bg=backgroundmain)
        description.place(relx=0.05, rely=0.22)


    def gotofulldescription(self):
        self.framec.forget()
        self.framedesc.pack(fill=BOTH, expand=1)


    def goback(self):
        self.framedesc.forget()
        self.framec.pack(fill=BOTH, expand=1)


class librarygame():
    def __init__(self, frame, root, json):
        frame.destroy()
        self.root = root
        try:
            self.framec.destroy()
        except:
            pass
        self.framec = Frame(self.root,
                            bg=backgroundmain)
        self.framec.pack(fill=BOTH, expand=1)
        self.displaygameinfo(json)


    def displaygameinfo(self, json):
        gotogeneralpage =  lambda x: (lambda y: gamescreen(self.framec, self.root, x))
        generalgameinfo = gamescreen.getgameinfo(gamescreen, json['appid'])
        imagevol = general.getimage(general, generalgameinfo[str(json['appid'])]['data']['header_image'], gamepagebreedte, int(gamepagebreedte * gameratio), 0)
        steamjson = general.binarysearch(general, mainscreen.gamesjson, 'appid', json['appid'])
        searchtag = random.choice(steamjson['steamspy_tags'].split(';'))
        popsort = general.QuickSort(general, mainscreen.gamesjson, 'positive_ratings', ascending=False)
        suggames = []
        for game in popsort:
            if searchtag in game['steamspy_tags']:
                if game['appid'] not in mainscreen.gamelist:
                    suggames.append(game)
            if len(suggames) >= 3:
                break
        gamepicture = Label(self.framec,
                          bg=backgroundmain)
        gamepicture.image = imagevol
        gamepicture.configure(image=imagevol)
        gamepicture.place(relx=0.05, rely=0.15)
        gamename = Label(self.framec,
                         text=generalgameinfo[str(json['appid'])]['data']['name'],
                         font=gamepagetitlefont,
                         justify=LEFT,
                         fg=maintxt,
                         bg=backgroundmain)
        gamename.place(relx=0.05, rely=0.38)
        gotogeneral = Label(self.framec,
                          text='Go to general page',
                          font=gamepagefont,
                          fg='gray',
                          bg=backgroundmain)
        gotogeneral.place(relx=0.85, rely=0.28, anchor='e')
        gotogeneral.bind('<1>', gotogeneralpage(json['appid']))
        playtime = 0
        if 'playtime_2weeks' in json.keys():
            playtime = round(json['playtime_2weeks']/60, 1)
        playtimerecent = Label(self.framec,
                          text='Your playtime the last two weeks: {} hours'.format(playtime),
                          font=gamepagefont,
                          fg=maintxt,
                          bg=backgroundmain)
        playtimerecent.place(relx=0.05, rely=0.5)
        playtimeall = Label(self.framec,
                               text='Your total playtime: {} hours'.format(round(json['playtime_forever']/60, 1)),
                               font=gamepagefont,
                               fg=maintxt,
                               bg=backgroundmain)
        playtimeall.place(relx=0.05, rely=0.55)
        suggestedtxt = Label(self.framec,
                            text='Other {} games like this'.format(searchtag.lower()),
                            font=gamepagefont,
                            fg=maintxt,
                            bg=backgroundmain)
        suggestedtxt.place(relx=0.05, rely=0.68)
        ind = 0
        for suggame in suggames:
            sugjson = gamescreen.getgameinfo(gamescreen, suggame['appid'])
            sugimage = general.getimage(general, sugjson[str(suggame['appid'])]['data']['header_image'], gamebreedte, int(gamebreedte*gameratio), 0)
            sugg = Label(self.framec,
                         bg=backgroundmain)
            sugg.image = sugimage
            sugg.configure(image=sugimage)
            sugg.place(relx=0.2+0.3*ind, rely=0.8, anchor='center')
            sugg.bind('<1>', gotogeneralpage(suggame['appid']))
            ind += 1


class personscreen():
    def __init__(self, frame, root, steamid):
        frame.destroy()
        self.root = root
        try:
            self.framec.destroy()
        except:
            pass
        self.framec = Frame(self.root,
                            bg=backgroundmain)
        self.framec.pack(fill=BOTH, expand=1)
        self.displayinfo(steamid)


    def getpersoninfo(self, steamid):
        personurl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(steamkey, steamid)
        personjson = general.getjson(general, personurl)
        return personjson


    def getrecentgames(self, steamid):
        recenturl = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={}&steamid={}&format=json'.format(steamkey, steamid)
        recentjson = general.getjson(general, recenturl)
        if recentjson['response'] == {}:
            return 'private'
        else:
            return recentjson


    def getownedgames(self, steamid):
        ownedurl = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json&include_appinfo=true&include_played_free_games=true'.format(steamkey, steamid)
        ownedjson = general.getjson(general, ownedurl)
        if ownedjson['response'] == {}:
            return 'private'
        else:
            return ownedjson


    def displayinfo(self, steamid):
        personjson = self.getpersoninfo(steamid)
        personinfo = personjson['response']['players'][0]
        imageurl = personinfo['avatarfull']
        image = general.getimage(general, imageurl, personprofilebreedte, personprofilebreedte, 0)
        profilepic = Label(self.framec,
                           bg=backgroundmain)
        profilepic.image = image
        profilepic.configure(image=image)
        profilepic.place(relx=0.05, rely=0.2)
        profilename = Label(self.framec,
                            text=personinfo['personaname'],
                            font=discountpercentfont,
                            fg=maintxt,
                            bg=backgroundmain)
        profilename.place(relx=0.25, rely=0.25, anchor='w')
        if 'realname' in list(personinfo.keys()):
            profilerealname = Label(self.framec,
                                    text=personinfo['realname'],
                                    font=personpagefont,
                                    fg=maintxt,
                                    bg=backgroundmain)
            profilerealname.place(relx=0.25, rely=0.3, anchor='w')
        personastates = {0:'Offline', 1:'Online', 2:'Busy', 3:'Away', 4:'Snooze', 5:'Looking to Trade', 6:'Looking to Play'}
        personastate = personinfo['personastate']
        txtcolor = maintxt
        personstate = personastates[personastate]
        if personastate > 0:
            if 'gameextrainfo' in list(personinfo.keys()):
                txtcolor = gameplaycolor
                gamename = personinfo['gameextrainfo']
                if len(gamename) > 30:
                    gamename = '{}...'.format(gamename[:27])
                personstate = 'Playing a game: {}'.format(gamename)
            else:
                txtcolor = onlinecolor
        profilestate = Label(self.framec,
                             text=personstate,
                             font=personpagefont,
                             fg=txtcolor,
                             bg=backgroundmain)
        profilestate.place(relx=0.25, rely=0.4, anchor='w')
        if txtcolor == gameplaycolor:
            profilestate.bind('<1>', lambda x:gamescreen(self.framec, self.root, personinfo['gameid']))
        recentgames = self.getrecentgames(steamid)
        if recentgames == 'private':
            privateprofile = Label(self.framec,
                                   text='This profile is private',
                                   font=discountpercentfont,
                                   fg='gray',
                                   bg=backgroundmain)
            privateprofile.place(relx=0.5, rely=0.6, anchor='center')
        else:
            self.gotograph = Label(self.framec,
                                   text='Graph',
                                   font=gamepagefont,
                                   width=15,
                                   height=2,
                                   fg=maintxt,
                                   bg=backgroundprofile)
            self.gotograph.place(relx=0.72, rely=0.47, anchor='e')
            self.gotograph.bind('<1>', lambda x:self.gograph())
            self.gotogeneral = Label(self.framec,
                                     text='General',
                                     font=gamepagefont,
                                     width=15,
                                     height=2,
                                     fg=maintxt,
                                     bg=backgroundmain)
            self.gotogeneral.place(relx=0.72, rely=0.47, anchor='w')
            self.gotogeneral.bind('<1>', lambda x:self.gogeneral())
            self.graphframe = Frame(self.framec,
                                    bg=backgroundprofile,
                                    width=self.framec.winfo_screenwidth()-2*sidewidth,
                                    height=440)
            self.graphframe.place(relx=0, rely=1, anchor='sw')
            self.generalframe = Frame(self.framec,
                                      bg=backgroundprofile,
                                      width=self.framec.winfo_screenwidth()-2*sidewidth,
                                      height=440)
            self.generalframe.place(relx=0, rely=1, anchor='sw')
            self.generalframe.place_forget()
            try:
                combostyle = ttk.Style()
                combostyle.theme_create('combostyle', parent='alt',
                                        settings={'TCombobox':
                                                      {'configure':
                                                           {'selectbackground': '#2c3e52',
                                                            'fieldbackground': '#2c3e52',
                                                            'background': '#1f2e3e',
                                                            'foreground': 'white',
                                                            }}})
                combostyle.theme_use('combostyle')
            except:
                pass
            self.game = StringVar()
            self.time = StringVar()
            self.gameframe = Frame()
            self.gameframe = Frame(self.graphframe,
                                   bg=backgroundprofile,
                                   width=205)
            self.gameframe.place(relx=0.05, rely=0.39, anchor='nw')
            thegames = self.getownedgames(steamid)['response']['games']
            thegamessorted = general.QuickSort(general, thegames, 'name')
            self.postedgames = []
            self.gamelst = []
            self.errormsg = False
            self.gamechange = lambda x: (lambda y: self.deletegame(x))
            self.allgames = {}
            for game in thegamessorted:
                self.allgames[game['name']] = game
            self.times = {'Last two weeks':'playtime_2weeks', 'Alltime':'playtime_forever'}
            ownedtxt = Label(self.graphframe,
                             text='Owned games',
                             font=gamepagefont,
                             fg=maintxt,
                             bg=backgroundprofile)
            ownedtxt.place(relx=0.05, rely=0.25)
            self.ownedgames = ttk.Combobox(self.graphframe,
                                           state='readonly',
                                           values=list(self.allgames.keys()),
                                           textvariable=self.game,
                                           font=gamepagefont,
                                           width=16)
            self.ownedgames.place(relx=0.05, rely=0.32)
            self.ownedgames.bind("<<ComboboxSelected>>", self.changegame)
            timetxt = Label(self.graphframe,
                            text='Timespan',
                            font=gamepagefont,
                            fg=maintxt,
                            bg=backgroundprofile)
            timetxt.place(relx=0.05, rely=0.08)
            self.timespan = ttk.Combobox(self.graphframe,
                                         state='readonly',
                                         values=list(self.times.keys()),
                                         textvariable=self.time,
                                         font=gamepagefont,
                                         width=16)
            self.timespan.current(0)
            self.timespan.place(relx=0.05, rely=0.15)
            confirm = Label(self.graphframe,
                            text='Make graph',
                            font=searchgamefont,
                            width=20,
                            height=2,
                            fg=maintxt,
                            bg=backgroundsearchgame)
            confirm.place(relx=0.0525, rely=0.8)
            confirm.bind('<1>', lambda x:self.makenewgraph())
            recentgamelist = recentgames['response']['games']
            self.games = []
            self.time_2weeks = []
            self.time_forever = []
            for item in recentgamelist[:5]:
                self.games.append(item['name'])
                self.time_2weeks.append(item['playtime_2weeks'])
                self.time_forever.append(item['playtime_forever'])
            self.makegraph(self.games, self.time_2weeks)
            self.timelst = []
            for game in thegamessorted:
                self.timelst.append(game['playtime_forever'])
            averagetime = general.average(general, self.timelst)
            averageplaytime = Label(self.generalframe,
                                    text='Average playtime: {} hours'.format(round(averagetime/60, 1)),
                                    font=gamepagefont,
                                    fg=maintxt,
                                    bg=backgroundprofile)
            averageplaytime.place(relx=0.1, rely=0.1)
            diff = -1
            closestgame = ''
            for thing in thegamessorted:
                newdiff = abs(thing['playtime_forever']-averagetime)
                if diff == -1:
                    closestgame = thing['name']
                    diff = newdiff
                elif diff > newdiff:
                    diff = newdiff
                    closestgame = thing['name']
            closesttoaverage = Label(self.generalframe,
                                     text='Closest to this: {}'.format(closestgame),
                                     font=gamepagefont,
                                     fg=maintxt,
                                     bg=backgroundprofile)
            closesttoaverage.place(relx=0.15, rely=0.18)
            mediantime = general.median(general, self.timelst)
            medianplaytime = Label(self.generalframe,
                                   text='Median playtime: {} hours'.format(round(mediantime/60, 1)),
                                   font=gamepagefont,
                                   fg=maintxt,
                                   bg=backgroundprofile)
            medianplaytime.place(relx=0.1, rely=0.32)
            diff = -1
            closestgame = ''
            for thing in thegamessorted:
                newdiff = abs(thing['playtime_forever']-mediantime)
                if diff == -1:
                    closestgame = thing['name']
                    diff = newdiff
                elif diff > newdiff:
                    diff = newdiff
                    closestgame = thing['name']
            closesttomedian = Label(self.generalframe,
                                    text='Closest to this: {}'.format(closestgame),
                                    font=gamepagefont,
                                    fg=maintxt,
                                    bg=backgroundprofile)
            closesttomedian.place(relx=0.15, rely=0.4)
            hourlist = [round(time/60, 1) for time in self.timelst]
            variance = Label(self.generalframe,
                             text='Variance: {}'.format(round(general.var(general, hourlist), 1)),
                             font=gamepagefont,
                             fg=maintxt,
                             bg=backgroundprofile)
            variance.place(relx=0.1, rely=0.6)
            standarddev = Label(self.generalframe,
                             text='Standard deviation: {}'.format(round(general.std(general, hourlist), 1)),
                             font=gamepagefont,
                             fg=maintxt,
                             bg=backgroundprofile)
            standarddev.place(relx=0.1, rely=0.7)


    def gograph(self):
        self.gotogeneral['bg'] = backgroundmain
        self.gotograph['bg'] = backgroundprofile
        self.generalframe.place_forget()
        self.graphframe.place(relx=0, rely=1, anchor='sw')


    def gogeneral(self):
        self.gotogeneral['bg'] = backgroundprofile
        self.gotograph['bg'] = backgroundmain
        self.graphframe.place_forget()
        self.generalframe.place(relx=0, rely=1, anchor='sw')


    def makegraph(self, xlst, ylst):
        try:
            self.thegraph.destroy()
        except:
            pass
        self.thegraph = Frame(self.graphframe,
                              width=700,
                              height=400,
                              bg=backgroundprofile)
        self.thegraph.place(relx=0.625, rely=0.5, anchor='center')
        xlist = ['\n'.join(wrap(l, 15)) for l in xlst]
        ylist = [round(m/60, 1) for m in ylst]
        font = {'family': 'arial', 'size': 7}
        plt.rc('font', **font)
        fig = plt.figure(figsize=(6, 3.75))
        plt.bar(x=xlist, height=ylist)
        # plt.tight_layout(rect=[0,0,0,0])
        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
        plt.xlabel('Games')
        plt.ylabel('Hours played')
        plt.title('Time played {}'.format(self.time.get()))
        canvas = FigureCanvasTkAgg(fig, master=self.thegraph)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center')


    def makenewgraph(self):
        timespan = self.time.get()
        listedgames = self.postedgames
        games = []
        time = []
        if listedgames == []:
            if self.times[timespan] == 'playtime_2weeks':
                self.makegraph(self.games, self.time_2weeks)
            elif self.times[timespan] == 'playtime_forever':
                self.makegraph(self.games, self.time_forever)
        else:
            for game in listedgames:
                games.append(self.allgames[game]['name'])
                if self.times[timespan] == 'playtime_2weeks':
                    if 'playtime_2weeks' not in self.allgames[game].keys():
                        time.append(0)
                    else:
                        time.append(self.allgames[game][self.times[timespan]])
                else:
                    time.append(self.allgames[game][self.times[timespan]])
            self.makegraph(games, time)


    def changegame(self, event):
        game = self.game.get()
        if game not in self.gamelst:
            if len(self.gamelst) >= 5:
                if not self.errormsg:
                    error = Label(self.gameframe,
                                  text='The limit is 5 games',
                                  justify=LEFT,
                                  font=tagfont,
                                  fg=wrong,
                                  bg=backgroundmain)
                    error.pack(pady=2, anchor='w')
                    self.errormsg = True
            else:
                self.gamelst.append(game)
                self.addgame()


    def addgame(self):
        for game in self.gamelst:
            if game not in self.postedgames:
                self.postedgames.append(game)
                if len(game) > 25:
                    gametxt = '{}...'.format(game[:22])
                else:
                    gametxt = game
                newgame = Label(self.gameframe,
                                text=gametxt,
                                justify=LEFT,
                                font=tagfont,
                                fg=maintxt,
                                bg=backgroundside)
                newgame.pack(pady=2, anchor='w')
                newgame.bind('<1>', self.gamechange(game))


    def deletegame(self, game):
        self.gameframe.destroy()
        self.gameframe = Frame(self.graphframe,
                               bg=backgroundmain,
                               width=205)
        self.gameframe.place(relx=0.05, rely=0.39, anchor='nw')
        for lstgame in self.postedgames:
            if lstgame != game:
                if len(lstgame) > 25:
                    gametxt = '{}...'.format(lstgame[:22])
                else:
                    gametxt = lstgame
                newgame = Label(self.gameframe,
                                text=gametxt,
                                font=tagfont,
                                fg=maintxt,
                                bg=backgroundside)
                newgame.pack(pady=2, anchor='w')
                newgame.bind('<1>', self.gamechange(lstgame))
        self.postedgames.remove(game)
        self.gamelst.remove(game)


class searchscreen():
    def __init__(self, frame, root, searchterm):
        frame.destroy()
        self.root = root
        try:
            self.framec.destroy()
        except:
            pass
        self.framec = Frame(self.root,
                            bg=backgroundmain)
        self.framec.pack(fill=BOTH, expand=1)
        self.showsearchscreen(searchterm)


    def getsearchresults(self, searchterm):
        newlst = []
        for game in mainscreen.gamesjson:
            if searchterm.lower() in game['name'].lower():
                newlst.append(game)
        return newlst


    def getpossibletags(self, json):
        taglst = []
        for game in json:
            tags = game['steamspy_tags'].split(';')
            for tag in tags:
                if {'tag':tag} not in taglst:
                    taglst.append({'tag':tag})
        return general.QuickSort(general, taglst, 'tag')


    def showsearchscreen(self, searchterm):
        self.arrowup = general.getimage(general, mainscreen.arrowpicture, 50, 50, 90)
        self.arrowdown = general.getimage(general, mainscreen.arrowpicture, 50, 50, 270)
        searchbar = Entry(self.framec,
                          font=searchbarfont,
                          width=19,
                          borderwidth=0,
                          insertbackground=maintxt,
                          fg=maintxt,
                          bg=backgroundside)
        searchbar.place(relx=0.05, rely=0.1)
        searchbar.bind('<Return>', lambda x: searchscreen(self.framec, self.root, searchbar.get()))
        searchbar.insert(0, searchterm)
        searchicon = 'https://www.eaolthof.nl/wp-content/uploads/2021/01/zoek2.png'
        searchimage = general.getimage(general, searchicon, 35, 35, 0)
        searchic = Label(self.framec,
                         bg=backgroundmain)
        searchic.image = searchimage
        searchic.configure(image=searchimage)
        searchic.place(relx=0.27, rely=0.0925)
        searchic.bind('<1>', lambda x:searchscreen(self.framec, self.root, searchbar.get()))
        searchtitle = Label(self.framec,
                            text='Search results for \'{}\''.format(searchterm),
                            font=gamepagetitlefont,
                            fg=maintxt,
                            bg=backgroundmain)
        searchtitle.place(relx=0.05, rely=0.14)
        self.searchresults = self.getsearchresults(searchterm)
        if len(self.searchresults) == 0:
            noresults = Label(self.framec,
                              text='No results',
                              font=('', 40, 'bold'),
                              fg='gray',
                              bg=backgroundmain)
            noresults.place(relx=0.5, rely=0.4, anchor='center')
        else:
            try:
                combostyle = ttk.Style()
                combostyle.theme_create('combostyle', parent='alt',
                                        settings={'TCombobox':
                                                      {'configure':
                                                           {'selectbackground': '#2c3e52',
                                                            'fieldbackground': '#2c3e52',
                                                            'background': '#1b2838',
                                                            'foreground': 'white',
                                                            }}})
                combostyle.theme_use('combostyle')
            except:
                pass
            self.sortterms = {'Name': 'name', 'Release date': 'release_date', 'Positive ratings': 'positive_ratings',
                              'Negative ratings': 'negative_ratings', 'Owners':'owners', 'Ratings ratio':'ratio',
                              'Price': 'price'}
            self.sortorders = {'Ascending': True, 'Descending': False}
            self.taglst = []
            self.track = StringVar()
            self.getterm = StringVar()
            self.sortorder = StringVar()
            self.tagchange = lambda x: (lambda y: self.deletetag(x))
            self.tagframe = Frame(self.framec,
                             bg=backgroundmain,
                             width=200)
            self.tagframe.place(relx=0.75, rely=0.4, anchor='nw')
            tagtitle = Label(self.framec,
                             text='Filter tags',
                             font=gamepagefont,
                             fg=maintxt,
                             bg=backgroundmain)
            tagtitle.place(relx=0.75, rely=0.315)
            searchtitle = Label(self.framec,
                                text='Sort by',
                                font=gamepagefont,
                                fg=maintxt,
                                bg=backgroundmain)
            searchtitle.place(relx=0.75, rely=0.615)
            taglstdict = self.getpossibletags(self.searchresults)
            taglst = []
            for tag in taglstdict:
                taglst.append(tag['tag'])
            self.tagdropdown = ttk.Combobox(self.framec,
                                            state='readonly',
                                            values=taglst,
                                            textvariable=self.track,
                                            font=gamepagefont,
                                            width=15)
            self.tagdropdown.place(relx=0.75, rely=0.35)
            self.tagdropdown.bind("<<ComboboxSelected>>", self.changetag)
            self.searchdropdown = ttk.Combobox(self.framec,
                                               state='readonly',
                                               values=list(self.sortterms.keys()),
                                               textvariable=self.getterm,
                                               font=gamepagefont,
                                               width=15)
            self.searchdropdown.place(relx=0.75, rely=0.65)
            self.searchorder = ttk.Combobox(self.framec,
                                               state='readonly',
                                               values=list(self.sortorders.keys()),
                                               textvariable=self.sortorder,
                                               font=gamepagefont,
                                               width=15)
            self.searchorder.current(0)
            self.searchorder.place(relx=0.75, rely=0.7)
            confirm = Label(self.framec,
                            text='Commit changes',
                            font=searchgamefont,
                            width=19,
                            height=2,
                            fg=maintxt,
                            bg=backgroundsearchgame)
            confirm.place(relx=0.75, rely=0.8)
            confirm.bind('<1>', lambda x:self.usesearchterms())
            self.postedtaglst = []
            self.errormsg = False
            self.usesearchterms()


    def changetag(self, event):
        tag = self.track.get()
        if tag not in self.taglst:
            if len(self.taglst) >= 5:
                if not self.errormsg:
                    error = Label(self.tagframe,
                                  text='The limit is 5 tags',
                                  justify=LEFT,
                                  font=tagfont,
                                  fg=wrong,
                                  bg=backgroundmain)
                    error.pack(pady=2, anchor='w')
                    self.errormsg = True
            else:
                self.taglst.append(tag)
                self.addtag()


    def addtag(self):
        for tag in self.taglst:
            if tag not in self.postedtaglst:
                self.postedtaglst.append(tag)
                newtag = Label(self.tagframe,
                               text=tag,
                               justify=LEFT,
                               font=tagfont,
                               fg=maintxt,
                               bg=backgroundside)
                newtag.pack(pady=2, anchor='w')
                newtag.bind('<1>', self.tagchange(tag))


    def deletetag(self, tag):
        self.tagframe.destroy()
        self.tagframe = Frame(self.framec,
                              bg=backgroundmain,
                              width=200)
        self.tagframe.place(relx=0.75, rely=0.4, anchor='nw')
        for lsttag in self.postedtaglst:
            if lsttag != tag:
                newtag = Label(self.tagframe,
                               text=lsttag,
                               font=tagfont,
                               fg=maintxt,
                               bg=backgroundside)
                newtag.pack(pady=2, anchor='w')
                newtag.bind('<1>', self.tagchange(lsttag))
        self.postedtaglst.remove(tag)
        self.taglst.remove(tag)


    def getgameinfo(self):
        added = 0
        while added < 5 and self.json != []:
            try:
                jsonfile = gamescreen.getgameinfo(gamescreen, self.json[0]['appid'])
                image = general.getimage(general, jsonfile[str(self.json[0]['appid'])]['data']['header_image'], 200,
                                         int(200*gameratio), 0)
                self.displayedgames.append({'appid':self.json[0]['appid'],
                                            'name':self.json[0]['name'],
                                            'picture':image,
                                            'price':self.json[0]['price'],
                                            'tags':self.json[0]['steamspy_tags'].split(';'),
                                            'positive':self.json[0]['positive_ratings'],
                                            'negative':self.json[0]['negative_ratings'],
                                            'release':self.json[0]['release_date'],
                                            'owners':self.json[0]['owners']})
                added += 1
            except:
                pass
            self.json.pop(0)


    def displaygames(self, json, startindex):
        try:
            self.gameframe.destroy()
        except:
            pass
        self.gameframe = Frame(self.framec,
                               bg=backgroundmain,
                               width=750,
                               height=700)
        self.gameframe.place(relx=0, rely=1, anchor='sw')
        self.gotogeneral = lambda x: (lambda y: gamescreen(self.framec, self.root, x))
        uparrow = False
        downarrow = True
        self.json = json
        if startindex > 0:
            uparrow = True
        if startindex+5 > len(self.displayedgames):
            if self.json != []:
                self.getgameinfo()
        totalpages = math.ceil((len(self.displayedgames)+len(self.json))/5)
        currentpage = math.ceil((startindex+5)/5)
        if currentpage == totalpages:
            downarrow = False
        ind = 0
        for game in self.displayedgames[startindex:startindex+5]:
            searchedgamebg = Canvas(self.gameframe,
                                    bg=backgroundsearchgame,
                                    borderwidth=0,
                                    highlightthickness=0,
                                    width=700,
                                    height=105)
            searchedgamebg.place(relx=0.065, rely=0.18+0.16*ind, anchor='w')
            searchedgamebg.bind('<1>', self.gotogeneral(game['appid']))
            searchedgame = Label(self.gameframe,
                                 bg=backgroundmain)
            searchedgame.image = game['picture']
            searchedgame.configure(image=game['picture'])
            searchedgame.place(relx=0.075, rely=0.18+0.16*ind, anchor='w')
            searchedgame.bind('<1>', self.gotogeneral(game['appid']))
            gamename = game['name']
            if len(gamename) > 25:
                gamename = '{}...'.format(gamename[:22])
            searchedgamename = Label(self.gameframe,
                                     text=gamename,
                                     font=searchgamefont,
                                     fg=maintxt,
                                     bg=backgroundsearchgame)
            searchedgamename.place(relx=0.98, rely=0.13+0.16*ind, anchor='e')
            searchedgamename.bind('<1>', self.gotogeneral(game['appid']))
            if type(game['release']) is str:
                try:
                    game['release'] = datetime.strptime(game['release'], '%Y-%m-%d').strftime('%d/%m/%Y')
                except ValueError:
                    pass
            else:
                game['release'] = game['release'].strftime('%d/%m/%Y')
            searchedgamerelease = Label(self.gameframe,
                                        text=game['release'],
                                        font=searchgamefont,
                                        fg=maintxt,
                                        bg=backgroundsearchgame)
            searchedgamerelease.place(relx=0.98, rely=0.16+0.16*ind, anchor='e')
            searchedgamerelease.bind('<1>', self.gotogeneral(game['appid']))
            owners = str(game['owners'])
            if 3 < len(owners) < 7:
                owners = '{}.{}'.format(owners[:-3], owners[-3:])
            elif 6 < len(owners) < 10:
                owners = '{}.{}.{}'.format(owners[:-6], owners[-6:-3], owners[-3:])
            searchedgameowners = Label(self.gameframe,
                                       text='{} owners'.format(owners),
                                       font=searchgamefont,
                                       fg=maintxt,
                                       bg=backgroundsearchgame)
            searchedgameowners.place(relx=0.35, rely=0.13+0.16*ind, anchor='w')
            searchedgameowners.bind('<1>', self.gotogeneral(game['appid']))
            searchedgamepos = Label(self.gameframe,
                                    text='+ {}'.format(game['positive']),
                                    font=searchgamefont,
                                    fg=maintxt,
                                    bg=backgroundsearchgame)
            searchedgamepos.place(relx=0.35, rely=0.16+0.16*ind, anchor='w')
            searchedgamepos.bind('<1>', self.gotogeneral(game['appid']))
            searchedgameneg = Label(self.gameframe,
                                    text='- {}'.format(game['negative']),
                                    font=searchgamefont,
                                    fg=maintxt,
                                    bg=backgroundsearchgame)
            searchedgameneg.place(relx=0.35, rely=0.19+0.16*ind, anchor='w')
            searchedgameneg.bind('<1>', self.gotogeneral(game['appid']))
            if game['price'] == 0.0:
                price = 'Free'
            else:
                price = '€{}'.format(game['price'])
            searchedgameprice = Label(self.gameframe,
                                     text=price,
                                     font=searchgamefont,
                                     fg=maintxt,
                                     bg=backgroundsearchgame)
            searchedgameprice.place(relx=0.98, rely=0.19+0.16*ind, anchor='e')
            searchedgameprice.bind('<1>', self.gotogeneral(game['appid']))
            alltags = ''
            for tag in game['tags'][:4]:
                alltags += '{}   '.format(tag)
            searchedgametags = Label(self.gameframe,
                                     text=alltags,
                                     font=tagfont,
                                     fg=maintxt,
                                     bg=backgroundsearchgame)
            searchedgametags.place(relx=0.35, rely=0.235+0.16*ind, anchor='w')
            searchedgameprice.bind('<1>', self.gotogeneral(game['appid']))
            ind +=1
        if uparrow:
            goup = Label(self.gameframe,
                         bg=backgroundmain)
            goup.image = self.arrowup
            goup.configure(image=self.arrowup)
            goup.place(relx=0.5325, rely=0.05, anchor='center')
            goup.bind('<1>', lambda x:self.displaygames(json, startindex-5))
        if downarrow:
            godown = Label(self.gameframe,
                           bg=backgroundmain)
            godown.image = self.arrowdown
            godown.configure(image=self.arrowdown)
            godown.place(relx=0.5325, rely=0.95, anchor='center')
            godown.bind('<1>', lambda x: self.displaygames(json, startindex+5))
        page = Label()
        page = Label(self.gameframe,
                     text='{}/{}'.format(currentpage, totalpages),
                     font=gamepagefont,
                     fg=maintxt,
                     bg=backgroundmain)
        page.place(relx=1, rely=0.93, anchor='e')


    def usesearchterms(self):
        newjson = self.searchresults.copy()
        tagfilters = self.taglst
        sortterm = self.getterm.get()
        aftertags = []
        ascending = self.sortorder.get()
        if tagfilters != []:
            for game in newjson:
                gametags = game['steamspy_tags']
                for tag in tagfilters:
                    if tag in gametags:
                        aftertags.append(game)
                        break
        else:
            aftertags = newjson
        for dict in aftertags:
            try:
                values = dict['owners'].split('-')
                for i in range(len(values)):
                    values[i] = int(values[i])
                dict['owners'] = int(general.average(general, values))
            except AttributeError:
                break
        if sortterm != '':
            if self.sortterms[sortterm] == 'ratio':
                for item in aftertags:
                    try:
                        item['ratio'] = item['positive_ratings']/item['negative_ratings']
                    except ZeroDivisionError:
                        item['ratio'] = 100000
            elif self.sortterms[sortterm] == 'release_date':
                for item in aftertags:
                    try:
                        item['release_date'] = datetime.strptime(item['release_date'], '%Y-%m-%d')
                    except TypeError:
                        break
            aftertags = general.QuickSort(general, aftertags, self.sortterms[sortterm], ascending=self.sortorders[ascending])
        self.displayedgames = []
        self.displaygames(aftertags.copy(), 0)



def goodbye():
    print('closing sequence')
    newloginkey = client.login_key
    if newloginkey is None:
        newloginkey = login.loginkey
    sessiontxt = '{}\n{}\n{}'.format(login.remember, client.username, newloginkey)
    if int(login.remember) == 0:
        sessiontxt = '{}\n{}\n{}'.format(0, None, None)
    with open('session.txt', 'w') as sessionfile:
        sessionfile.write(sessiontxt)
    client.logout()


if __name__ == "__main__":
    login()
    atexit.register(goodbye)
