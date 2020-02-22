import numpy as np
from scipy import interpolate

class Animation:

    def __init__(self):
        pass
    
    def init(self, trajectory, time, frequency):
        self.x = np.linspace(0, time, num=time*frequency)
        self.y = np.linspace(trajectory[0], trajectory[1], num=time*frequency)
        self.f = interpolate.interp1d(self.x, self.y)

    def callback(self, time):
        return self.f(time)

initialized = False
animation = Animation()
def linear(trajectory, time, frequency):
    global initialized
    global animation
    if initialized == False:
        animation.init(trajectory, time, frequency)
        initialized = True
    return animation.callback
