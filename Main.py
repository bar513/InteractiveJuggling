
import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
warnings.warn("deprecated", DeprecationWarning)
from scipy.spatial import distance as dist
from collections import OrderedDict
from OurClasses import *
from JServer import *
from GlobalUsefullFunctions import *
from JGame import *
from PatternManager import *
import math

online = True
colors = [(255,0,0),[0,255,0],(0,0,255),[255,255,255]]
backSub = cv.createBackgroundSubtractorKNN(history = 20, dist2Threshold = 100) #1000
backSub2 = cv.createBackgroundSubtractorMOG2(history = 100, varThreshold = 100)#y
historyReal=History(999,4)

# ballsCounter=0
maxDistanceToMatch = 180
videoTrail = cv.VideoCapture("fireball.gif")
frameT_width = int(videoTrail.get(3))
frameT_height = int(videoTrail.get(4))
images = video_to_array('library1.mp4')

if online:
    myServer = JServer()
myGame = JGame()
myPatternManager = PatternManager()
for i in range(50):
        historyReal.insertAllBalls([Ball(0,0,0,Btype.REAL),Ball(0,0,0,Btype.REAL),Ball(0,0,0,Btype.REAL),Ball(0,0,0,Btype.REAL)],Btype.REAL)

vid = cv.VideoCapture(0)

# for count,img in enumerate(images):
while True:
    ret,img = vid.read()
    img = cv.resize(img, (640, 400))

    copy_img = img.copy()
    th_img, balls_list  , contours = ball_detection(img,backSub)
    hands_mask  = hands_detection(img, backSub2, detect = False, ball = None) #y

    balls_list = [ball for ball in balls_list if ball.area>50]
    numOfCandidates = len(balls_list)


    # print("len " + str(len(balls_list)),end='')
    # for b in balls_list:
    #     print("x " + str(b.x),end='')
    #     print("y " + str(b.y),end='')
    #     print("area " + str(b.area))
    # if np.mean(myPatternManager.numBallsHistory[-6:]) >3.8:
    #     if(np.mean(myPatternManager.numOfCandidates[-6:])<3.1):
    #         # for i in range(historyReal.numOfBalls):
    #         #     if historyReal.get(i).ballAlive:
    #         historyReal.get(0).ballAlive = False
    #         print("killed")
    #         # break

    # ballsAlive , aliveIDs,ballsDead,deadIDs, numOfBalls = historyReal.predictNumOfBalls(historySizeNotReal=20,historySizeSpeedKill=20,historySizeSpeedRevive=10,historySizeSizeRevive=10,THavgNotRealKill=0.85,THavgSpeedToKill=10,THavgSpeedToRevive=20,THavgSizeToRevive=70)
    ballsAlive , aliveIDs,ballsDead,deadIDs, numOfBalls = historyReal.predictNumOfBalls(historySizeNotReal=20,historySizeSpeedKill=20,historySizeSpeedRevive=15,historySizeSizeRevive=15,THavgNotRealKill=0.85,THavgSpeedToKill=10,THavgSpeedToRevive=20,THavgSizeToRevive=70)
    #kalman~~~~~~~~~~
    for idx,id in enumerate(aliveIDs):
        if(ballsAlive[idx].btype==Btype.REAL):
            ball = historyReal.get(id).kalmanPredict()
            ballsAlive[idx].x = ball.x
            ballsAlive[idx].y = ball.y
            ballsAlive[idx].btype = Btype.KALMAN_PREDICTION
    #kalman end~~~~~~
    lst=[]
    #~~~~alive balls~~~~~
    if len(ballsAlive) > 0:
        if len(balls_list) > 0:
            lst = get_closest_point(ballsAlive,balls_list) #lst[i][0]=old balls index,lst[i][1]=new balls index,lst[i][2]=distance
        else:
            lst = [(i,-1,-1) for i in range(len(aliveIDs))]

        historyReal.insertByLst(lst, aliveIDs, balls_list, img, backSub2, useHand=True,maxDistanceToMatch=maxDistanceToMatch)
        if len(balls_list) > 0:
            indices = [int(lst[i][1]) for i in range(len(lst))]
            balls_list = np.delete(balls_list, indices)


    #~~~~dead balls~~~~~
    if len(balls_list) > 0 and len(ballsDead) > 0:
        lst_dead = get_closest_point(ballsDead,balls_list)
        historyReal.insertByLst(lst_dead,deadIDs,balls_list,img,backSub2,useHand = False)




    patternTime, isStable, pattern = myPatternManager.getPattern(historyReal,numOfBalls,numOfCandidates)

    # print(patternTime)
    if patternTime==0:
        myGame.updatePattern(pattern)

    if patternTime>100 and pattern==Pattern.UNKNOWN:
        myGame.resetCounter()

    if patternTime>50 and (pattern==Pattern.ONE_BALL_ONE_HAND or pattern==Pattern.ONE_BALL_TWO_HANDS):
        myGame.startMinGame()
    else:
        if not (myGame.MG_isOn and (pattern==Pattern.ONE_BALL_ONE_HAND or pattern==Pattern.ONE_BALL_TWO_HANDS)):
            myGame.quitGame()

    myGame.checkCollusion([ballH[-1] for ballH in historyReal.arr if ballH.ballAlive])

    if historyReal.isNewBallAtMax():# and isStable:
        myGame.add1ToCounter()


    historyReal.drawLastBalls(copy_img)
    #trail part
    retT, frameT = videoTrail.read()
    if not retT:
        # print('no video')
        videoTrail.set(cv.CAP_PROP_POS_FRAMES, 0)
        retT, frameT = videoTrail.read()
        # continue


    historyReal.drawTrailsLastBalls(copy_img,640,400,frameT,frameT_width,frameT_height)


    # draw_label(copy_img, Pattern(pattern).name, (20,60), (255, 0, 0))
    # draw_label(copy_img, str(myGame.miniGameCounter), (20,80), (255, 0, 0))
    # draw_label(copy_img, str(myGame.miniGameScore), (20, 100), (255, 0, 0))
    if(myGame.MG_isOn):
        # print(myGame.MG_x,myGame.MG_y, myGame.MG_rad)
        cv.circle(copy_img, (myGame.MG_x,myGame.MG_y), myGame.MG_rad, (255,0,0), 7)
    # print(numOfBalls,"  ",numOfCandidates)
    copy_img = cv.flip(copy_img, 1)
    if online:
        myServer.sendData(copy_img,historyReal,patternNum=pattern,score=myGame.score,combo=myGame.getComboScore(),bonus=4,targetPosX=myGame.MG_x,targetPosY=myGame.MG_y,targetBonus=myGame.miniGameScore,targetCounter=myGame.miniGameCounter,b_totalCounter=myGame.totalCounter,b_combo_counter=myGame.comboCounter)

    cv.imshow('first_mask',th_img)
    cv.imshow('hands_mask',hands_mask)
    cv.imshow('real_time',copy_img)
    if cv.waitKey(1) and 0xFF == ord('q'):
        break

    # cv.waitKey(0)
cv.destroyAllWindows()