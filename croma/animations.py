import numpy as np
from scipy import interpolate

class Animation:

    def __init__(self, trajectory, time, frequency):
        self.x = np.linspace(0, time, num=time*frequency)
        self.y = np.linspace(trajectory[0], trajectory[1], num=time*frequency).T
        self.f = interpolate.interp1d(self.x, self.y)
        print('interpolation created')

    def callback(self, time):
        return self.f(time)

def linear(trajectory, time, frequency):
    animation = Animation(trajectory, time, frequency)
    return animation.callback
