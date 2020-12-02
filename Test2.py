import requests #pip install requests
import urllib.parse #pip install urllib
from tkinter import *
from PIL import Image, ImageTk #pip install pillow
import io

steamjson = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
breedte = 250

class mainscreen():
    def gamesget(self):
        self.numb = 0
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
            image = image.resize((breedte, int(breedte * gameratio)), Image.ANTIALIAS)
            imagevolgame = ImageTk.PhotoImage(image)
            self.gamephoto.append({'image':imagevolgame,
                                  'appid':game})
        self.gameshow()


    def gameshow(self):
        try:
            self.frame.destroy()
        except AttributeError:
            pass
        self.frame = Frame(root)
        self.frame.pack(pady=(200,0))
        gamepageshow = lambda x:(lambda y:self.gameklik(x))
        for j in range(3):
            ind = self.numb + j
            gamepiccont = self.gamephoto[ind]['image']
            gamepic = Label(self.frame)
            gamepic.image = gamepiccont
            gamepic.config(image=gamepiccont)
            gamepic.bind('<1>', gamepageshow(self.gamephoto[ind]['appid']))
            gamepic.grid(row=0, column=1+j, padx=50)
        left = Label(self.frame,
                     text = '<',
                     font=('',50))
        left.grid(row=0, column=0)
        left.bind('<1>', lambda go:self.gameleft())
        right = Label(self.frame,
                      text = '>',
                      font=('',50))
        right.grid(row=0, column=4)
        right.bind('<1>', lambda go:self.gameright())


    def gameleft(self):
        self.numb -= 3
        if self.numb < 0:
            self.numb = 6
        self.gameshow()


    def gameright(self):
        self.numb += 3
        if self.numb > 6:
            self.numb = 0
        self.gameshow()


    def gameklik(self, gameid):
        print(gameid)


    def __init__(self):
        self.gamesget()


root = Tk()
root.attributes('-fullscreen', True)
root.bind('<F8>', lambda sluiten:root.destroy())
mainscreen()
root.mainloop()