import cv2 as cv
import numpy as np
import math
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result

def overlayTrail(x1,y1,x2,y2,frame,frameT,frame_width,frame_height,frameT_width,frameT_height,trailLength=900,scaleFactor=1,lastResizedFactor=0,overlay=False,color=(255,255,255)):
    # trail size is the actually trial length in pixels, not its image width or height
    #scaleFactor make the trail bigger or smaller. its size also depend on the distance between the points
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    midPosX = int((x1+x2)/2)
    midPosY = int((y1+y2)/2)
    angle = (math.atan2(y1-y2, x1-x2)*180)/math.pi

    resizeFactor = (distance / trailLength)*scaleFactor


    changeResizedFactor=2 #how much the trail can be changed between frames
    if lastResizedFactor!=0:
        if resizeFactor>lastResizedFactor*changeResizedFactor:
            resizeFactor=lastResizedFactor*changeResizedFactor
        elif resizeFactor < lastResizedFactor/changeResizedFactor:
            resizeFactor=lastResizedFactor/changeResizedFactor
    if resizeFactor<0.01:
        resizeFactor=0.01

    newWidth = int(frameT_width*resizeFactor)
    newHeight = int(frameT_height*resizeFactor)

    resized = cv.resize(frameT, (newWidth, newHeight), interpolation=cv.INTER_AREA)


    resized_rotated = rotate_image(resized,angle*(-1)+180)
    if (midPosX> newWidth/2 and midPosY>newHeight/2 and midPosX<frame_width-newWidth/2 and midPosY<frame_height-newHeight/2):
        left = midPosX - int(newWidth / 2)
        right = midPosX + int(newWidth / 2)
        up = midPosY + int(newHeight / 2)
        down = midPosY - int(newHeight / 2)

        if overlay:
            frame[down:up, left:right, :] = resized_rotated[:up-down,:right-left,:] + frame[down:up, left:right, :]
        else:
            x=resized_rotated[:up-down,:right-left,:]
            y=frame[down:up, left:right, :]

            # x[x[:,:,0]>50,0]=255
            # x[x<50]=y[x<50]

            blackThreshold=30
            if color[0]!=0:
                x[x[:,:,0]>blackThreshold,0]=color[0]
            if color[1]!=0:
                x[x[:,:,1]>blackThreshold,1]=color[1]
            if color[2]!=0:
                x[x[:,:,2]>blackThreshold,2]=color[2]
            x[x<blackThreshold]=y[x<blackThreshold]

            frame[down:up, left:right, :] = x

        # resized_rotated[:up-down,:right-left,:] = cv.bitwise_or(frame[down:up, left:right, :],resized_rotated[:up-down,:right-left,:])
        # frame[down:up, left:right, :] = resized_rotated[:up-down,:right-left,:]

    return frame,resizeFactor