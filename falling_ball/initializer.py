import numpy as np

windowWidth = 800
windowHeight = 400

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

crclCentreX = 400
crclCentreY = 50
crclRadius = 20

crclYStepFalling = windowHeight // 10

rctLeft = 400
rctTop = 350
rctWidth = 200
rctHeight = 50

QIDic = {}

Q = np.zeros([5000, 3])
