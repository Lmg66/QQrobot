# coding： utf8
from .spygame import *
from aiocqhttp.exceptions import ActionFailed
import nonebot
game_dict = {}

from nonebot import on_command, CommandSession


auto_fp = False
game_start = False


@on_command('create', aliases=("Create","Reset",'谁是卧底', '开房',"reset","重置"),only_to_me=True)
async def create(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            game_dict[group_id] = SpyGame()

        result = game_dict[group_id].reset()
        global game_start
        game_start = True
        await session.send("谁是卧底游戏开始啦，输入'参加'、'加入'加入游戏吧")
    else:
        await session.send("不要私聊发我这个了啦")



@on_command('join', aliases=('Join','参加', '加入'), only_to_me=False)
async def join(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，艾特我输入start、‘谁是卧底’开始吧")
            return
        else:
            qq = session.ctx["sender"]["user_id"]
            nickname = session.ctx["sender"]["nickname"]
            result, msg = game_dict[group_id].join(qq, nickname)
            if result:
                await session.send("{}加入游戏成功,当前加入的人有\n".format(nickname) + game_dict[group_id].out_join_list())
            else:
                if msg["id"] == 1:
                    await session.send("{},你已经加入本次游戏了,不用重复加入啦".format(nickname))
                else:
                    await session.send("游戏已经开始，等待下一次游戏再加入吧~")

    else:
        await session.send("不要私聊发我这个了啦")



@on_command('quit', aliases=('Quit','不玩了', '退出'), only_to_me=False)
async def quit(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return
        qq = session.ctx["sender"]["user_id"]
        nickname = session.ctx["sender"]["nickname"]
        result,msg = game_dict[group_id].quit(qq)
        if result:
            game_dict[group_id].quit(qq)
            await session.send("{}退出了本次游戏，下次再一起玩吧~".format(nickname))
        else:
            if msg["id"] < 0:
                await session.send("游戏已经开始，下次再来加入吧")
            else:
                await session.send("{},你还没有加入游戏，不来尝试一下吗".format(nickname))
    else:
        await session.send("不要私聊发我这个了啦")



@on_command('start', aliases=('开始',"ok"), only_to_me=False)
async def start(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入create、‘谁是卧底’开始吧")
            return


        result = game_dict[group_id].start()
        if result:
            word_dict = game_dict[group_id].word_dict
            bot = nonebot.get_bot()
            for k,v in word_dict.items():

                try:
                    await bot.send_private_msg(user_id = k, message = v)
                    # await bot.send_msg(message_type = "private",user_id=1772190525, message='哇',auto_escape = True)
                except ActionFailed as e:
                    print(e.retcode)

            await session.send("----Game Start----")
            await session.send("参与的玩家及其序号为::\n"+game_dict[group_id].out_index_list())

        else:
            await session.send("人数不足无法开始或者游戏已经开始，请静等游戏结束~或者输入reset、readd、restart、create重新开始游戏")
    else:
        await session.send("不要私聊发我这个了啦")




@on_command('cs',aliases=["投","Cs"],only_to_me=False)
async def cs(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return
        qq = session.ctx["sender"]["user_id"]
        nickname = session.ctx["sender"]["nickname"]

        vote_index = session.get('vote_index', prompt='你想投哪个人呢？下一次直接输入编号即可无需加前缀cs')
        try:
            vote_index = int(vote_index)
        except:
            await session.send("{}投票无效，请输入正确序号".format(nickname))
            return

        result = game_dict[group_id].vote(qq,vote_index)
        if result:
            await session.send("{}投了{}号({}),目前投票情况为\n".format(nickname,vote_index,game_dict[group_id].get_name_by_index(vote_index))+game_dict[group_id].out_vote_list())
        else:
            await session.send("{}投票无效，请输入正确序号".format(nickname))

    else:
        await session.send("不要私聊发我这个了啦")


# start.args_parser 装饰器将函数声明为 start 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@cs.args_parser
async def cs_parser(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    print(session.current_arg_text)
    print(session.ctx["message"])
    if session.current_key:
        # 如果当前正在向用户询问更多信息（本例中只有可能是要查询的城市），则直接赋值
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        # 如果当前没有在询问，但用户已经发送了内容，则理解为要查询的城市
        # 这种情况通常是用户直接将城市名跟在命令名后面，作为参数传入
        session.args['vote_index'] = stripped_arg


@on_command('ce',aliases=["Ce","投票结束"],only_to_me=False)
async def ce(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return
        result,msg = game_dict[group_id].kill()
        if result:
            await session.send("最终结果:{}号({})被投出,ta是{}".format(msg["text"],game_dict[group_id].get_name_by_index(int(msg["text"])),game_dict[group_id].get_identity_by_index(int(msg["text"]))["text"]))
            wresult,wmsg = game_dict[group_id].judge_winner()
            if wresult:
                if auto_fp:
                    await session.send("游戏结束！最终胜利者是:{}\n词语分配情况为:\n".format(wmsg["text"],game_dict[group_id].out_name_word_list()))
                else:
                    await session.send("游戏结束！最终胜利者是:{}\n输入.fp查看词语分配".format(wmsg["text"]))
            else:
                await session.send("游戏继续...下一轮投票开始")

        else:
            if msg["id"] < 0:
                pass
            else:
                await session.send("没有办法完成投票，因为"+msg["text"])

    else:
        await session.send("不要私聊发我这个了啦")


@on_command('fp',aliases=["复盘","Fp"],only_to_me=False)
async def fp(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return

        if game_dict[group_id].state == 2:
            await session.send("词语分配情况为:\n{}".format(game_dict[group_id].out_name_word_list()))
        else:
            await session.send("游戏还没有结束，不能查看词语分配情况，大家再加把劲吧")

    else:
        await session.send("不要私聊发我这个了啦")




@on_command('readd',aliases=["重新加入","Readd"],only_to_me=False)
async def readd(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return
        game_dict[group_id].readd()
        await session.send("谁是卧底游戏开始啦，输入'参加'、'加入'加入游戏吧")
        await session.send("当前人员延续上一局游戏，已经加入的人有:\n" + game_dict[group_id].out_join_list())

    else:
        await session.send("不要私聊发我这个了啦")



@on_command('restart',aliases=["重新开始","Restart"],only_to_me=False)
async def restart(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            game_dict[group_id] = SpyGame()
            await session.send("游戏没有进行过...重置中...游戏开始，输入join、参加、加入加入游戏")
            return
        result = game_dict[group_id].restart()
        if result:
            word_dict = game_dict[group_id].word_dict
            bot = none.get_bot()
            for k, v in word_dict.items():

                try:
                    await bot.send_private_msg(user_id=k, message=v)
                    # await bot.send_msg(message_type = "private",user_id=1772190525, message='哇',auto_escape = True)
                except ActionFailed as e:
                    print(e.retcode)


            await session.send("----Game Start----")
            await session.send("参与的玩家及其序号为::\n" + game_dict[group_id].out_index_list())

    else:
        await session.send("不要私聊发我这个了啦")






@on_command('npc',aliases=["Npc"],only_to_me=False)
async def npc(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return
        qq = session.ctx["sender"]["user_id"]
        nickname = session.ctx["sender"]["nickname"]

        npc_num = session.get('npc_num', prompt='你想加入几个npc？下一次直接输入数字即可无需加前缀cs')
        if npc_num == "off":
            game_dict[group_id].quit_npc()
            return

        try:
            npc_num = int(npc_num)
        except:
            await session.send("{}数字无效，请输入阿拉伯数字即可，建议1-5个".format(nickname))
            return

        game_dict[group_id].join_npc(npc_num)
        await session.send("加入了{}个npc，现在的游戏成员有:\n".format(npc_num)+game_dict[group_id].out_join_list())

    else:
        await session.send("不要私聊发我这个了啦")


# start.args_parser 装饰器将函数声明为 start 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@npc.args_parser
async def npc_parser(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    print(session.current_arg_text)
    print(session.ctx["message"])
    if session.current_key:
        # 如果当前正在向用户询问更多信息（本例中只有可能是要查询的城市），则直接赋值
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        # 如果当前没有在询问，但用户已经发送了内容，则理解为要查询的城市
        # 这种情况通常是用户直接将城市名跟在命令名后面，作为参数传入
        session.args['npc_num'] = stripped_arg




@on_command('nv',aliases=["Nv"],only_to_me=False)
async def npc(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        if not game_start:
            return
        group_id = session.ctx["group_id"]
        if session.ctx["group_id"] not in game_dict:
            await session.send("游戏还没有开始，@我输入start、‘谁是卧底’开始吧")
            return

        result = game_dict[group_id].npc_vote()
        if result:
            await session.send("npc投票成功,目前投票情况为\n"+game_dict[group_id].out_vote_list())
        else:
            await session.send("npc投票失败，没有npc或者不在投票流程中")


    else:
        await session.send("不要私聊发我这个了啦")


@on_command('close',aliases=["Close","结束","结束游戏"],only_to_me=False)
async def close(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    if "group_id" in session.ctx:
        global game_start
        if not game_start:
            return
        await session.send("关闭游戏，下次@我再开房吧~")

        game_start = False


    else:
        await session.send("不要私聊发我这个了啦")
