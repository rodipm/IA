import sys
import getopt
import json
import pickle
from utils import *

opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "ofile="])
inputfile = None
outputfile = None



for opt, arg in opts:
      if opt == '-h':
         print('main.py -i <inputQFile> -o <outputQFile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

if inputfile:
    with open(inputfile, 'rb') as file:
        Q = np.load(file)
    with open(inputfile + 'dict', 'r') as file:
        QIDic = json.load(file)
    with open(inputfile + 'state', 'r') as file:
        crclCentreX = int(file.readline())
        crclCentreY = int(file.readline())
        rctLeft = int(file.readline())
        rctTop = int(file.readline())
        rctWidth = int(file.readline())
        rctHeight = int(file.readline())

print(rctLeft,
      rctTop,
      rctWidth,
      rctHeight)
sys.exit()
FPS = 9999999999999999999999999999999999*999999999999999
fpsClock = pygame.time.Clock()

pygame.init()

window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Falling Ball - AI")

rct = pygame.Rect(rctLeft, rctTop, rctWidth, rctHeight)

action = 1 # 0 - stay, 1 - left, 2 - right

score = 0
missed = 0
reward = 0
font = pygame.font.Font(None, 30)

# learning rate
lr = 0.85
y = .99

i = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if outputfile:
                with open(outputfile, 'wb') as file:
                    np.save(file, Q)
                with open(outputfile + 'dict', 'w') as file:
                    file.write(json.dumps(QIDic))
                with open(outputfile + 'state', 'w') as file:
                    file.write(str(crclCentreX) + '\n')
                    file.write(str(crclCentreY) + '\n')

                    file.write(str(rctLeft) + '\n')
                    file.write(str(rctTop) + '\n')
                    file.write(str(rctWidth) + '\n')
                    file.write(str(rctHeight) + '\n')
            sys.exit()

    window.fill(BLACK)

    #trigger the reward calculations (ball hits or misses rect)
    if crclCentreY >= windowHeight - rctHeight - crclRadius:
        reward = calculate_score(rct, Circle(crclCentreX, crclCentreY))
        crclCentreX = circle_falling(crclRadius)    #random circle X position
        crclCentreY = 50
    else:
        reward = 0 #nothing happened
        crclCentreY += crclYStepFalling #falling ball

    # Q-LEARNING calculations
    s = State(rct, Circle(crclCentreX, crclCentreY)) #get current state
    print('Current State (s):', s)
    act = get_best_action(s)
    print('Actions (act): ', act)
    r0 = calculate_score(s.rect, s.circle)
    print('Reward: ', r0)
    s1 = new_state_after_action(s, act)
    print('Next State: ', s1)

    # update Q-Table
    Q[state_to_number(s), act] += lr * (r0 + y * np.max(Q[state_to_number(s1), :]) - Q[state_to_number(s), act])

    # update models
    rct = new_rect_after_action(s.rect, act)
    crclCentreX = s.circle.circleX
    crclCentreY = s.circle.circleY

    pygame.draw.circle(window, RED, (crclCentreX, crclCentreY), crclRadius)
    pygame.draw.rect(window, GREEN, rct)


    #update score
    if reward == 1:
        score += reward
    elif reward == -1:
        missed += reward

    # scores
    rate = 0
    if missed or score:
        rate = (missed*-1)/(missed*-1 + score)

    text = font.render('score: ' + str(score), True, (238, 58, 140))
    text1 = font.render('missed: ' + str(missed), True, (238, 58, 140))
    text2 = font.render('hit rate: ' + str(1 - rate), True, (0, 255, 0))
    text3 = font.render('miss rate: ' + str(rate), True, (255, 0, 0))

    window.blit(text, (windowWidth - 120, 10))
    window.blit(text1, (windowWidth - 280, 10))
    window.blit(text2, (0, 10))
    window.blit(text3, (0, 40))

    # update display
    pygame.display.update()
    fpsClock.tick(FPS)
