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
import math

def video_to_array(path):
    cap = cv.VideoCapture(path)
    frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    buf = np.empty((frameCount, 400, 640, 3), np.dtype('uint8'))

    fc = 0
    ret = True

    while (fc < frameCount  and ret):
        ret, frame = cap.read()
        buf[fc] = cv.resize(frame, (640, 400))
        fc += 1

    cap.release()
    return buf

def video_to_array(path):
    cap = cv.VideoCapture(path)
    frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    buf = np.empty((frameCount, 400, 640, 3), np.dtype('uint8'))

    fc = 0
    ret = True

    while (fc < frameCount  and ret):
        ret, frame = cap.read()
        buf[fc] = cv.resize(frame, (640, 400))
        fc += 1

    cap.release()
    return buf


def filter_with_stats(img, area_th=300):
    output = cv.connectedComponentsWithStats(img, 8, cv.CV_32S)
    (numLabels, labels, stats, centroids) = output
    for i in range(0, numLabels):
        x = stats[i, cv.CC_STAT_LEFT]
        y = stats[i, cv.CC_STAT_TOP]
        w = stats[i, cv.CC_STAT_WIDTH]
        h = stats[i, cv.CC_STAT_HEIGHT]
        area = stats[i, cv.CC_STAT_AREA]
        if area < area_th:
            labels[labels == i] = 0
    labels[labels != 0] = 255
    return labels.astype(np.uint8)


def ball_filter(img, back_object):
    lab = cv.cvtColor(img, cv.COLOR_RGB2LAB)
    fgMask = back_object.apply(lab[:, :, 1])
    th, b_th = cv.threshold(lab[:, :, 2], 90, 255, cv.THRESH_BINARY_INV) #100 #90 255
    th, a_th = cv.threshold(fgMask, 180, 255, cv.THRESH_BINARY) #180 255
    a_filter = filter_with_stats(a_th, 100) #200
    b_filter = filter_with_stats(b_th, 100) #200
    th_img = cv.bitwise_and(a_filter, b_filter)
    return th_img


def ball_detection(img, back_object):
    balls_lst = []
    th_img = ball_filter(img, back_object)
    contours, _ = cv.findContours(th_img.astype(np.uint8), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # list for storing names of shapes
    for contour in contours:
        # approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        #     # finding center point of shapes
        M = cv.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])

            #     # putting shape name at center of each shape
            # if len(approx)>12:
            #     cv.putText(img, 'circle', (x, y),cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            ball = Ball(x, y, cv.arcLength(contour, True))
            balls_lst.append(ball)
    return th_img, balls_lst, contours

def get_closest_point(ball_old,ball_new):
    old = np.array([(i.x,i.y) for i in ball_old])
    new = np.array([(j.x,j.y) for j in ball_new])
    D = dist.cdist(old,new)
    arr = np.column_stack((np.arange(len(old)),np.zeros((len(old),2))))
    if D.shape[0]>D.shape[1]:
        for dis in range(D.shape[1]):
            d = np.unravel_index(D.argmin(), D.shape)
            arr[d[0],1] = d[1]
            arr[d[0],2] = D[d]
            D[d[0]] = 999
            D[:,d[1]] = 999
    else:
        for dis in range(D.shape[0]):
            d = np.unravel_index(D.argmin(), D.shape)
            arr[d[0],1] = d[1]
            arr[d[0],2] = D[d]
            D[d[0]] = 999
            D[:,d[1]] = 999
    arr[(arr[:,2]==0),2]=-1
    return arr


def draw_label(img, text, pos, bg_color):
   font_face = cv.FONT_HERSHEY_SIMPLEX
   scale = 1
   color = (0, 0, 0)
   thickness = cv.FILLED
   margin = 2
   txt_size = cv.getTextSize(text, font_face, scale, thickness)

   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin

   cv.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
   cv.putText(img, text, pos, font_face, scale, color, 1, cv.LINE_AA)

   