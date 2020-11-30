from tkinter import *
import requests #pip install requests
from PIL import ImageTk,Image  #pip install pillow
import urllib.parse #pip install urllib
import io

# key = "7139EBA744B55B104024D221C07EFB38"
# url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={evaID}"

Luka = '76561198174496762'
Robin = '76561197960434622'
Joel = '76561198152182165'
Eva = '76561198803753153'
Henry = '76561198074124658'

steamid = Henry
steamkey = '7139EBA744B55B104024D221C07EFB38'
spelid = '20'


def steamgameslibrary():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    res = requests.get(url)
    data = res.json()
    return data


def appID():
    app_id = []
    for item in steamgameslibrary():
        app_id.append(item['appid'])
    return (app_id)


def header():
    game = str(appID()[0])
    gameurl = 'https://store.steampowered.com/api/appdetails?appids={}'.format(game) #json file met app info
    res1 = requests.get(gameurl)
    data1 = res1.json()

    gamepic = data1[game]['data']['header_image'] #de link van de afbeelding

    return gamepic


#LAYOUTS
Root = Tk()
Root.title("Steam dashboard")
Root.configure(bg="#1B2838")
Root.geometry("1920x1080")



#ACHTERGROND
urlBG = "https://www.eaolthof.nl/wp-content/uploads/2020/11/004-002.png"
image_bytes = urllib.request.urlopen(urlBG).read()
data_stream = io.BytesIO(image_bytes)
pil_image = Image.open(data_stream)
tk_image = ImageTk.PhotoImage(pil_image)
Main = Label(Root, image=tk_image)
Main.pack()

breedte = 376

raw_data1 = urllib.request.urlopen(header()).read()
image1 = Image.open(io.BytesIO(raw_data1))
imagevolgame = ImageTk.PhotoImage(image1)
gameratio = imagevolgame.height()/imagevolgame.width()
image1 = image1.resize((breedte, int(breedte*gameratio)), Image.ANTIALIAS)
imagevolgame = ImageTk.PhotoImage(image1)

beeldgame = Canvas(Main, height=175, width=376)
beeldgame.create_image(0, 0, image=imagevolgame, anchor=NW)
beeldgame.place(x=371, y=181)

Root.mainloop()