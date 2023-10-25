

from enum import IntEnum
import numpy as np
from OurClasses import Extremom, Direction
class Pattern(IntEnum):
    UNKNOWN = 0
    ONE_BALL_ONE_HAND = 1
    ONE_BALL_TWO_HANDS = 2
    TWO_BALLS_ONE_HAND = 3
    TWO_BALLS_TWO_HANDS = 4
    THREE_BALLS_CACADE = 5
    THREE_BALLS_CACADE_WIDE = 6
    THREE_BALLS_FOUNTAIN = 7
    THREE_BALLS_ONE_ABOVE = 8
    THREE_BALLS_ONE_ELEVATOR = 9
    FOUR_BALLS_ASYNC = 10
    FOUR_BALLS_SYNC = 11


class PatternManager():
    def __init__(self,minChangeTime=30):
        self.patternHistory=np.array([],dtype=int)
        self.numBallsHistory = np.array([],dtype=int)
        self.numOfCandidates = np.array([],dtype=int)
        self.lastPattern = Pattern.UNKNOWN
        self.changeCounter=0
        self.minChangeTime = minChangeTime
        return

    def getPattern(self,history,numOfBalls,numOfCandidates):
        pattern = self.pattern_recognition(history, numOfBalls)
        self.patternHistory = np.append(self.patternHistory,int(pattern))
        self.numBallsHistory = np.append(self.numBallsHistory, int(numOfBalls))
        self.numOfCandidates = np.append(self.numOfCandidates, int(numOfCandidates))
        self.changeCounter += 1


        if(len(self.patternHistory) >100):
            self.patternHistory = self.patternHistory[1:]
            self.numBallsHistory = self.numBallsHistory[1:]

        if(self.changeCounter<self.minChangeTime):
            return self.changeCounter,1, self.lastPattern

        if len(self.patternHistory) < 30:
            return self.changeCounter,0, self.lastPattern

        B_mostFrequent, B_howFrequent = self.frequentCheck(self.numBallsHistory, 20)
        P_mostFrequent, P_howFrequent = self.frequentCheck(self.patternHistory, 25)

        if B_howFrequent < 0.9: #if balls not stable, stay with same pattern
            return self.changeCounter,0, self.lastPattern
        else:
            if(P_howFrequent > 0.9):
                if(self.lastPattern != P_mostFrequent):
                    self.lastPattern =P_mostFrequent
                    self.changeCounter=0
                return self.changeCounter,1, P_mostFrequent
            else:
                return self.changeCounter,0, self.lastPattern

    def frequentCheck(self,arr,historySize):
        counts = np.bincount(arr[-historySize:])
        mostFrequent = np.argmax(counts)
        howFrequent = counts[mostFrequent]/historySize
        return (mostFrequent,howFrequent)



    def pattern_recognition(self,history,numOfBAlls):

        meanXvar= np.mean([ballH.xVar[-1] for ballH in history.arr if ballH.ballAlive])
        meanYvar = np.mean([ballH.yVar[-1] for ballH in history.arr if ballH.ballAlive])
        yDx_var = meanYvar / meanXvar
        # kernel = np.array([0.0331,	0.0465,	0.0616,	0.0765,	0.0894,	0.0982,	0.1013,	0.0982,	0.0894,	0.0765,	0.0616,	0.0465,	0.0331])*10
        kernel = np.array([1,1,1,1,1]).astype(float)
        yExtremomHistory = [(np.array(ballH.yExtremom[-40:])==Extremom.MAX).astype(float) for ballH in history.arr if ballH.ballAlive]
        sumGaussians=np.array([0.0]*40)
        for h in yExtremomHistory:
            sumGaussians+=np.convolve(kernel, h, mode='same')


        meanGaussians = sumGaussians/len(yExtremomHistory) if len(yExtremomHistory)>0 else sumGaussians

        # sync = np.max(meanGaussians)
        syncMean = np.mean(meanGaussians[np.argpartition(meanGaussians, -3)[-3:]])
        sync =  syncMean > 0.7

        yExtremomDirHistory = [np.array(ballH.yExtremomDir[-40:])[np.array(ballH.yExtremom[-40:]) == Extremom.MAX] for ballH in history.arr if ballH.ballAlive]
        # sameDirection = np.mean(yExtremomDirHistory==Direction.RIGHT) > 0.9 or np.mean(yExtremomDirHistory==Direction.RIGHT) < 0.1

        sameDirectionMean = np.mean([np.sum(hist==Direction.RIGHT)/len(hist) for hist in yExtremomDirHistory if len(hist)>0])
        sameDirection = sameDirectionMean > 0.8
        # print(numOfBAlls," ",sameDirection)




        if numOfBAlls == 0:
             return Pattern.UNKNOWN

        elif numOfBAlls == 1:
            if yDx_var > 20:
                return Pattern.ONE_BALL_ONE_HAND
            return Pattern.ONE_BALL_TWO_HANDS

        elif numOfBAlls == 2:
            xVars = np.var([ np.mean(ballH.x[-20:]) for ballH in history.arr if ballH.ballAlive])
            if xVars==0:
                return Pattern.TWO_BALLS_ONE_HAND
            if meanYvar/xVars< 50:
                return Pattern.TWO_BALLS_TWO_HANDS
            return Pattern.TWO_BALLS_ONE_HAND

        elif numOfBAlls == 3:
            # if(np.sum([len(hist) for hist in yExtremomDirHistory if len(hist)>0])) > 8:
            #     print("dfs")
            # print(np.sum([len(hist) for hist in yExtremomDirHistory if len(hist)>0]))
            if yDx_var > 40: #and sync
                    return Pattern.THREE_BALLS_ONE_ELEVATOR
            else:
                if sameDirection:
                    return Pattern.THREE_BALLS_FOUNTAIN
                if yDx_var > 0.8:
                    return Pattern.THREE_BALLS_CACADE

                return Pattern.THREE_BALLS_CACADE_WIDE

        elif numOfBAlls == 4:  # (N==4)
            if sync:
                return Pattern.FOUR_BALLS_SYNC
            else:
                return Pattern.FOUR_BALLS_ASYNC


