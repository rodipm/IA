import sys
import pygame
import random
import numpy as np
import heapq

pygame.init()

width = height = 800
menu_height = 100
size = width, height  + menu_height

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze - AI PLay")

black = (0, 0, 0)
white = (100, 100, 100)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 200)
yellow = (255, 255, 0)
orange = (255, 127, 80)
brown = (84, 1, 15)

font = pygame.font.Font(None, 30)


num_squares = 20
square_size = width//num_squares
squares = [[0 for x in range(0, width, square_size)]
           for y in range(0, height, square_size)]

saved_squares = squares

player_pos = (0, 0)
goal_pos = (-1, -1)

b_pos = (-1, -1)
d_pos = (-1, -1)
aStar_pos = (-1, -1)
q_pos = (-1, -1)

positions_d = []
positions_b = []
positions_aStar = []
positions_q = []

algs = []

tick_counter = 0
started = False


def Q_learning(initial_state):
    EPISODES = 5000
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
            action_key = keys[action]
            new_state = move_player_key(action_key, state)
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

        keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
        action_key = keys[action]
        actions.append(action_key)

        new_state = move_player_key(action_key, state)
        found = is_goal_state(new_state)
        state = new_state
    print("Q-Learning Done!")
    return actions

def manhattan_distance(player_pos, goal_pos):
    return abs(player_pos[0] - goal_pos[0]) + abs(player_pos[1] - goal_pos[1])

def get_new_state_reward(new_state):
    if is_goal_state(new_state):
        return 10
    else:
        return -1


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


def get_possible_moves_with_costs(current_pos):
    possible_moves = get_possible_moves(current_pos)
    costs = []
    for next_state, _ in possible_moves:
        if is_goal_state(next_state):
            costs.append(10)
        else:
            costs.append(1)
    
    possible_moves_costs = []
    for i, move in enumerate(possible_moves):
        possible_moves_costs.append(move + (costs[i], ))

    return possible_moves_costs

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


def move_player_to(new_pos):
    global player_pos
    if new_pos in get_possible_moves(player_pos):
        player_pos = new_pos


class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0, item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


def depth_first_search(startState):

    if is_goal_state(startState):
        return []

    visitedStates, stack = [], Stack()

    stack.push((startState, []))  # (estado, acoes)

    while not stack.isEmpty():
        currentState, actions = stack.pop()

        if currentState not in visitedStates:
            visitedStates.append(currentState)

            if squares[currentState[0]][currentState[1]] == "goal":
                return actions

            successors = get_possible_moves(currentState)
            for nextState, action in successors:
                newActions = actions + [action]
                stack.push((nextState, newActions))


def bredth_first_search(startState):
    if is_goal_state(startState):
        return []

    visitedStates, queue = [], Queue()

    queue.push((startState, []))  # (estado, acoes)

    while not queue.isEmpty():
        currentState, actions = queue.pop()

        if currentState not in visitedStates:
            visitedStates.append(currentState)

            if is_goal_state(currentState):
                return actions

            successors = get_possible_moves(currentState)
            for nextState, action in successors:
                newActions = actions + [action]
                queue.push((nextState, newActions))


def a_star_search(startState):

    if is_goal_state(startState):
        return []

    visitedStates, queue = [], PriorityQueue()

    queue.push((startState, [], 0), 0)

    while not queue.isEmpty():
      currentState, actions, currentCost = queue.pop()

      if currentState not in visitedStates:
        visitedStates.append(currentState)

        if is_goal_state(currentState):
          return actions

        successors = get_possible_moves_with_costs(currentState)
        for next_state, action, cost in successors:
          new_actions = actions + [action]
          new_cost = currentCost + cost
          heuristic_cost = new_cost + manhattan_distance(next_state, goal_pos) #heuristic(nextState, problem)
          queue.push((next_state, new_actions, new_cost), heuristic_cost)

def restart_game():
    global tick_counter, started, algs, d_pos, b_pos, aStar_pos, q_pos, squares, saved_squares, positions_b, positions_d, positions_q, positions_aStar
    tick_counter = 0
    started = False
    algs = []
    d_pos = (-1, -1)
    b_pos = (-1, -1)
    aStar_pos = (-1, -1)
    q_pos = (-1, -1)
    squares = saved_squares
    positions_b = []
    positions_d = []
    positions_aStar = []
    positions_q = []


def restart_all():
    global tick_counter, started, algs, d_pos, b_pos, q_pos, squares, saved_squares, player_pos, positions_b, positions_d, positions_q, positions_aStar
    tick_counter = 0
    started = False
    algs = []
    d_pos = (-1, -1)
    b_pos = (-1, -1)
    aStar_pos = (-1, -1)
    q_pos = (-1, -1)
    player_pos = 0, 0
    positions_b = []
    positions_d = []
    positions_aStar = []
    positions_q = []
    squares = [[0 for x in range(0, width, square_size)] for y in range(0, height, square_size)]



def exec_movements(positions_d, positions_b, positions_aStar, positions_q, d_pos, b_pos, aStar_pos, q_pos):
    global tick_counter
    pygame.time.wait(500)

    if tick_counter >= len(positions_d) and tick_counter >= len(positions_b) and tick_counter >= len(positions_q) and tick_counter >= len(positions_aStar):
        return False, d_pos, b_pos, aStar_pos, q_pos

    if tick_counter < len(positions_d):
        d_pos = move_player_key(positions_d[tick_counter], d_pos)
    if tick_counter < len(positions_b):
        b_pos = move_player_key(positions_b[tick_counter], b_pos)
    if tick_counter < len(positions_aStar):
        aStar_pos = move_player_key(positions_aStar[tick_counter], aStar_pos)
    if tick_counter < len(positions_q):
        q_pos = move_player_key(positions_q[tick_counter], q_pos)
    tick_counter = tick_counter + 1
    return True, d_pos, b_pos, aStar_pos, q_pos


