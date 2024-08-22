import pytube
from pytube import YouTube
import datetime

video_url = [
# first series
"https://www.youtube.com/watch?v=2eGhMSdIJEs",
"https://www.youtube.com/watch?v=TzSxBnX4uDk",
"https://www.youtube.com/watch?v=dJKajNwbJ74",
"https://www.youtube.com/watch?v=XKqislC2GYA",
"https://www.youtube.com/watch?v=gHXXGYIgasE",
"https://www.youtube.com/watch?v=SuHcOYqIOrY",
"https://www.youtube.com/watch?v=q0RHlFAk544",
"https://www.youtube.com/watch?v=UgTIGQxJtOc",
"https://www.youtube.com/watch?v=v_CCLyjQ3yI",
"https://www.youtube.com/watch?v=0o9rV2cWiJU",
"https://www.youtube.com/watch?v=EoErcfzwtA8",
"https://www.youtube.com/watch?v=PJovdFGb8KQ",
"https://www.youtube.com/watch?v=2k7RacpoIBk",
"https://www.youtube.com/watch?v=RftHvdwrEEk",
# second series
"https://www.youtube.com/watch?v=7nHU4S5uCnA",
"https://www.youtube.com/watch?v=HCI_FtnSnck",
"https://www.youtube.com/watch?v=ZL81ZxN_eo0",
"https://www.youtube.com/watch?v=T8a-kP6V3_g",
"https://www.youtube.com/watch?v=q1D39A_LQag",
"https://www.youtube.com/watch?v=1XYGfA4kJ1c",
"https://www.youtube.com/watch?v=Rn5JgItgKX4",
"https://www.youtube.com/watch?v=XsRBGl1wWAU",
"https://www.youtube.com/watch?v=veSnKC9hmWo",
"https://www.youtube.com/watch?v=A7mOOXZvqbQ",
"https://www.youtube.com/watch?v=o4IMzRr04AY",
"https://www.youtube.com/watch?v=vsN_Ff3bluU",
"https://www.youtube.com/watch?v=b2_1LccKj9c",
"https://www.youtube.com/watch?v=_WBRLitZZY8",
"https://www.youtube.com/watch?v=H1nFtEf96-M",
"https://www.youtube.com/watch?v=ADXJErS9vgs",
"https://www.youtube.com/watch?v=m5eTgR232V4",
"https://www.youtube.com/watch?v=LexZoELjR5c",
"https://www.youtube.com/watch?v=xAWhtFk5cMM",
"https://www.youtube.com/watch?v=Cmw_v2Y8o9k",
"https://www.youtube.com/watch?v=rVFEF4YNLnk",
"https://www.youtube.com/watch?v=tPHxDmNW7to",
"https://www.youtube.com/watch?v=H1KfRU8aEFY",
"https://www.youtube.com/watch?v=ViI55NckukI",
"https://www.youtube.com/watch?v=TeiEeR3jwd0",
"https://www.youtube.com/watch?v=1GSKhM57lo0",
"https://www.youtube.com/watch?v=JjpKSzb9kJM",
"https://www.youtube.com/watch?v=6zGBxlx0qeE",
"https://www.youtube.com/watch?v=srZfm_TIgwc"
]

views = 0
for v in video_url:
    try:
     views += int(YouTube(v).views)

mydate = datetime.datetime.now()
mydate = mydate.strftime("%B")+" "+ str(mydate.strftime("%Y"))
print("All classes have been recorded and are available on [YouTube](https://www.youtube.com/@plumedorg1402). As of %s, they have been viewed %d times. In 2024, PLUMED Masterclass lectures were converted to PLUMED Tutorials and are available [here](https://www.plumed-tutorials.org/browse?search=masterclass)." % (mydate, views))
