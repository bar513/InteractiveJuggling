import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
from enum import Enum
import math

class Pattern(Enum):
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


class GameManager:
    def __init__(self,maximum_number_of_balls = 4,
                 refresh_rate = 10,
                 minmax_y_diff_batch = 3):

        self.minmax_y_diff_batch = minmax_y_diff_batch
        self.refresh_rate = refresh_rate
        self.maximum_number_of_balls = maximum_number_of_balls

        self.count = 0
        self.points = 0
        self.frame = 0
        self.number_of_balls = 0
        self.history_number_of_balls = []
        self.maximoms = [[] for i in range(self.maximum_number_of_balls)]
        self.minimoms = [[] for i in range(self.maximum_number_of_balls)]
        self.frequency = [None for i in range(self.maximum_number_of_balls)]
        self.juggs = [False for i in range(self.maximum_number_of_balls)]
        self.der = [[] for i in range(self.maximum_number_of_balls)]
        self.T = [[] for i in range(self.maximum_number_of_balls)]
        self.max_frame_distance = [[] for i in range(self.maximum_number_of_balls)]
        self.frames_of_maxs = []
        self.directions_of_maxs = []
        self.directions_of_mins = []
        self.ball_type = []
        self.new_min = False
        self.wh_oneball = None
        self.var_x = [[] for i in range(self.maximum_number_of_balls)]
        self.mean_var_x = None

        self.pattern = Pattern.UNKNOWN
        self.patterns = [Pattern.UNKNOWN]

        # gathering data for understanding drill
        self.minmin_x_diff = [[] for i in range(self.maximum_number_of_balls)]
        self.minmax_y_diff = [[] for i in range(self.maximum_number_of_balls)]
        self.maxs_frames = [None for i in range(self.maximum_number_of_balls)]

    def update_features(self,frame_number):
        self.count += 1
        self.frame = frame_number
        self.update_minmax()        # updates the min and max arrays
        self.update_juggs()         # updates the balls array
        self.update_count()         # updates the number of balls
        self.variance_x()


        # update number of balls
        self.history_number_of_balls.append(sum(self.juggs))
        self.update_number_of_balls()

        # update features
        self.update_minmax_y_diff()
        self.update_minmin_x_diff()
        self.update_der()

    def check_pattern(self,numOfBAlls):
        mean_width, mean_hight, mean_der, mean_T = self.get_mean_values()
        w, h, d, T, one_ball_hight_diff, N, maxs_together, maxs_same_direction, mins_same_direction, min_hand_type,alternate_mins_direction = self.pre_process_pattern_recognition(
            mean_width=mean_width, mean_hight=mean_hight, mean_der=mean_der, mean_T=mean_T)
        return self.pattern_recognition(w, h, d, T, one_ball_hight_diff, numOfBAlls, maxs_together, maxs_same_direction,mins_same_direction,min_hand_type,alternate_mins_direction)
    def update_minmax(self):
        for id in range(self.maximum_number_of_balls):
            if historyReal.arr[id].yExtremom[-1]== Extremom.MAX:
                # getting the location of the last max
                location = historyReal.arr[id].y.index(historyReal.arr[id].y[-1])
                self.frames_of_maxs.append(self.frame)
                self.directions_of_maxs.append(historyReal.get(id).xDirection[-1])
                self.maximoms[id].append((location,historyReal.arr[id].x[-1],historyReal.arr[id].y[-1],self.frame))
                if len(self.maximoms[id])>1:
                    self.T[id].append(np.abs(self.maximoms[id][-1][0] - self.maximoms[id][-2][0]))
                    if len(self.T[id])>1:
                        self.frequency[id] = np.mean(self.T[id])
            if historyReal.arr[id].yExtremom[-1] == Extremom.MIN:
                location = historyReal.arr[id].y.index(historyReal.arr[id].y[-1])
                self.directions_of_mins.append(historyReal.get(id).xDirection[-1])
                self.minimoms[id].append((location,historyReal.arr[id].x[-1],historyReal.arr[id].y[-1],self.frame))
                self.ball_type.append(historyReal.arr[id].btype[-1])
                # self.new_min = True
    def update_juggs(self):
        for id in range(self.maximum_number_of_balls):
            self.juggs[id] = historyReal.get(id).ballAlive
    def update_count(self):
        for id in range(self.maximum_number_of_balls):
            if self.juggs[id] and historyReal.arr[id].yExtremom[-1]== Extremom.MAX:
                self.count += 1
    def update_number_of_balls(self,num_of_balls_batch = 10):
        if len(self.history_number_of_balls) > num_of_balls_batch:
            self.number_of_balls = np.round(np.mean(self.history_number_of_balls[-num_of_balls_batch:]))
        else:
            self.number_of_balls = np.round(np.mean(self.history_number_of_balls))
    def update_minmin_x_diff(self):
        for id in range(self.maximum_number_of_balls):
            if self.juggs and len(self.maximoms[id])>1 and len(self.minimoms[id])>1 :
                diff = np.abs(self.minimoms[id][-1][1] - self.minimoms[id][-2][1])
                self.minmin_x_diff[id].append(diff)
                # self.new_min = False
    def update_minmax_y_diff(self):
        batch = self.minmax_y_diff_batch
        for id in range(self.maximum_number_of_balls):
            if self.juggs and len(self.maximoms[id])>1 and len(self.minimoms[id])>1:
                diff = np.abs(self.maximoms[id][-1][2] - self.minimoms[id][-1][2])
                if len(self.minmax_y_diff[id])==0:
                    self.minmax_y_diff[id].append(diff)
                elif diff != self.minmax_y_diff[id][-1]:
                    self.minmax_y_diff[id].append(diff)
    def update_der(self):
        for id in range(self.maximum_number_of_balls):
            if self.juggs[id] and len(self.maximoms[id])>1:
                y1 = self.maximoms[id][-1][2]
                x1 = self.maximoms[id][-1][1]
                location = self.maximoms[id][-1][0]
                y2 = historyReal.arr[id].y[location-5]
                x2 = historyReal.arr[id].x[location-5]
                if x1!=x2:
                    der = (y1-y2)/(x1-x2)
                else:
                    der = 100
                if len(self.der[id])==0:
                    self.der[id].append(der)
                elif self.der[id][-1] != der:
                    self.der[id].append(der)
    def variance_x(self):
        for id in range(self.maximum_number_of_balls):
            if self.juggs[id] and len(historyReal.get(id).x)>30:
                self.var_x[id] = np.var(historyReal.get(id).x[-30:])
            elif self.juggs[id]:
                self.var_x[id] = np.var(historyReal.get(id).x)
        self.mean_var_x = np.mean([self.var_x[id] for id in range(len(self.juggs)) if self.juggs[id]])


    def check_for_almost_same_maxs_frame(self,look_back = 10, threshold = 2):
        # check how much values are the same
        cur_frames = self.frames_of_maxs[-look_back:]
        for i in range(len(cur_frames)):
            if len(cur_frames) > i+1:
                if cur_frames[-i-1] - cur_frames[-i-2] < threshold:
                    return True
        return False
    def check_for_almost_same_maxs_direction(self,look_back = 10, threshold = 7):
        # check how much values are the same
        if len(self.directions_of_maxs) > look_back:
            NUM_SAME = np.sum(np.array(self.directions_of_maxs[-look_back:]) == Bdirection.RIGHT)
            print(self.directions_of_maxs[-look_back:])
            if NUM_SAME >= threshold or look_back- NUM_SAME >= threshold:
                return True
        return False
    def check_for_almost_same_mins_direction(self,look_back = 10, threshold = 7):
        # check how much values are the same
        if len(self.directions_of_mins) > look_back:
            NUM_SAME = np.sum(np.array(self.directions_of_mins[-look_back:]) == Bdirection.RIGHT)
            if NUM_SAME >= threshold or look_back- NUM_SAME >= threshold:
                return True
        return False
    def check_for_min_ball_type(self,look_back = 10, threshold = 7):
        bool_list = []
        if len(self.ball_type) < look_back:
            return False
        else:
            for ball_type in self.ball_type[-look_back:]:
                if isinstance(ball_type,type(Btype.HAND)):
                    bool_list.append(True)
                else:
                    bool_list.append(False)
            if np.sum(bool_list) > threshold:
                return True
            else:
                return False
    def check_for_altenate_mins_direction(self,look_back = 10, threshold = 8):
        # check how much values are the same
        count = 0
        if len(self.directions_of_mins) > look_back+1:
            # print("%%%%%%%%%%%%%%%%%%%%%%%%")
            for dir_indx in range(look_back):
                current_dir = self.directions_of_mins[-dir_indx-1]
                # print("current_dir: ",current_dir)
                if current_dir == Bdirection.RIGHT:
                    if self.directions_of_mins[-dir_indx-1] == Bdirection.LEFT:
                        # print('alternated!@@@@@@@@@@@')
                        count += 1
                elif current_dir == Bdirection.LEFT:
                    if self.directions_of_mins[-dir_indx-1] == Bdirection.RIGHT:
                        # print('alternated!@@@@@@@@@@@@@@')
                        count += 1
        return count >= threshold
    def get_mean_values(self, num_of_values_for_mean = 5):
        mean_width = np.zeros(self.maximum_number_of_balls)
        mean_hight = np.zeros(self.maximum_number_of_balls)
        mean_der = np.zeros(self.maximum_number_of_balls)
        mean_T = np.zeros(self.maximum_number_of_balls)
        for id in range(self.maximum_number_of_balls):
            if len(self.minmin_x_diff[id])<num_of_values_for_mean:
                mean_width[id] = np.mean(self.minmin_x_diff[id])
            else:
                mean_width[id] = np.mean(self.minmin_x_diff[id][-num_of_values_for_mean:])

            if len(self.minmax_y_diff[id])<num_of_values_for_mean:
                mean_hight[id] = np.mean(self.minmax_y_diff[id])
            else:
                mean_hight[id] = np.mean(self.minmax_y_diff[id][-num_of_values_for_mean:])

            if len(self.der[id])<num_of_values_for_mean:
                mean_der[id] = np.mean(self.der[id])
            else:
                mean_der[id] = np.mean(self.der[id][-num_of_values_for_mean:])

            if len(self.T[id])<num_of_values_for_mean:
                mean_T[id] = np.mean(self.T[id])
            else:
                mean_T[id] = np.mean(self.T[id][-num_of_values_for_mean:])

        return mean_width, mean_hight, mean_der, mean_T
    def pre_process_pattern_recognition(self,mean_width, mean_hight ,mean_der , mean_T):
        w = np.mean([val for val in mean_width if not math.isnan(val)])

        h = np.mean([val for val in mean_hight if not math.isnan(val)])
        d = np.mean([np.abs(val) for val in mean_der if not math.isnan(val)])
        T = np.mean([val for val in mean_T if not math.isnan(val)])
        one_ball_hight_diff = [0 for i in range(self.maximum_number_of_balls)]
        N = self.number_of_balls
        maxs_together = self.check_for_almost_same_maxs_frame(look_back = 4, threshold = 3)
        maxs_same_direction = self.check_for_almost_same_maxs_direction(look_back = 5, threshold = 5)
        mins_same_direction = self.check_for_almost_same_mins_direction(look_back = 5, threshold = 5)
        mins_hand_type = self.check_for_min_ball_type(look_back = 8, threshold = 4)
        alternate_mins_direction = self.check_for_altenate_mins_direction(look_back = 9, threshold = 7)
        return w,h,d,T,one_ball_hight_diff,N,maxs_together,maxs_same_direction,mins_same_direction,mins_hand_type,alternate_mins_direction
    def pattern_recognition(self,w,h,d,T,one_ball_hight_diff,N,maxs_together,maxs_same_direction,mins_same_direction,mins_hand_type,alternate_mins_direction):
        cur_pattern = self.pattern
        print("num of balls:   ",N)
        if N == 0:
            cur_pattern = self.pattern
        elif N==1:
            if self.mean_var_x < 1000:
                cur_pattern = Pattern.ONE_BALL_ONE_HAND
            elif self.mean_var_x>= 1000:
                cur_pattern = Pattern.ONE_BALL_TWO_HANDS
            else:
                cur_pattern = self.pattern
        elif N==2:
            print(self.mean_var_x)
            if maxs_together:
                cur_pattern = Pattern.TWO_BALLS_TWO_HANDS
            else:
                cur_pattern = Pattern.TWO_BALLS_ONE_HAND
        elif N==3:
            print(self.mean_var_x)
            if self.mean_var_x < 1500:
                if maxs_together:
                    cur_pattern = Pattern.THREE_BALLS_ONE_ELEVATOR
            else:
                if maxs_same_direction or mins_same_direction:
                    cur_pattern = Pattern.THREE_BALLS_FOUNTAIN
                else:
                    if self.mean_var_x < 3500:
                        cur_pattern = Pattern.THREE_BALLS_CACADE
                    else:
                        cur_pattern = Pattern.THREE_BALLS_CACADE_WIDE
        elif N==4: #(N==4)
            if maxs_together:
                cur_pattern = Pattern.FOUR_BALLS_SYNC
            else:
                cur_pattern = Pattern.FOUR_BALLS_ASYNC
        else:
            cur_pattern = Pattern.UNKNOWN
        self.patterns.append(cur_pattern)
        if len(self.patterns) < 30:
            self.pattern = max(set(self.patterns), key=self.patterns.count)

        else:
            self.pattern = max(set(self.patterns[-30:]), key=self.patterns[-30:].count)


