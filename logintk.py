from tkinter import *
from steam.client import SteamClient #pip install steam
#pip install google-cloud
# pip install google-cloud-
#pip install steam[client]
from steam.enums import EResult
import requests #pip install requests
from PIL import ImageTk,Image  #pip install pillow
import urllib.parse #pip install urllib
import io
import atexit
from bs4 import BeautifulSoup #pip install lxml

Luka = '76561198174496762'
Luka2 = '76561198371592493'
Robin = '76561197960434622'
Joel = '76561198152182165'
Eva = '76561198803753153'
Henry = '76561198074124658'
# steamkey = '7139EBA744B55B104024D221C07EFB38'
steamkey = '783790D02B11E668DE41726C35D66B15'
steamjson = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
client = SteamClient()
language = 'en'
# user = sw.WebAuth('username')
# ac = AnyCache()
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
#achtergrondkleuren
backgroundlogin = '#1b2838'
backgroundmain = backgroundlogin
backgroundtest = 'white'
backgroundside = '#101822'
#afmetingen
sidewidth = 240
gamebreedte = 260
gamepagebreedte = 300
iconbreedte = 30
iconbreedtemore = 50
profilepicbreedte = 60
screenshotbreedte = 300
gamenamelength = 20
namelength = gamenamelength
steamlogowidth = 150
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


    def QuickSort(self, lst, key, ascending=True):
        if not lst:
            return []
        else:
            pivot = (len(lst) // 2)
            pivot_value = lst[pivot]
            lesser = self.QuickSort(self, [l for i, l in enumerate(lst)
                                           if l[key] < pivot_value[key] and i != pivot], key)
            greater = self.QuickSort(self, [l for l in lst if l[key] > pivot_value[key]], key)
            equal = [l for l in lst if l[key] == pivot_value[key]]
            newlst = lesser + equal + greater
            if not ascending:
                newlst.reverse()
            return newlst


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
        passtxt.place(relx=0.31, rely=0.45)
        self.password = Entry(self.frame,
                              show="\u2022",
                              width=30)
        self.password.place(relx=0.5, rely=0.525, anchor=CENTER)
        self.passwrong = Label(self.frame,
                               bg=backgroundlogin,
                               fg=wrong)
        self.passwrong.place(relx=0.31, rely=0.56)
        self.rem = IntVar()
        remember = Checkbutton(self.frame,
                               bg=backgroundlogin,
                               activebackground=backgroundlogin,
                               bd=0,
                               variable=self.rem)
        remember.place(relx=0.305, rely=0.65)
        remembertxt = Label(self.frame,
                            text='Stay logged in',
                            fg=txt,
                            bg=backgroundlogin)
        remembertxt.place(relx=0.34, rely=0.65)
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
    def gamesget(self):
        games = general.getjson(general, steamjson)
        mainscreen.gamesjson = games
        allgamelist = []
        gamephoto = []
        for i in range(9):
            game = str(mainscreen.gamesjson[i]['appid'])
            gameurl = 'https://store.steampowered.com/api/appdetails?appids={}&language={}'.format(game, language)
            gamejson = general.getjson(general, gameurl)
            gamepic = gamejson[game]['data']['header_image']
            imagevolgame = general.getimage(general, gamepic, gamebreedte, int(gamebreedte * gameratio), 0)
            gamephoto.append({'image':imagevolgame, 'appid':game})
        popsort = general.QuickSort(general, games, 'positive_ratings', ascending=False)
        games = self.gamesjson['response']['games']
        gamelist = []
        popgamesnotinlib = []
        for game in games:
            gamelist.append(game['appid'])
        for game in popsort:
            if game['appid'] not in gamelist:
                gameurl = 'https://store.steampowered.com/api/appdetails?appids={}&language={}'.format(game['appid'],
                                                                                                       language)
                gamejson = general.getjson(general, gameurl)
                gamepic = gamejson[str(game['appid'])]['data']['header_image']
                imagevolgame = general.getimage(general, gamepic, gamebreedte, int(gamebreedte * gameratio), 0)
                popgamesnotinlib.append({'image': imagevolgame, 'appid': game['appid']})
            if len(popgamesnotinlib) >= 9:
                break
        allgamelist.append(gamephoto)
        allgamelist.append(gamephoto)
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
        steamlogo = 'https://www.eaolthof.nl/wp-content/uploads/2020/12/steam.jpg'
        imagevol = general.getimage(general, steamlogo, steamlogowidth, int(steamlogowidth*46/191), 0)
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
                          fg=maintxt,
                          bg=backgroundside)
        searchbar.grid(row=0, column=1, padx=(380,0), pady=(150,10), sticky='e')
        searchicon = 'https://www.eaolthof.nl/wp-content/uploads/2021/01/search.jpg'
        searchimage = general.getimage(general, searchicon, 35, 35, 0)
        searchic = Label(self.framesearch,
                         bg=backgroundmain)
        searchic.image = searchimage
        searchic.configure(image=searchimage)
        searchic.grid(row=0, column=2, pady=(140,0), sticky='w')
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
        self.gamesjson = self.getownedgames(steamid)
        games = self.gamesjson['response']['games']
        gametitle = Label(self.framel,
                          text='Owned Games:',
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
            gamepic.bind('<1>', self.gamepageshow(game['appid']))
            gamepic.place(relx=0.1, rely=y+ind*0.05)
            gamename = Label(self.framel,
                             text=gamenamevar,
                             fg=maintxt,
                             bg=backgroundside)
            gamename.bind('<1>', self.gamepageshow(game['appid']))
            gamename.place(relx=0.25, rely=y+0.02+ind*0.05, anchor='w')
            ind += 1


    def gamemoreclick(self):
        self.cleanscreen()
        showfulllist(self.framec, self.framecunder, self.gamesjson, 'games', 'Your library')


    def gamefavorites(self):
        games = self.gamesjson['response']['games']
        fav_games = general.QuickSort(general, games, 'playtime_forever', ascending=False)
        favorgames = fav_games[:3]
        favortitle = Label(self.framel,
                           text='Favorite games:',
                           font=sidefont,
                           bg=backgroundside,
                           fg=maintxt)
        favortitle.place(relx=0.1, rely=0.2, anchor='w')
        self.gamesideshow(favorgames, 0.23)


    def getfriends(self, steamid):
        friendurl = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend'.format(steamkey, steamid)
        friendjson = general.getjson(general, friendurl)
        return friendjson


    def friendtitleshow(self, steamid):
        friendurl = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend'.format(steamkey, steamid)
        friendjson = general.getjson(general, friendurl)
        friends = friendjson['friendslist']['friends']
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
                                         'personastate':person['personastate'],
                                         'gameplaying':gameplaying,
                                         'gameplayingid':person['gameid']})
            else:
                gameplaying = ''
                self.new_personlst.append({'id':person['steamid'],
                                      'name':person['personaname'],
                                      'picture':person['avatar'],
                                      'personastate':person['personastate'],
                                      'gameplaying':gameplaying})
        friendtitle = Label(self.framer,
                          text='Friends:',
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
        userlogout = Label(self.framer,
                           text='Logout',
                           font=logoutfont,
                           fg='gray',
                           bg=backgroundside)
        userlogout.place(relx=0.575, rely=0.95, anchor='e')
        userlogout.bind('<1>', lambda x:self.logout())
        image = general.getimage(general, userinfo['avatar'], profilepicbreedte, profilepicbreedte, 0)
        userpicture = Label(self.framer,
                            bg=backgroundmain)
        userpicture.image = image
        userpicture.configure(image=image)
        userpicture.place(relx=0.6, rely=0.9)
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
        showfulllist(self.framec, self.framecunder, self.new_personlst, 'friends', 'Your friends')


    def friendclick(self, steamid):
        print(steamid)


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
        self.gamepictures = []
        for game in gamelist:
            gameicurl = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(
                game['appid'], game['img_icon_url'])
            imagevol = general.getimage(general, gameicurl, iconbreedtemore, iconbreedtemore, 0)
            self.gamepictures.append({'id':str(game['appid']),
                                      'name':game['name'],
                                      'picture':imagevol})
        self.startindex = 0
        self.displayinfo(self.gamepictures, self.startindex, title)


    def showfriends(self, dict, title):
        for friend in dict:
            profilepicurl = friend['picture']
            imagevol = general.getimage(general, profilepicurl, iconbreedtemore, iconbreedtemore, 0)
            friend['picture'] = imagevol
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
                gameicon = Label(self.framec,
                                 bg=backgroundmain)
                gameicon.image = image
                gameicon.configure(image=image)
                gameicon.place(relx=0.05+y*0.32, rely=0.25+x*0.12)
                gamenamedisplay = Label(self.framec,
                                        text=gamename,
                                        font=gamepagefont,
                                        fg=bordercolor,
                                        bg=backgroundmain)
                gamenamedisplay.place(relx=0.11+y*0.32, rely=0.265+x*0.12)
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


def goodbye():
    print('closing sequence')
    newloginkey = client.login_key
    if newloginkey is None:
        newloginkey = login.loginkey
    sessiontxt = '{}\n{}\n{}'.format(login.remember, client.username, newloginkey)
    if int(login.remember) == 1:
        with open('session.txt', 'w') as sessionfile:
            sessionfile.write(sessiontxt)
    client.logout()


if __name__ == "__main__":
    login()
    # mainscreen(Luka)
    atexit.register(goodbye)
