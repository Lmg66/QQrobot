# coding： utf8
import random,datetime
import os
from collections import Counter
'''
.start 开始
参加
退出
.white on/off 是否开启白板
.ok确认人数
.
.cs选择
所有人都选了后自动去除
判断是否结束
    输出进行下一轮
.reset回到确认人数
.readd回到确认人数，但是之前的人数没有清空
.reload当前游戏直接结束，按当前人重新分配词直接开始
'''

HAVE_WHITE = True


class WordLoader:

    def load_default_dict(self):
        with open("{}/spy_word.txt".format(os.path.split(os.path.realpath(__file__))[0]),encoding="utf-8") as f:
            self.lines = f.readlines()
    def random_choose(self,usewhite = True):
        li = random.choice(self.lines)
        li = li.strip()
        li = li.split(":")
        random.shuffle(li)
        result = li + ["白板"]
        return result
    def add_word(self,wa,wb):
        if ":" not in wa and ":"not in wb:
            self.lines.append("{}:{}".format(wa,wb))
            with open("spy_word.txt","w") as f:
                f.writelines(self.lines)
            print("添加 {}:{}".format(wa,wb))
        else:
            print("添加失败，请不要包含冒号")




def cdict(text, id):
    return {"text": text, "id": id}
class SpyGame:
    def __init__(self):
        self.word_chooser = WordLoader()
        self.word_chooser.load_default_dict()
        self.reset()

    def join(self,qq,nickname):
        if not self._assert_state(0):
            return False,cdict("state err",-2)

        if qq not in self.qq_set:
            self.qq_set.add(qq)
            self.name_dict[qq] = nickname
            return True,cdict("success",0)
        else:
            return False,cdict("have join",1)

    def quit(self,qq):
        if not self._assert_state(0):
            return False,cdict("state error",-2)

        if qq in self.qq_set:
            self.qq_set.remove(qq)
            self.name_dict.pop(qq)
            return True,cdict("success",0)
        else:
            return False,cdict("not join",1)

    def start(self):
        if self._assert_state(0) and len(self.qq_set) > 4:
            self.state = 1
            self._load_word()
            self._dispatch_word()
            self._dispatch_index()
            return True
        else:
            return False

    def _load_word(self):
        self.normal,self.spy,self.white = self.word_chooser.random_choose(True)
    def _dispatch_word(self):
        dispatch = [self.normal] * (len(self.qq_set)-2) + [self.spy] + [self.white]
        self._seed()
        random.shuffle(dispatch,)
        self.word_dict = {k:v for k,v in zip(self.qq_set,dispatch)}
    def _dispatch_index(self):
        index = 1
        for qq in self.qq_set:
            self.qq_index_dict[qq] = index
            self.index_qq_dict[index] = qq
            index = index + 1

    def _seed(self):
        random.seed(datetime.datetime.now().timestamp())
    def vote(self,qq,i):
        if not self._assert_state(1):
            return False

        if qq in self.kill_set:
            return False

        kill_index_set = {self.qq_index_dict[qq] for qq in self.kill_set}
        if i in kill_index_set:
            return False

        if i in self.index_qq_dict or i == 0:
            self.vote_dict[qq] = i
            return True
        else:
            return False

    def join_npc(self,num):
        if not self._assert_state(0):
            return

        self.quit_npc()
        for i in range(num):
            npc_qq = "10{}".format(i)
            self.npc_set.add("10{}".format(i))
            self.join(npc_qq,"npc_{}".format(i))

    def quit_npc(self):
        if not self._assert_state(0):
            return

        for qq in self.npc_set:
            self.quit(qq)
        self.npc_set.clear()

    def npc_vote(self):
        if not self._assert_state(1):
            return False

        self._seed()
        live_index_list = [self.qq_index_dict[qq] for qq in self.qq_set-self.kill_set]
        vote_set = random.choices(live_index_list,k=len(self.npc_set-self.kill_set))
        result = False
        for k,v in zip(self.npc_set-self.kill_set,vote_set):
            result = self.vote(k,v)
        return True

    def kill(self):
        if not self._assert_state(1):
            return False, cdict("status", -2)

        if len(self.vote_dict) != len(self.qq_set -self.kill_set):
            return False, cdict("not_enough", 1)
        be_kill = self._count_kill_list()
        if len(be_kill) == 1:#判断是否只剩一个人
            self.kill_set.add(be_kill[0])
            self.vote_dict.clear()
            return True, cdict("{}".format(self.qq_index_dict[be_kill[0]]), 2)
        else:#有多个人
            return False, cdict("many people", 3)

    def judge_winner(self):
        if not self._assert_state(1):
            return False,cdict("status not right",-2)

        normal_num = 0
        killed_spy_num = 0
        for i in self.kill_set:
            if self.get_identity_by_qq(i)["id"] == 0:
                normal_num = normal_num + 1
            else:
                killed_spy_num = killed_spy_num + 1

        if killed_spy_num == 2:
            self.state = 2
            return True,cdict("平民，存活的平民有"+"、".join([self.name_dict[qq] for qq in self.qq_set-self.kill_set]),0)
        else:
            last = self.qq_set - self.kill_set
            print(killed_spy_num,last)
            if len(last) - (2-killed_spy_num ) < 2:
                self.state = 2
                return True,cdict("卧底，存活的卧底有"+"、".join([self.name_dict[qq] for qq in self.qq_set-self.kill_set if self.get_identity_by_qq(qq)["id"] != 0]),1)


        return False,cdict("not end",-1)

    def _count_kill_list(self):
        count = Counter(self.vote_dict.values())
        if 0 in count:
            count.pop(0)
        be_kill = count.most_common(1)
        if len(be_kill) == 0:
            return None
        else:
            be_kill = be_kill[0]

        be_kill_list = []
        print(count,be_kill)
        for k,v in count.items():
            if be_kill[1] == v:
                be_kill_list.append(self.index_qq_dict[k])
        print(be_kill_list)
        return be_kill_list

    def reset(self):
        self.normal = None
        self.spy = None
        self.white = None
        self.name_dict = {}
        self.word_dict = {}
        self.qq_index_dict = {}
        self.index_qq_dict = {}
        self.npc_set = set()
        self.qq_set = set()
        self.kill_set = set()
        self.vote_dict = {}
        self.state = 0
        return True

    def readd(self):
        self.normal = None
        self.spy = None
        self.white = None
        self.word_dict = {}
        self.qq_index_dict = {}
        self.index_qq_dict = {}
        self.kill_set = set()
        self.vote_dict = {}
        self.state = 0

    def restart(self):
        self.readd()
        return self.start()

    def out_join_list(self):
        st = ""
        for k,v in self.name_dict.items():
            st = st + "{}\n".format(v)
        return st
    def out_live_list(self):
        st = ""
        last = self.qq_set-self.kill_set
        for qq in last:
            st = st + "{}. {}\n".format(self.qq_index_dict[qq],self.name_dict[qq])
        return st
    def out_vote_list(self):
        st = ""
        count = Counter(self.vote_dict.values())
        for k,v in count.items():
            st = st + "{}. {}:{}票\n".format(k,self.get_name_by_index(k),v)
        return st

    def out_index_list(self):
        st = ""
        for k in self.index_qq_dict.keys():
            st = st + "{}. {}\n".format(k,self.get_name_by_index(k))
        return st
    def out_name_word_list(self):
        st = ""
        for k,v in self.word_dict.items():
            if k in self.kill_set:
                st = st + "[{}]{} : {}\n".format("投出", self.name_dict[k], v)
            else:
                st = st + "[{}]{} : {}\n".format("胜利",self.name_dict[k],v)
        return st

    def get_identity_by_index(self,index):
        return self.get_identity_by_qq(self.index_qq_dict[index])

    def get_name_by_qq(self,qq):
        return self.name_dict[qq]
    def get_index_by_qq(self,qq):
        return self.qq_index_dict[qq]
    def get_qq_by_index(self,index):
        return self.index_qq_dict[index]
    def get_name_by_index(self,index):
        if index == 0:
            return "弃票"
        return self.name_dict[self.index_qq_dict[index]]
    def get_identity_by_qq(self,qq):
        if self.word_dict[qq] == self.normal:
            return {"text":"普通人","id":0}
        elif self.word_dict[qq] == self.spy:
            return {"text":"卧底","id":1}
        else:
            return {"text":"卧底","id":2}

    def _assert_state(self,i):
        return self.state == i

if __name__ == "__main__":
    w = WordLoader()
    w.load_default_dict()
    for i in range(5):
        a,b,c = w.random_choose(True)
        print(a,b,c)
