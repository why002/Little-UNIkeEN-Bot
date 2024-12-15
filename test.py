from subprocess import list2cmdline
from turtle import update
#from blackJack import BlackJack
from wordle import *
from utils.accountOperation import update_user_coins
#from blackJack import drawHelpPic
from utils.basicConfigs import ROOT_PATH, SAVE_TMP_PATH, FONTS_PATH
import os
#savePath=os.path.join(ROOT_PATH,SAVE_TMP_PATH,"test.png")
#drawHelpPic(savePath)
#print(savePath)
a=re.compile(r"s")
print(type(a))
print(isinstance(a,re.Pattern))
#black=BlackJack()

#while True:
#    word=str(input())
#    black.executeEvent(word,{"user_id":1,"group_id":1})
