import requests
import re
import json
from nonebot import on_command, CommandSession
@on_command('lol新闻', aliases=('lol新闻'))
async def weather(session: CommandSession):
    url = "http://l.zhangyoubao.com/news/"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.6) Gecko/20040206 Firefox/0.8'
        }
    reponse = requests.get(url, headers=headers)
    reponse.encoding = "utf-8"
    html = reponse.text
    if reponse.status_code == 200:
        pattern = re.compile('<h2><a class="omit" target="_blank" href="(.*)" title=".*">(.*)</a></h2>')
        #html = reponse.text
        items = re.findall(pattern, html)
        #print(items)
        LMG = [];
        for item in items:
            Lmg = item[1].strip()
            Lmg1 = item[0]
            Lmg2 = Lmg + " " + Lmg1
            LMG.append(Lmg2)
        Lmg4 = LMG[0:5]
        Lmg3 = '\n'.join(Lmg4)
        #print(Lmg3)
        await session.send(Lmg3)