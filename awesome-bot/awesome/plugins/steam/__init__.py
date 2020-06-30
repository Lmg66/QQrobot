import re
import asyncio
from requests import *
from bs4 import *
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult
from nonebot import on_command, CommandSession
from .Smile import get_steam
import lxml


def get_resource():
    url = 'https://www.newyx.net/news/steam1/'
    data = get(url).text
    bs = BeautifulSoup(data, 'lxml').find_all('li', class_='humor')
    bs1 = bs[0:4]
    return bs1


@on_command('steam', aliases=('steam'))
async def scence(session: CommandSession):
    try:
        a = session.event['group_id']
        if a == 586078667:
            return
    except:
        pass
    bs = get_resource()
    src = ''
    for i in bs:
        c = i.a.img.get('alt')
        c = str(c).replace("免费领取", "").replace("steam喜加一", '')
        b = i.a.get('href')
        uri = get_steam_url(b)
        if uri is None:
            continue
        src += c + '\n' + str(uri) + '-----------------------\n'
    await session.send(src)


def get_steam_url(url):
    date = get(url).text
    bs = BeautifulSoup(date, 'lxml').find_all('p', style='text-indent:2em;')
    uri = ''
    for i in bs:
        a = i.strong
        if a is None:
            continue
        if re.search('领取地址', i.get_text()) and re.search('\s', i.get_text()):
            uri += i.get_text()
            return uri


@on_natural_language(keywords=('喜加一'), only_to_me=False)
async def _(session: NLPResult):
    return IntentCommand(90.0, 'steam')


@on_command('STEAM', aliases=('steam促销'))
async def scence(session: CommandSession):
    a = ''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    bs = get_steam()
    await session.send(bs)


@on_natural_language(keywords=('促销'), only_to_me=False)
async def _(session: NLPResult):
    return IntentCommand(90.0, 'STEAM')