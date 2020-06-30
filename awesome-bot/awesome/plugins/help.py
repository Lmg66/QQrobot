from nonebot import on_command, CommandSession
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('help', aliases=('使用帮助', '帮助', '使用方法'))
async def weather(session: CommandSession):
	await session.send('我现在支持的功能有: \n 1.天气，食用方法"小安+天气" \n 2.图灵对话，食用方+你想说的话" \n 3.信息的获取，食用方法"小安+碧蓝航线"还可以+知乎+steam+新番+*年*月有什么新番+先知社区 \n 4.游戏功能,食用方法"小安+谁是卧底"---->测试ing \n 5.以图搜番，食用方法"小安+以图搜番" \n 6.音乐功能,食用方法"小安+来首"------>此处有bug不建议食用会让小安卡住 \n 7.早安，午安，晚安 \n 还有隐藏功能哦，不妨输入"小安+来个涩图”试试有惊喜哦，嘻嘻嘻')