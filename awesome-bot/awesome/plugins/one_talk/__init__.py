from datetime import datetime
import random
import nonebot
from aiocqhttp.default import on_message
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult, session, on_request
from nonebot import on_command, CommandSession
from requests import get
from bs4 import BeautifulSoup
import lxml
import json
import asyncio
from .music_config import *
from .goodMorning_talk import *


async def get_scence():
    url = "https://v1.hitokoto.cn/?j=j&a=a&i=i"
    data = get(url).json()
    who = '' if data['from_who'] == None else data['from_who']
    bs = data['hitokoto'] + '\n——《' + data['from'] + '》' + who
    return bs


tasks = []


@nonebot.scheduler.scheduled_job(
    'cron',
    day='*',
    hour='8,22,0'
)
async def dateTime_weather():
    loop = asyncio.get_event_loop()
    bot = nonebot.get_bot()
    hour = datetime.today().hour
    group_list = await bot.get_group_list()
    message = morning[random.randint(0, len(morning) - 1)]
    if hour == 8 or hour == '8':
        for i in group_list:
            task = asyncio.ensure_future(goodmorning(i, message))
            tasks.append(task)
    elif hour == 0:
        for i in group_list:
            task = asyncio.ensure_future(NNight(i))
            tasks.append(task)
    elif hour >= 22 or hour <= 5:
        for i in group_list:
            task = asyncio.ensure_future(goodNight(i, message))
            tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))


async def NNight(i):
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=i['group_id'], message="噔噔咚~已经十二点了,猝死高危人群需要睡觉啦")


async def goodmorning(i, message):
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=i['group_id'], message="早安")
    await bot.send_group_msg(group_id=i['group_id'], message=message)


async def goodNight(i, message):
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=i['group_id'], message="晚安")
    await bot.send_group_msg(group_id=i['group_id'], message=message)


@on_command('one_talk', aliases=('一言'), only_to_me=False)
async def one_talke(session: CommandSession):
    talk = session.state
    await session.send(talk)
    src = await get_scence()
    await session.send(src)


@on_natural_language(keywords=('晚安', '早安', '午安'), only_to_me=False)
async def _(session: NLPSession):
    d = datetime.today().hour
    src = session.msg_text
    src = str(src).replace(' ', '')
    if src == '晚安' or src == '早安' or src == '午安' or src == '早':
        if 4 < d < 11:
            await session.send("早安")
        elif 11 <= d <= 16:
            await session.send("午安")
        elif 18 <= d <= 23:
            await session.send("晚安")
        elif 0 <= d <= 5:
            await session.send(f"夜已经深了，分享一个纯音歌单给你，祝好梦，晚安\n{music[random.randint(0,len(music))]}")
    else:
        return
    return IntentCommand(90.0, 'one_talk')