def init_game(player_pos, algs):
    global started, saved_squares, d_pos, b_pos, q_pos, aStar_pos
    started = True
    saved_squares = squares
    if "d" in algs:
        d_pos = player_pos
    if "b" in algs:
        b_pos = player_pos
    if "q" in algs:
        q_pos = player_pos
    if "aStar" in algs:
        aStar_pos = player_pos

def is_goal_state(player_pos):
    return squares[player_pos[0]][player_pos[1]] == "goal"


def get_frontier_cells(grid, position):
    x, y = position
    max_x = len(grid)
    max_y = len(grid[0])

    possible_moves = []

    if x - 1 > -1:
        possible_moves.append((x-1, y))
    if x + 1 < max_x:
        possible_moves.append((x+1, y))
    if y - 1 > -1:
        possible_moves.append((x, y-1))
    if y + 1 < max_y:
        possible_moves.append((x, y+1))

    return possible_moves


# generate maze function
def generate_maze(grid, start):

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y] = "wall"

    path = set()
    visited_blocks = set()

    start_x, start_y = start
    grid[start_x][start_y] = 0
    path.add(start)

    while len(path):
        # for i in range(100):
        cell = random.choice(list(path))
        visited_blocks.add(cell)
        path.remove(cell)
        neighbors = []

        # get frontier cells
        for fc in get_frontier_cells(grid, cell):
            x, y = fc
            if fc not in visited_blocks and grid[x][y] == "wall":
                neighbors.append(fc)

        if(len(neighbors)):
            random_neighbor = random.choice(neighbors)
            neighbors.remove(random_neighbor)

            x, y = random_neighbor
            grid[x][y] = 0
            path.add(random_neighbor)
            # visited_blocks.add(random_neighbor)

        for n in neighbors:
            path.add(n)

    return grid


drag_draw = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x, y = pos[0]//square_size, pos[1]//square_size
            if event.button == 3:
                squares[x][y] = "goal"
                goal_pos = (x, y)
            elif squares[x][y] == "wall":
                squares[x][y] = 0
            else:
                squares[x][y] = "wall"

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            positions_b = bredth_first_search(player_pos)
            algs.append("b")
            init_game(player_pos, algs)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            positions_d = depth_first_search(player_pos)
            algs.append("d")
            init_game(player_pos, algs)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            positions_aStar = a_star_search(player_pos)
            algs.append("aStar")
            init_game(player_pos, algs)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            positions_q = Q_learning(player_pos)
            algs.append("q")
            init_game(player_pos, algs)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            positions_d = depth_first_search(player_pos)
            positions_b = bredth_first_search(player_pos)
            positions_aStar = a_star_search(player_pos)
            positions_q = Q_learning(player_pos)
            algs.append("b")
            algs.append("d")
            algs.append("q")
            algs.append("aStar")
            init_game(player_pos, algs)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and event.mod & pygame.KMOD_LSHIFT:
            restart_all()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()


        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            squares = generate_maze(squares, player_pos)

        elif event.type == pygame.KEYDOWN:
            player_pos = move_player_key(event.key, player_pos)

        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            drag_draw = not drag_draw

    if drag_draw:
        x, y = pygame.mouse.get_pos()
        x, y = x // square_size, y // square_size
        squares[x][y] = "wall"

    if started:
        started, new_d_pos, new_b_pos, new_q_pos, new_aStar_pos = exec_movements(positions_d, positions_b, positions_q, positions_aStar, d_pos, b_pos, q_pos, aStar_pos)
        if "d" in algs:
            d_pos = new_d_pos
        if "b" in algs:
            b_pos = new_b_pos
        if "aStar" in algs:
            aStar_pos = new_aStar_pos
        if "q" in algs:
            q_pos = new_q_pos
            
    if (is_goal_state(d_pos) and "d" in algs) and (is_goal_state(b_pos) and "b" in algs) and (is_goal_state(q_pos) and "q" in algs) and (is_goal_state(aStar_pos) and "aStar" in algs):
        restart_game()

    screen.fill(white)

    for col in range(0, width, square_size):
        for row in range(0, height, square_size):
            x, y = col//square_size, row//square_size
            color = black

            if squares[x][y] == "wall":
                color = red
            elif squares[x][y] == "goal":
                color = green
            elif (x, y) == player_pos:
                color = blue
            elif (x, y) == d_pos and "d" in algs:
                color = purple
            elif (x, y) == b_pos and "b" in algs:
                color = yellow
            elif (x, y) == q_pos and "q" in algs:
                color = orange
            elif (x, y) == aStar_pos and "aStar" in algs:
                color = brown
            pygame.draw.rect(screen, color, (col, row, square_size-1, square_size-1))

    text1 = font.render('Depth First Search (d)', True, purple)
    text2 = font.render('Breadth First Search (b)', True, yellow)
    text3 = font.render('Q-Learning (q)', True, orange)
    text4 = font.render('A Star Search(*)', True, brown)

    screen.blit(text1, (0, height + 10))
    screen.blit(text2, (300, height + 10))
    screen.blit(text3, (0, height + 50))
    screen.blit(text4, (300, height + 50))

    pygame.display.flip()
