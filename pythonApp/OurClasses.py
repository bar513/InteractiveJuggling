from collections import deque
import itertools
from enum import Enum
from ball_predictor import BallPredictor
import numpy as np
import cv2 as cv
from DrawFunctions import *
class Btype(Enum):
    REAL = 1
    CORRECTION =2
    PREDICTION = 3
    HAND=4
    DUPLICATE=5
    KALMAN_PREDICTION=6
    NONE=7



class Extremom(Enum):
    MIN = 1
    MAX =2
    NONE = 3

class Direction(Enum):
    NONE = 1
    RIGHT =2
    LEFT = 3

class BallHistory:
    def __init__(self,historySize,id,color):
        self.historySize=historySize
        self.x = []
        self.y = []
        self.area = []
        self.btype = []
        self.yExtremom =[]
        self.speed = []
        self.kalmanPredictor = BallPredictor()
        self.ballAlive = False
        self.id = id
        self.color  = color
        self.lastTrailResize = 0.1 # the default may affect the first trails

        self.yExtremomDir = []
        self.xVar = []
        self.yVar = []
        self.varHistoryLen = 25

    def append(self,ball,overrideBtype=Btype.NONE):
        speed = np.linalg.norm((self.x[-1]-ball.x,self.y[-1]-ball.y)) if len(self.speed)>0 else 1
        self.speed.append(speed)
        self.x.append(ball.x)
        self.y.append(ball.y)
        self.area.append(ball.area)


        ballBtype = ball.btype if overrideBtype==Btype.NONE else overrideBtype
        self.btype.append(ballBtype)



        if len(self.y)>5:
            if self.y[-2] > self.y[-1] and self.y[-2] > self.y[-3] and np.mean(np.array(self.yExtremom[-5:])!=Extremom.NONE)==0: #7
                self.yExtremom.append(Extremom.MIN)
            elif self.y[-2] < self.y[-1] and self.y[-2] < self.y[-3] and np.mean(np.array(self.yExtremom[-8:])==Extremom.MAX)==0:# and self.y[-2] + 60 < self.y[-5]:
                self.yExtremom.append(Extremom.MAX)
            else:
                self.yExtremom.append(Extremom.NONE)
        else:
            self.yExtremom.append(Extremom.NONE)

        if len(self.y)>self.varHistoryLen:
            self.yExtremomDir.append(Direction.RIGHT if (self.x[-1] - self.x[-4]) > 0 else Direction.LEFT)
            self.xVar.append(np.var(self.x[-self.varHistoryLen:]))
            self.yVar.append(np.var(self.y[-self.varHistoryLen:]))
        else:
            self.yExtremomDir.append(Direction.NONE)
            self.xVar.append(0)
            self.yVar.append(0)

        if len(self.x)>self.historySize:
            self.x.pop(0)
        if len(self.y)>self.historySize:
            self.y.pop(0)
        if len(self.area)>self.historySize:
            self.area.pop(0)
        if len(self.btype) > self.historySize:
            self.btype.pop(0)
        if len(self.yExtremom) > self.historySize:
            self.yExtremom.pop(0)
        if len(self.speed) > self.historySize:
            self.speed.pop(0)

        if len(self.yExtremomDir) > self.historySize:
            self.yExtremomDir.pop(0)
        if len(self.xVar) > self.historySize:
            self.xVar.pop(0)
        if len(self.yVar) > self.historySize:
            self.yVar.pop(0)

        if ball.btype == Btype.REAL:
            self.kalmanPredictor.update((ball.x,ball.y))

    def kalmanPredict(self):
        x,y = self.kalmanPredictor.predict()
        return Ball(x,y,0,Btype.KALMAN_PREDICTION)

    def isAlive(self,historySizeNotReal=20,historySizeSpeedKill=20,historySizeSpeedRevive=20,historySizeSizeRevive=20,THavgNotRealKill=0.85,THavgSpeedToKill=10,THavgSpeedToRevive=10,THavgSizeToRevive=70): #can be more efficient to count the new ones and avoid mean every time
        if len(self.btype) <= np.max([historySizeNotReal,historySizeSpeedKill,historySizeSpeedRevive,historySizeSizeRevive]):
            return self.ballAlive
        else:
            if self.ballAlive:
                # kill ball by not being real
                averageNotReal = np.mean(np.array(self.btype[-historySizeNotReal:]) != Btype.REAL)
                if averageNotReal > THavgNotRealKill:
                    return False
                # kill ball that is static
                averageSpeed = np.mean(self.speed[-historySizeSpeedKill:])
                if averageSpeed < THavgSpeedToKill:
                    return False

                return True
            else:
                averageSize = np.mean(self.area[-historySizeSizeRevive:])
                averageSpeed = np.mean(self.speed[-historySizeSpeedRevive:])
                if averageSize>THavgSizeToRevive and averageSpeed>THavgSpeedToRevive:
                    return True
                else:
                    return False



    def drawCircleLastBall(self,image,radius=4,thickness=3):
        if self.ballAlive:
            if self.btype[-1]==Btype.REAL:
                cv.circle(image,(self.x[-1], self.y[-1]), radius, self.color, thickness)
            if self.btype[-1]==Btype.HAND:
                cv.circle(image, (self.x[-1], self.y[-1]), radius, (255,255,255), thickness)
            if self.btype[-1]==Btype.DUPLICATE:
                cv.circle(image, (self.x[-1], self.y[-1]), radius, (0, 0, 0), thickness)


    def __getitem__(self, key):
        if isinstance(key, slice):
          start, stop, step = key.indices(self.historySize)
          newBallHistory = BallHistory(self.historySize)
          newBallHistory.x = self.x[start:stop]
          newBallHistory.y = self.y[start:stop]
          newBallHistory.area = self.area[start:stop]
          return newBallHistory
        elif isinstance(key, int):
            return Ball(self.x[key],self.y[key],self.area[key],self.btype[key])



