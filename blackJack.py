from ctypes.wintypes import tagPOINT
from email import message
from pickle import LIST
from typing import Any, Set, Union, Dict, List, Tuple, Optional
#from utils.basicEvent import send
from plugins.wordle import WordleGame
from utils import standardPlugin
from utils.accountOperation import get_user_coins,update_user_coins
from utils.standardPlugin import StandardPlugin
from utils.responseImage_beta import ResponseImage,PALETTE_CYAN
from utils.basicConfigs import ROOT_PATH, SAVE_TMP_PATH, FONTS_PATH
from PIL import ImageFont, Image, ImageDraw
import os,re

from utils.standardPlugin import StandardPlugin

def send(*args):
    for arg in args:
        print(arg)

def drawHelpPic(savePath:str):
    helpWords=("""输入“21点 n”“黑杰克 n”“-blackjack n" 开始游戏；
小马和玩家各发两张扑克牌，小马的第一张为暗牌；
玩家可选择发送“要牌”获得一张扑克牌；
玩家发送“停止”停止要牌，小马亮出底牌；
若小马点数小于17则小马要牌，反之停止要牌；
最后最靠近21点的玩家获胜，获得两倍金币奖励；
若点数大于21点则立即失败；
A可视为1点或11点，JQK均为10点。""")
    helpCards=ResponseImage(
        title="21点帮助",
        titleColor= PALETTE_CYAN,
        width=1000,
        cardBodyFont= ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceHanSansCN-Medium.otf'), 24),
    )
    cardList=[];
    cardList.append(("body",helpWords))
    helpCards.addCard(ResponseImage.RichContentCard(
        raw_content=cardList,
        titleFontColor=PALETTE_CYAN,
    ))
    helpCards.generateImage(savePath)

class BlackJack(StandardPlugin):
    def __init__(self)->None:
        self.keyWord={
            "startPattern":re.compile(r"^(?:21点|黑杰克|-blackjack)\s*(\d+)$"),
            "wrongStartWord":("21点","黑杰克","-blackjack"),
            "addCardWord":("要牌"),
            "stopCardWord":("停止"),
            "forceStopWord":("结束")
        }
        self.games:Dict[int,Optional[BlackJackGame]]={}
        self.money:Dict[int,Optional[Dict[int,int]]]={}

    def judgeTrigger(self, msg: str, data: Any) -> bool:
        for i in self.keyWord.items:
            if isinstance(i,re.Pattern):
                if i.match(msg)!=None:
                    return True
            if isinstance(i,tuple):
                if msg in i:
                    return True
        return False
                
    def executeEvent(self,msg:str,data:Any)->Union[str,None]:
        groupId=data["group_id"]
        userId=data["user_id"]
        if self.startPattern.match(msg) !=None:
            game =self.games.get(groupId)
            if game==None:
                money=int(self.startPattern.findall(msg)[0])
                if money>get_user_coins(userId):
                    send(groupId,"[CQ:replay,id={message}]金币数量不足，当前拥有金币{coin}".format(message=data["message_id"],coin=get_user_coins(userId)))
                else:
                    update_user_coins(userId,-money,"黑杰克下注")
                    game=self.games[groupId]=BlackJackGame
                    self.money[userId]=money
                    game.getCard(2)
                    game.getCard(2,userId)
                    sendWord="游戏开始\n小马:暗 "
                    for i in game.showCard()[1:]:
                        sendWord+=i+" "
                    sendWord+="\n"
                    sendWord+=str(userId)+":"
                    for i in game.showCard():
                        sendWord+=i+" "
                    send(groupId,sendWord)
        else:
                money=int(self.startPattern.findall(msg)[0])
                if money>get_user_coins(userId):
                    send(groupId,"[CQ:replay,id={message}]金币数量不足，当前拥有金币{coin}".format(message=data["message_id"],coin=get_user_coins(userId)))
                else:
                    update_user_coins(userId,-money,"黑杰克下注")
                    game=self.games[groupId]=BlackJackGame
                    send(groupId,"加入成功")


            

                



class BlackJackGame:
    def __init__(self):
        card=[*['A']*4, *[(str(x)) for x in range(2,11)]*4,*['J']*4,*['Q']*4,*['K']*4]
        own=Dict[int,List[str]]
    
    def getCard(self,num:int=1,userId:int=0)->None:
        for _ in range(num):
            self.own[userId].append(self.card.shuffle().pop())

    def showCard(self,userId:int=0)->List[str]:
        return self.own[userId]

