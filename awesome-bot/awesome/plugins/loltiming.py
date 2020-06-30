from datetime import datetime
import requests
import nonebot
import json
import re
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult, session, on_request
# on_command 装饰器将函数声明为一个命令处理器


#async def get_scence():
# url = "https://xz.aliyun.com/"
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.6) Gecko/20040206 Firefox/0.8'
#     }
# reponse = requests.get(url, headers=headers)
#     # if reponse.status_code == 200:
# pattern = re.compile('<a class="topic-title" href="(.*?)">\n(.*?)</a>', re.S)
# html = reponse.text
# items = re.findall(pattern, html)
# LMG = [];
# for item in items:
#     Lmg = item[1].strip()
#     Lmg1 = "https://xz.aliyun.com" + item[0]
#     #print(Lmg)
#     #print(Lmg1)
#     Lmg = item[1].strip()
#     Lmg1 = "https://xz.aliyun.com" + item[0]
#     Lmg2 = Lmg + " " + Lmg1
#     LMG.append(Lmg2)
# Lmg4 = LMG[0:4]
# Lmg3 = '\n'.join(Lmg4)
url = "http://l.zhangyoubao.com/news/"
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.6) Gecko/20040206 Firefox/0.8'
    }
reponse = requests.get(url, headers=headers)
reponse.encoding = "utf-8"
html = reponse.text
#if reponse.status_code == 200:
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
    #await session.send(Lmg3)
        # return str(Lmg3, encoding='utf-8')
	
@nonebot.scheduler.scheduled_job('cron', hour = 13, minute = 30)
async def _():
	bot = nonebot.get_bot()
	await bot.send_group_msg(group_id=, message=Lmg3)
	await bot.send_group_msg(group_id=, message=Lmg3)
	# url = "https://xz.aliyun.com/"
 #   headers = 
 #   {
 #           'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.6) Gecko/20040206 Firefox/0.8'
 #       }
 #   reponse = requests.get(url, headers=headers)
 #   if reponse.status_code == 200:
 #       pattern = re.compile('<a class="topic-title" href="(.*?)">\n(.*?)</a>', re.S)
 #       html = reponse.text
 #       items = re.findall(pattern, html)
 #       LMG = [];
 #       for item in items:
 #           Lmg = item[1].strip()
 #           Lmg1 = "https://xz.aliyun.com" + item[0]
 #           #print(Lmg)
 #           #print(Lmg1)
 #           Lmg = item[1].strip()
 #           Lmg1 = "https://xz.aliyun.com" + item[0]
 #           Lmg2 = Lmg + " " + Lmg1
 #           LMG.append(Lmg2)
 #       Lmg4 = LMG[0:4]
 #       Lmg3 = '\n'.join(Lmg4)
 #       #await session.send(Lmg3)
	#if hour == 11 or hour == '11':
		# await bot.send_group_msg(group_id=908082145, message=get_scence())