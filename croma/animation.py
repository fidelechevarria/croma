import numpy as np
from scipy import interpolate

class Animation:

    def __init__(self, trajectory, time, method):
        self.x = np.array(time)
        self.y = np.array(trajectory).T
        self.f = interpolate.interp1d(self.x, self.y, kind=method)

    def callback(self, time):
        time = np.clip(time, self.x[0], self.x[-1])
        return self.f(time)

def animation(trajectory, time, method='linear'):
    animation = Animation(trajectory, time, method)
    return animation.callback, time[-1]
