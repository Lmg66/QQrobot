import requests
import re
from nonebot import on_command, CommandSession
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('aliyun', aliases=('先知社区'))
async def weather(session: CommandSession):
    url = "https://xz.aliyun.com/"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.6) Gecko/20040206 Firefox/0.8'
        }
    reponse = requests.get(url, headers=headers)
    if reponse.status_code == 200:
        pattern = re.compile('<a class="topic-title" href="(.*?)">\n(.*?)</a>', re.S)
        html = reponse.text
        items = re.findall(pattern, html)
        LMG = [];
        for item in items:
            Lmg = item[1].strip()
            Lmg1 = "https://xz.aliyun.com" + item[0]
            #print(Lmg)
            #print(Lmg1)
            Lmg = item[1].strip()
            Lmg1 = "https://xz.aliyun.com" + item[0]
            Lmg2 = Lmg + " " + Lmg1
            LMG.append(Lmg2)
        Lmg4 = LMG[0:4]
        Lmg3 = '\n'.join(Lmg4)
        await session.send(Lmg3)
