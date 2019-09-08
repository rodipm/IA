import random
import pygame
from initializer import *
from classes import *

def new_state_after_action(s, act):
    rct = None

    if act == 2:
        if s.rect.right + s.rect.width > windowWidth:
            rct = s.rect
        else:
            rct = pygame.Rect(s.rect.left + s.rect.width, s.rect.top, s.rect.width, s.rect.height)
    elif act == 1:
        if s.rect.left - s.rect.width < 0:
            rct = s.rect
        else:
            rct = pygame.Rect(s.rect.left - s.rect.width, s.rect.top, s.rect.width, s.rect.height)
    else:
        rct = s.rect

    newCircle = Circle(s.circle.circleX, s.circle.circleY + crclYStepFalling)

    return State(rct, newCircle)

def new_rect_after_action(rect, act):
    if act == 2:
        if rect.right + rect.width > windowWidth:
            return rect
        else:
            return pygame.Rect(rect.left + rect.width, rect.top, rect.width, rect.height)
    elif act == 1:
        if rect.left - rect.width < 0:
            return rect
        else:
            return pygame.Rect(rect.left - rect.width, rect.top, rect.width, rect.height)
    else:
        return rect

def circle_falling(crclradius):
    newx = 100 - crclRadius
    multiplier = random.randint(1, 8)
    newx *= multiplier
    return newx

def calculate_score(rect, circle):
    if rect.left <= circle.circleX <= rect.right:
        return 1
    else:
        return -1

def state_to_number(s):
    r = s.rect.left
    c = s.circle.circleY
    n = int(str(r) + str(c) + str(s.circle.circleX))

    if n in QIDic:
        return QIDic[n]
    else:
        if len(QIDic):
            maximum = max(QIDic, key=QIDic.get)
            QIDic[n] = QIDic[maximum] + 1
        else:
            QIDic[n] = 0
    return QIDic[n]

def get_best_action(s):
    return np.argmax(Q[state_to_number(s), :])
