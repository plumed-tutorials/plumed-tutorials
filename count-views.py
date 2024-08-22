from pytube import YouTube
import datetime

video_url = [
# first series
"https://www.youtube.com/watch?v=2eGhMSdIJEs&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=1&pp=iAQB",
"https://www.youtube.com/watch?v=TzSxBnX4uDk&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=2&pp=iAQB",
"https://www.youtube.com/watch?v=dJKajNwbJ74&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=3&pp=iAQB",
"https://www.youtube.com/watch?v=XKqislC2GYA&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=4&pp=iAQB",
"https://www.youtube.com/watch?v=gHXXGYIgasE&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=5&pp=iAQB",
"https://www.youtube.com/watch?v=SuHcOYqIOrY&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=6&pp=iAQB",
"https://www.youtube.com/watch?v=q0RHlFAk544&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=7&pp=iAQB",
"https://www.youtube.com/watch?v=UgTIGQxJtOc&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=8&pp=iAQB",
"https://www.youtube.com/watch?v=v_CCLyjQ3yI&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=9&pp=iAQB",
"https://www.youtube.com/watch?v=0o9rV2cWiJU&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=10&pp=iAQB",
"https://www.youtube.com/watch?v=EoErcfzwtA8&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=11&pp=iAQB",
"https://www.youtube.com/watch?v=PJovdFGb8KQ&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=12&pp=iAQB",
"https://www.youtube.com/watch?v=2k7RacpoIBk&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=13&pp=iAQB",
"https://www.youtube.com/watch?v=RftHvdwrEEk&list=PLmdKEn2znJEld8l6Hp9PXf4EursC4-8nC&index=14&pp=iAQB",
# second series
"https://www.youtube.com/watch?v=7nHU4S5uCnA&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=1&pp=iAQB",
"https://www.youtube.com/watch?v=HCI_FtnSnck&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=2&pp=iAQB",
"https://www.youtube.com/watch?v=ZL81ZxN_eo0&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=3&pp=iAQB",
"https://www.youtube.com/watch?v=T8a-kP6V3_g&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=4&pp=iAQB",
"https://www.youtube.com/watch?v=q1D39A_LQag&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=5&pp=iAQB",
"https://www.youtube.com/watch?v=1XYGfA4kJ1c&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=6&pp=iAQB",
"https://www.youtube.com/watch?v=Rn5JgItgKX4&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=7&pp=iAQB",
"https://www.youtube.com/watch?v=XsRBGl1wWAU&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=8&pp=iAQB",
"https://www.youtube.com/watch?v=veSnKC9hmWo&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=9&pp=iAQB",
"https://www.youtube.com/watch?v=A7mOOXZvqbQ&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=10&pp=iAQB",
"https://www.youtube.com/watch?v=o4IMzRr04AY&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=11&pp=iAQB",
"https://www.youtube.com/watch?v=vsN_Ff3bluU&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=12&pp=iAQB",
"https://www.youtube.com/watch?v=b2_1LccKj9c&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=13&pp=iAQB",
"https://www.youtube.com/watch?v=_WBRLitZZY8&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=14&pp=iAQB",
"https://www.youtube.com/watch?v=H1nFtEf96-M&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=15&pp=iAQB",
"https://www.youtube.com/watch?v=ADXJErS9vgs&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=16&pp=iAQB",
"https://www.youtube.com/watch?v=m5eTgR232V4&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=17&pp=iAQB",
"https://www.youtube.com/watch?v=LexZoELjR5c&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=18&pp=iAQB",
"https://www.youtube.com/watch?v=xAWhtFk5cMM&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=19&pp=iAQB",
"https://www.youtube.com/watch?v=Cmw_v2Y8o9k&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=20&pp=iAQB",
"https://www.youtube.com/watch?v=rVFEF4YNLnk&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=21&pp=iAQB",
"https://www.youtube.com/watch?v=tPHxDmNW7to&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=22&pp=iAQB",
"https://www.youtube.com/watch?v=H1KfRU8aEFY&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=23&pp=iAQB",
"https://www.youtube.com/watch?v=ViI55NckukI&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=24&pp=iAQB",
"https://www.youtube.com/watch?v=TeiEeR3jwd0&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=25&pp=iAQB",
"https://www.youtube.com/watch?v=1GSKhM57lo0&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=26&pp=iAQB",
"https://www.youtube.com/watch?v=JjpKSzb9kJM&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=27&pp=iAQB",
"https://www.youtube.com/watch?v=6zGBxlx0qeE&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=28&pp=iAQB",
"https://www.youtube.com/watch?v=srZfm_TIgwc&list=PLmdKEn2znJEmCw1OfLLhv43TXl-QDvkUO&index=29&pp=iAQB"
]

views = 0
for v in video_url:
    yt = YouTube(v)
    views += int(yt.views)

mydate = datetime.datetime.now()
mydate = mydate.strftime("%B")+" "+ str(mydate.strftime("%Y"))
print("All classes have been recorded and are available on [YouTube](https://www.youtube.com/@plumedorg1402). As of %s, they have been viewed %d times. In 2024, PLUMED Masterclass lectures were converted to PLUMED Tutorials and are available [here](https://www.plumed-tutorials.org/browse?search=masterclass)." % (mydate, views))
