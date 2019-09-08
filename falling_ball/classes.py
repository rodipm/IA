class Circle:
    def __init__(self, circleX, circleY):
        self.circleX = circleX
        self.circleY = circleY

class State:
    def __init__(self, rect, circle):
        self.rect = rect
        self.circle = circle
