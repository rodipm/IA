import numpy as np
import sys
import pygame

size = 800, 800
width, height = size
num_squares = 20

num_squares = 10
square_size = width//num_squares

squares = [[0 for x in range(0, width, square_size)]
           for y in range(0, height, square_size)]


def Q_learning(initial_state):
    EPISODES = 2500
    LEARNING_RATE = 0.1
    DISCOUNT = 0.95

    SIZE = [width//num_squares, height//num_squares]
    NUMBER_OF_POSSIBLE_ACTIONS = 4  # up down left right

    epsilon = 1  # not a constant, qoing to be decayed
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = EPISODES//2
    epsilon_decay_value = epsilon / \
        (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    # q_table size =
    q_table = np.zeros(SIZE + [NUMBER_OF_POSSIBLE_ACTIONS])


    for episode in range(EPISODES):
        state = initial_state

        done = False

        while not done:

            if np.random.random() > epsilon:
                # Get action from Q table
                action = np.argmax(q_table[state])
            else:
                # Get random action
                action = np.random.randint(0, NUMBER_OF_POSSIBLE_ACTIONS)

            # get new states
            keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
            new_state = move_player_key(keys[action], state)
            reward = get_new_state_reward(new_state)
            done = is_goal_state(new_state)

            # If simulation did not end yet after last step - update Q table
            if not done:

                # Maximum possible Q value in next step (for new state)
                max_future_q = np.max(q_table[new_state])

                # Current Q value (for current state and performed action)
                current_q = q_table[state + (action,)]

                # And here's our equation for a new Q value for current state and action
                new_q = (1 - LEARNING_RATE) * current_q + \
                    LEARNING_RATE * (reward + DISCOUNT * max_future_q)

                # Update Q table with new Q value
                q_table[state + (action,)] = new_q

            # Simulation ended (for any reson) - if goal position is achived - update Q value with reward directly
            elif is_goal_state(new_state):
                q_table[state + (action,)] = 0

            state = new_state

        # Decaying is being done every episode if episode number is within decaying range
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value

    #done training
    #now out q_table is prepared to generate good moves
    actions = []

    found = False
    state = initial_state
    while not found:

        action = np.argmax(q_table[state])
        actions.append(action)

        keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
        new_state = move_player_key(keys[action], state)
        found = is_goal_state(new_state)
        state = new_state

    print("Done!", actions)


def get_new_state_reward(new_state):
    if is_goal_state(new_state):
        return 10
    else:
        return -1

def move_player_key(key, player_pos):
    x, y = player_pos
    if key == pygame.K_DOWN:
        y = y + 1
    if key == pygame.K_UP:
        y = y - 1
    if key == pygame.K_RIGHT:
        x = x + 1
    if key == pygame.K_LEFT:
        x = x - 1

    # check if it is a possible move
    moves = [pos for pos, action in get_possible_moves(player_pos)]
    if (x, y) in moves:
        return (x, y)
    return player_pos

def is_goal_state(player_pos):
    return player_pos == (5, 5)


def get_possible_moves(current_pos):
    possible_moves = []

    x, y = current_pos
    max_x, max_y = width//square_size, height//square_size

    # check UP, RIGHT, DOWN, LEFT
    if y - 1 >= 0 and squares[x][y-1] != "wall":
        possible_moves.append(((x, y-1), pygame.K_UP))
    if y + 1 < max_y and squares[x][y+1] != "wall":
        possible_moves.append(((x, y+1), pygame.K_DOWN))
    if x - 1 >= 0 and squares[x-1][y] != "wall":
        possible_moves.append(((x-1, y), pygame.K_LEFT))
    if x + 1 < max_x and squares[x+1][y] != "wall":
        possible_moves.append(((x+1, y), pygame.K_RIGHT))

    return possible_moves

Q_learning((0, 0))
