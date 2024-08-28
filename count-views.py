from pytube import YouTube
import datetime

video_url = [
# first series
"http://www.youtube.com/watch?v=2eGhMSdIJEs",
"http://www.youtube.com/watch?v=TzSxBnX4uDk",
"http://www.youtube.com/watch?v=dJKajNwbJ74",
"http://www.youtube.com/watch?v=XKqislC2GYA",
"http://www.youtube.com/watch?v=gHXXGYIgasE",
"http://www.youtube.com/watch?v=SuHcOYqIOrY",
"http://www.youtube.com/watch?v=q0RHlFAk544",
"http://www.youtube.com/watch?v=UgTIGQxJtOc",
"http://www.youtube.com/watch?v=v_CCLyjQ3yI",
"http://www.youtube.com/watch?v=0o9rV2cWiJU",
"http://www.youtube.com/watch?v=EoErcfzwtA8",
"http://www.youtube.com/watch?v=PJovdFGb8KQ",
"http://www.youtube.com/watch?v=2k7RacpoIBk",
"http://www.youtube.com/watch?v=RftHvdwrEEk",
# second series
"http://www.youtube.com/watch?v=7nHU4S5uCnA",
"http://www.youtube.com/watch?v=HCI_FtnSnck",
"http://www.youtube.com/watch?v=ZL81ZxN_eo0",
"http://www.youtube.com/watch?v=T8a-kP6V3_g",
"http://www.youtube.com/watch?v=q1D39A_LQag",
"http://www.youtube.com/watch?v=1XYGfA4kJ1c",
"http://www.youtube.com/watch?v=Rn5JgItgKX4",
"http://www.youtube.com/watch?v=XsRBGl1wWAU",
"http://www.youtube.com/watch?v=veSnKC9hmWo",
"http://www.youtube.com/watch?v=A7mOOXZvqbQ",
"http://www.youtube.com/watch?v=o4IMzRr04AY",
"http://www.youtube.com/watch?v=vsN_Ff3bluU",
"http://www.youtube.com/watch?v=b2_1LccKj9c",
"http://www.youtube.com/watch?v=_WBRLitZZY8",
"http://www.youtube.com/watch?v=H1nFtEf96-M",
"http://www.youtube.com/watch?v=ADXJErS9vgs",
"http://www.youtube.com/watch?v=m5eTgR232V4",
"http://www.youtube.com/watch?v=LexZoELjR5c",
"http://www.youtube.com/watch?v=xAWhtFk5cMM",
"http://www.youtube.com/watch?v=Cmw_v2Y8o9k",
"http://www.youtube.com/watch?v=rVFEF4YNLnk",
"http://www.youtube.com/watch?v=tPHxDmNW7to",
"http://www.youtube.com/watch?v=H1KfRU8aEFY",
"http://www.youtube.com/watch?v=ViI55NckukI",
"http://www.youtube.com/watch?v=TeiEeR3jwd0",
"http://www.youtube.com/watch?v=1GSKhM57lo0",
"http://www.youtube.com/watch?v=JjpKSzb9kJM",
"http://www.youtube.com/watch?v=6zGBxlx0qeE",
"http://www.youtube.com/watch?v=srZfm_TIgwc"
]

# get total views
views = 0
for v in video_url:
    try:
     views += int(YouTube(v).views)
    except:
     views += 0

# get month and year
mydate = datetime.datetime.now()
mydate = mydate.strftime("%B")+" "+ str(mydate.strftime("%Y"))

# print stuff
print("All 21 classes are also available on [YouTube](https://www.youtube.com/@plumedorg1402). As of %s, they have been viewed %d times." % (mydate, views))
