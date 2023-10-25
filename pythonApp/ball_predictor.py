from filterpy.kalman import KalmanFilter
import numpy as np
import cv2


class BallPredictor:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=4, dim_z=2)
        # kf.F = np.array([[1, dt], [0, 1]])
        # Define the measurement matrix
        self.kf.x = np.array([0., 0., 0., 0.])
        self.kf.P = np.diag([100., 100., 10., 10.])
        dt = 0.05  # time of frame
        self.kf.F = np.array([[1., dt, 0., 0.], [0., 1., 0., 0.], [0., 0., 1., dt], [0., 0., 0., 1.]])
        self.kf.H = np.array([[1., 0., 0., 0.], [0., 0., 1., 0.]])
        self.kf.R = np.diag([0.5, 0.5])
        q = 0.1  # process noise standard deviation
        self.kf.Q = np.diag([20,999,20,999])

    def update(self,ball):
        self.kf.update(ball)

    def predict(self):
        self.kf.predict()
        self.update((self.kf.x[0],self.kf.x[2]))
        self.kf.predict()
        self.update((self.kf.x[0], self.kf.x[2]))
        self.kf.predict()
        self.update((self.kf.x[0], self.kf.x[2]))
        self.kf.predict()
        self.update((self.kf.x[0], self.kf.x[2]))
        self.kf.predict()
        return (self.kf.x[0],self.kf.x[2])

    def forget(self):
        self.__init__()

