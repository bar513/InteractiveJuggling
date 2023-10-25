from OurClasses import BallHistory,History,Ball
import numpy as np
import itertools

theHistory = History(5,2)
theHistory.insert(0,Ball(0,0,1))
theHistory.insert(0,Ball(1,1,1))
theHistory.insert(0,Ball(2,2,1))

ball0H = theHistory.get(0)

print(ball0H[-1].x)
# print(np.mean(ball0H[0:3].x))