class Ball:
    def __init__(self,x,y,area,btype=Btype.REAL):
        self.x = int(x)
        self.y = int(y)
        self.area = area
        self.btype = btype

class History:
    def __init__(self,historySize,numOfBalls):
        colors=[(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
        self.numOfBalls=numOfBalls
        self.arr = [0] * numOfBalls
        for i in range(numOfBalls):
            self.arr[i] = BallHistory(historySize,i,colors[i])

    def insert(self,id,newBall,overrideBtype=Btype.NONE):
        if(id>=0 and id<self.numOfBalls):
            self.arr[id].append(newBall,overrideBtype)
        else:
            print("id is not in range")

    def insertAllBalls(self,ballsArr,overrideBtype=Btype.NONE): # not efficient, for startup only
        if len(ballsArr)!=self.numOfBalls:
            print("cannot inset array of ball - the dim does not fit")
        else:
            for i in range(self.numOfBalls):
                self.insert(i, ballsArr[i],overrideBtype)

    def insertByLst(self,lst,IDs,balls_list,img,backSub,useHand = True,maxDistanceToMatch=120):
        for i in range(len(IDs)):
            oldBallInd = IDs[int(lst[i][0])]
            newBallInd = int(lst[i][1])
            distance = lst[i][2]

            if distance != -1 and (not useHand or distance < maxDistanceToMatch):  #check max distance only when use hand (for alive balls only)
                self.insert(oldBallInd, balls_list[newBallInd], Btype.REAL)
                # cv.circle(copy_img, (balls_list[newBallInd].x,balls_list[newBallInd].y), 4, colors[oldBallInd], 3)
            else:  # ball cannot be found, look for hand (or duplicate the last one)
                if useHand:
                    newBall, handsBallDist = hands_detection(img, backSub, True, self.get(oldBallInd)[-1])
                    self.insert(oldBallInd, newBall)



    def get(self,id):
        return self.arr[id]


    def isNewBallAtMax(self):
        for i in range(self.numOfBalls):
            if self.arr[i].ballAlive and self.arr[i].yExtremom[-1]==Extremom.MAX:
                return True
        return False

    def predictNumOfBalls(self,historySizeNotReal=20,historySizeSpeedKill=20,historySizeSpeedRevive=20,historySizeSizeRevive=20,THavgNotRealKill=0.85,THavgSpeedToKill=10,THavgSpeedToRevive=10,THavgSizeToRevive=70):
        aliveIDs = []
        aliveBalls=[]

        deadIDs = []
        deadBalls = []

        for i in range(self.numOfBalls):

            alive = self.arr[i].isAlive(historySizeNotReal,historySizeSpeedKill,historySizeSpeedRevive,historySizeSizeRevive,THavgNotRealKill,THavgSpeedToKill,THavgSpeedToRevive,THavgSizeToRevive) #check alive for ball
            self.arr[i].ballAlive=alive  #update the ball alive
            if alive:
                aliveIDs.append(i)
                aliveBalls.append(self.arr[i][-1])
            else:
                deadIDs.append(i)
                deadBalls.append(self.arr[i][-1])






        return aliveBalls,aliveIDs,deadBalls,deadIDs,len(aliveIDs) #list of balls ids out of the game, how many balls should be in the game now

    def drawLastBalls(self,image,radius=4,thickness=3):
        for i in range(self.numOfBalls):
            self.arr[i].drawCircleLastBall(image,radius,thickness)

    def drawTrailsLastBalls(self,image,image_width,image_height,frameT,frameT_width,frameT_height):
        for i in range(self.numOfBalls):
            ballH = self.arr[i]
            if ballH.ballAlive:
                frame, chosenResized = overlayTrail(ballH.x[-1], ballH.y[-1],
                                            ballH.x[-2], ballH.y[-2], image, frameT, image_width,
                                            image_height, frameT_width, frameT_height, 900, 2, ballH.lastTrailResize, False,
                                            ballH.color)
                ballH.lastTrailResize = chosenResized


def hands_detection(img, back_obj, detect, ball, square_size_to_search = 80, Number_of_pixels = 1 ):

    #       function's input:
    #       img : frame
    #       back_obj: cv.createBackgroundSubtractorMOG2()..
    #       detect: if True: we are tring to detect a hand in the era of the ball
    #               if false: the ouput will be the filter
    #       ball: the ball from the past frame.
    #       square_size_to_search : the size of the square we will comduct our search on
    #       Number_of_pixels : the number of pixels that counts as hand

    lower_skin = np.array([0, 135, 85])
    upper_skin = np.array([255, 180, 135])
    fgmask = back_obj.apply(img)
    img_ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    fgmask[fgmask == 255] = 1
    mask_skin = cv.inRange(img_ycrcb, lower_skin, upper_skin)
    naive_mask = fgmask * mask_skin
    naive_mask = cv.dilate(src=naive_mask, kernel=(5, 5), iterations=10)

    if detect: # on detect mode:
        area_to_search = np.zeros((img.shape[0], img.shape[1]))
        x = ball.x
        y = ball.y
        area_to_search[y - int(square_size_to_search/2) :y + int(square_size_to_search/2), x - int(square_size_to_search/2):x + int(square_size_to_search/2)] = 1
        mask = naive_mask * area_to_search

        if np.count_nonzero(mask) > int(Number_of_pixels):  # There is skin in that area
            # print("we detected skin")
            mask = np.ma.masked_equal(mask, 0)
            row_cm = np.average(np.arange(mask.shape[0]), weights=np.sum(mask, axis=1))
            col_cm = np.average(np.arange(mask.shape[1]), weights=np.sum(mask, axis=0))
            com = (row_cm, col_cm)
            new_ball = Ball(x = com[1],y = com[0] , area = ball.area ,btype=Btype.HAND)
            distance_from_ball = np.sqrt( (com[1] - ball.x)**2  + (com[0] - ball.y)**2)

        else:  # There is no skin in that area
            new_ball = Ball(x = ball.x,y = ball.y, area = ball.area, btype = Btype.DUPLICATE)
            distance_from_ball = None
        return new_ball, distance_from_ball  # 1 is the relayebility - for now always 1.

    else: # no detect - just return mask
        return naive_mask