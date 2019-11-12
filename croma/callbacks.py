import numpy as np

pos_dot = np.array([0.1, 0.1, 0.0])
pos = np.array([0., 0., 0.]) 
def centerCallback(dt):
    global pos
    global pos_dot
    pos = pos + pos_dot * dt
    return pos