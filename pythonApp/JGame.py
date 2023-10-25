import numpy as np

import PatternManager


class JGame:
    def __init__(self,scorePer1=1,comboScore=25,ComboLen=20,miniGameHitScore=500):
        self.scorePer1 = scorePer1
        self.score=0
        self.comboCounter=0
        self.totalCounter=0
        self.comboScore = comboScore
        self.comboLen =ComboLen
        self.isCombo=False
        self.currentComboScore=0
        self.currentPattern=PatternManager.Pattern.UNKNOWN

        self.miniGameScore = 0
        self.miniGameCounter = 0
        self.scorePerMiniGameHit = miniGameHitScore
        self.MG_x = -1
        self.MG_y = -1
        self.MG_rad = -1
        self.MG_isOn = False


    def add1ToCounter(self):
        if self.currentPattern==0:
            return

        self.totalCounter += 1
        self.comboCounter += 1
        self.isCombo = self.comboCounter %self.comboLen == 0 and self.comboCounter!= 0
        if(self.isCombo):
            self.currentComboScore =int(self.comboScore * (self.comboCounter/self.comboLen))
            self.score+= self.currentComboScore
        self.score+=self.scorePer1

    def updatePattern(self,pattern):
        self.currentPattern = pattern
        self.resetComboCounter()


    def resetComboCounter(self):
        self.comboCounter=0

    def resetCounter(self):
        self.totalCounter=0
        self.resetComboCounter()

    def getComboScore(self):
        if self.isCombo:
            # print(int(self.comboScore * (self.comboCounter/ self.comboLen)))
            return self.currentComboScore
        else:
            return 0


    def startMinGame(self):
        if not self.MG_isOn:
            self.miniGameScore=0
            self.miniGameCounter=0
            self.generateTarget()
            self.MG_isOn = True

    def getTarget(self):
        if(self.MG_isOn):
            return self.MG_x, self.MG_y, self.MG_rad
        return -1,-1,-1

    def generateTarget(self):
        self.MG_y = int(30 + 100 * np.random.random())
        self.MG_x = int(150 + 300 * np.random.random())
        self.MG_rad =  int(5 + 20 * np.random.random())

    def checkCollusion(self,balls):
        for ball in balls:
            if np.sqrt((self.MG_x - ball.x)**2 +(self.MG_y - ball.y)**2) < self.MG_rad:
                self.miniGameScore+=self.scorePerMiniGameHit
                self.miniGameCounter+=1
                self.generateTarget()
                return True
        return False

    def quitGame(self):
        self.miniGameScore = 0
        self.miniGameCounter=0
        self.MG_isOn = False
        self.MG_y = -1
        self.MG_x = -1
        self.MG_rad = -1