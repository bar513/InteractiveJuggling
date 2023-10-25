# first of all import the socket library
import socket
import numpy as np
import cv2 as cv

class JServer:
    def __init__(self):
        self.b_x = [0] * 4
        self.b_y = [0] * 4

        self.s = socket.socket()
        print("Socket successfully created")
        port = 12345
        self.s.bind(('', port))
        print("socket binded to %s" % (port))
        self.s.listen(5)
        print("socket is listening")
        self.c, self.addr = self.s.accept()
        print('Got connection from', self.addr)

    def sendData(self,frame,history,patternNum,score,combo,bonus,targetPosX,targetPosY,targetBonus,targetCounter,b_totalCounter,b_combo_counter):
        b_patternNum = int(patternNum).to_bytes(4, "little")

        b_totalCounter = int(b_totalCounter).to_bytes(4, "little")
        b_combo_counter = int(b_combo_counter).to_bytes(4, "little")

        b_score = int(score).to_bytes(4, "little")
        b_combo = int(combo).to_bytes(4, "little")
        b_bonus = int(bonus).to_bytes(4, "little")
        b_targetPosX = int(targetPosX).to_bytes(4, "little",signed=True)
        b_targetPosY = int(targetPosY).to_bytes(4, "little",signed=True)
        b_targetBonus = int(targetBonus).to_bytes(4, "little")
        b_targetCounter = int(targetCounter).to_bytes(4, "little")

        for i in range(len(self.b_x)):
            self.b_x[i] =  int(history.get(i)[-1].x).to_bytes(4, "little",signed=True) if history.get(i).ballAlive else int(-1).to_bytes(4, "little",signed=True)
            self.b_y[i] = int(history.get(i)[-1].y).to_bytes(4, "little", signed=True) if history.get(i).ballAlive else int(-1).to_bytes(4, "little", signed=True)




        ret, jpeg = cv.imencode('.jpg', frame)
        img = jpeg.tobytes()


        b_imgSize = int(len(img)).to_bytes(4, "little")

        self.c.send(b_patternNum+b_totalCounter+b_combo_counter+b_score+b_combo+b_bonus+b_targetPosX+b_targetPosY+b_targetBonus+b_targetCounter+
                    self.b_x[0] + self.b_y[0] +
                    self.b_x[1] + self.b_y[1] +
                    self.b_x[2] + self.b_y[2] +
                    self.b_x[3] + self.b_y[3] +
                    b_imgSize + img)

    def closeConnection(self):
        self.c.close()