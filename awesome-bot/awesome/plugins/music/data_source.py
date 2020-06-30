import json
import requests

async def get_song_of_music(music: str) -> str:
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=1&w=' + music
    data_text = requests.get(url).text
    data_json = json.loads(data_text[9:-1])
    songid = data_json["data"]["song"]["list"][0]["songid"]
    repass = "[CQ:music,type=qq,id=" + str(songid) + "]"
    print(repass)

    return repass
    # url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?w=" + music + "&format=json&n=10"
    # resopse = requests.get(url).text
    # content = json.loads(resopse)
    # musiclist=content['data']['song']['list']
    # # 这里简单的把这些歌详细的整理成json数据
    # all_data = {}
    # datas = []
    # for music in musiclist:
    #     data = {}
    #     data['name'] = music['songname']
    #     sgs = ""
    #     for sg in music['singer']:
    #         sgs += sg['name'] + " "
    #     data['sginer'] = sgs
    #     data['id'] = music['songid']
    #     datas.append(data)
    # all_data['result'] = datas
    # all_data['type'] = 'qq'
    # # 不需要精确判断，直接返回第一首歌
    # #添加歌手
    # signs=""
    # for sign in musiclist[0]['singer']:
    #     signs+=sign['name']+" "
    # all_data['singr']=signs
    # all_data['id'] = musiclist[0]['songid']
    # all_data['name']=musiclist[0]['songname']
    # return all_data