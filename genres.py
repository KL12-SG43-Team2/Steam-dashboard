import tkinter as tk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from textwrap import wrap


window = tk.Tk()
window.geometry("1920x1080")
steamID = 76561198803753153

def steamgameslibrary():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    res = requests.get(url)
    json = res.json()
    return json


def binarysearch(lst, key, target):
    new_lst = lst.copy()
    aver = int((len(lst) - 1) / 2)
    if new_lst != []:
        if target == new_lst[aver][key]:
            return new_lst[aver]
        elif aver >= len(lst) - 1:
            return False
        elif target > new_lst[aver][key]:
            return binarysearch(new_lst[aver + 1:], key, target)
        else:
            return binarysearch(new_lst[:aver], key, target)
    return False


def allTimeGenres(steamID):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=7139EBA744B55B104024D221C07EFB38&steamid={steamID}=json"
    res = requests.get(url)
    data = res.json()
    games = []

    length = len(data["response"]["games"])
    for i in range(length):
        gamesInfo = data["response"]["games"][i]["appid"]
        games.append(gamesInfo)

    steamlst = steamgameslibrary()
    freqs = dict()
    genres = []
    for i in games:
        result = binarysearch(steamlst, "appid", i)
        if result:
            splitting = result["genres"].split(";")
            for j in splitting:
                genres.append(j)

    for i in genres:
        if i in freqs.keys():
            freqs[i] += 1
        else:
            freqs[i] = 1

    sortedlist = sorted(freqs, key=freqs.get)
    sortedlist.reverse()

    frequency = []
    for i in sortedlist:
        frequency.append(freqs[i])


    sortedlist = ['\n'.join(wrap(l, 15)) for l in sortedlist]

    font = {'family': 'arial', 'size': 8}
    plt.rc('font', **font)

    fig = plt.figure(figsize=(4, 5))
    plt.bar(x=sortedlist[:5], height=frequency[:5])
    plt.xlabel("games")
    plt.ylabel("playtime")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=100, y=250)

def buttonAllTimeGenres():
    allTimeGenres(steamID)



btn2 = tk.Button(window, text='All time', command=buttonAllTimeGenres)
btn2.place(x=50, y=25)

window.mainloop()
