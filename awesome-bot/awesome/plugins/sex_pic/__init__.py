from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult
from nonebot import on_command, CommandSession
from requests import get, post
import re
import json
from .cache import *
import queue
import asyncio


async def get_sex_img(urls):
    global img
    url = urls
    data = get(url).text
    if data.startswith(u'\ufeff'):
        data = data.encode('utf8')[3:].decode('utf8')
        img = json.loads(data).get('imgurl')
    return img


@on_command('sex_pic', aliases=('猛男'),only_to_me=False)
async def sex_pic(session: CommandSession):
    a = ''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    url = 'https://api.ixiaowai.cn/api/api.php?return=json'
    src = await  get_sex_img(url)
    await session.send(src)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    test = session.msg
    try:
        re.search('CQ:image,file=B407F708A2C6A506342098DF7CAC4A57.jpg', test).span()
        return IntentCommand(90.0, 'R18')
    except:
        pass


@on_command('scence', aliases=('风景', '来份风景'))
async def scence(session: CommandSession):
    a=''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    url = 'https://api.ixiaowai.cn/gqapi/gqapi.php?return=json'
    src = await  get_sex_img(url)
    await session.send(src)


@on_natural_language(keywords=('风景', '照片'), only_to_me=False)
async def _(session: NLPResult):

    return IntentCommand(90.0, 'scence')


tasks = []


async def run():
    task = asyncio.ensure_future(get_sex())
    tasks.append(task)


async def get_sex():
    url = 'https://api.lolicon.app/setu/?apikey=705545485e92e380931b56'
    src = await get_seTu(url)
    message_src.put(src)


@on_command('R18', aliases=('色图', '来份涩图'))
async def scence(session: CommandSession):
    url = 'https://api.lolicon.app/setu/?apikey=705545485e92e380931b56'
    loop = asyncio.get_event_loop()
    a = ''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    if message_src.empty():
        await session.send("图库缺图，正在加载中，请稍等五秒~")
        await run()
        loop.run_until_complete(asyncio.wait(tasks))
        tasks.clear()
    await session.send(message_src.get())
    await run()
    loop.run_until_complete(asyncio.wait(tasks))


@on_natural_language(keywords=('炼铜', '色图', '涩图'), only_to_me=False)
async def _(session: NLPResult):
    return IntentCommand(90.0, 'R18')


async def get_seTu(url):
    data = get(url).json()
    data = str(data['data'])
    data = replace_char(data, '', 0)
    data = replace_char(data, '', len(data) - 1)
    data = str(data).replace("\'", '\"').replace("False", '\"False\"')
    print(data[169])
    data = json.loads(data)
    src = data['url'] + '\ntiltle:' + data['title'] + '\nauthor:' + data['author']
    return src


def replace_char(string, char, index):
    string = list(string)
    string[index] = char
    return ''.join(string)