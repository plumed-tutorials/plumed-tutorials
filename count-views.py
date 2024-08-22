import pytube
from pytube import YouTube
import datetime

video_url = [
# first series
"https://www.youtube.com/2eGhMSdIJEs",
"https://www.youtube.com/TzSxBnX4uDk",
"https://www.youtube.com/dJKajNwbJ74",
"https://www.youtube.com/XKqislC2GYA",
"https://www.youtube.com/gHXXGYIgasE",
"https://www.youtube.com/SuHcOYqIOrY",
"https://www.youtube.com/q0RHlFAk544",
"https://www.youtube.com/UgTIGQxJtOc",
"https://www.youtube.com/v_CCLyjQ3yI",
"https://www.youtube.com/0o9rV2cWiJU",
"https://www.youtube.com/EoErcfzwtA8",
"https://www.youtube.com/PJovdFGb8KQ",
"https://www.youtube.com/2k7RacpoIBk",
"https://www.youtube.com/RftHvdwrEEk",
# second series
"https://www.youtube.com/7nHU4S5uCnA",
"https://www.youtube.com/HCI_FtnSnck",
"https://www.youtube.com/ZL81ZxN_eo0",
"https://www.youtube.com/T8a-kP6V3_g",
"https://www.youtube.com/q1D39A_LQag",
"https://www.youtube.com/1XYGfA4kJ1c",
"https://www.youtube.com/Rn5JgItgKX4",
"https://www.youtube.com/XsRBGl1wWAU",
"https://www.youtube.com/veSnKC9hmWo",
"https://www.youtube.com/A7mOOXZvqbQ",
"https://www.youtube.com/o4IMzRr04AY",
"https://www.youtube.com/vsN_Ff3bluU",
"https://www.youtube.com/b2_1LccKj9c",
"https://www.youtube.com/_WBRLitZZY8",
"https://www.youtube.com/H1nFtEf96-M",
"https://www.youtube.com/ADXJErS9vgs",
"https://www.youtube.com/m5eTgR232V4",
"https://www.youtube.com/LexZoELjR5c",
"https://www.youtube.com/xAWhtFk5cMM",
"https://www.youtube.com/Cmw_v2Y8o9k",
"https://www.youtube.com/rVFEF4YNLnk",
"https://www.youtube.com/tPHxDmNW7to",
"https://www.youtube.com/H1KfRU8aEFY",
"https://www.youtube.com/ViI55NckukI",
"https://www.youtube.com/TeiEeR3jwd0",
"https://www.youtube.com/1GSKhM57lo0",
"https://www.youtube.com/JjpKSzb9kJM",
"https://www.youtube.com/6zGBxlx0qeE",
"https://www.youtube.com/srZfm_TIgwc"
]

views = 0
for v in video_url:
    views += int(YouTube(v).views)

mydate = datetime.datetime.now()
mydate = mydate.strftime("%B")+" "+ str(mydate.strftime("%Y"))
print("All classes have been recorded and are available on [YouTube](https://www.youtube.com/@plumedorg1402). As of %s, they have been viewed %d times. In 2024, PLUMED Masterclass lectures were converted to PLUMED Tutorials and are available [here](https://www.plumed-tutorials.org/browse?search=masterclass)." % (mydate, views))
