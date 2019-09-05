import sys, pygame
pygame.init()

size = width, height = 400, 400
screen = pygame.display.set_mode(size)


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 200)
yellow = (255, 255, 0)

square_size = width//20
squares = [[0 for x in range(0, width, square_size)] for y in range(0, height, square_size)] 
saved_squares = squares

player_pos = (0, 0)

b_pos = (-1, -1)
d_pos = (-1, -1)

positions_d = []
positions_b = []

algs = []

tick_counter = 0
started = False

def get_possible_moves(current_pos):
    possible_moves = []

    x, y = current_pos
    max_x, max_y = width//square_size, height//square_size

    #check UP, RIGHT, DOWN, LEFT
    if y - 1 >= 0 and squares[x][y-1] != "wall":
        possible_moves.append(((x, y-1), pygame.K_UP))
    if y + 1 < max_y and squares[x][y+1] != "wall":
        possible_moves.append(((x, y+1), pygame.K_DOWN))
    if x - 1 >= 0 and squares[x-1][y] != "wall":
        possible_moves.append(((x-1, y), pygame.K_LEFT))
    if x + 1 < max_x and squares[x+1][y] != "wall":
        possible_moves.append(((x+1, y), pygame.K_RIGHT))

    return possible_moves

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

    def push(self,item):
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

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

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

    stack.push((startState, [])) #(estado, acoes)

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
    if squares[startState[0]][startState[1]] == "goal":
        return []

    visitedStates, queue = [], Queue()

    queue.push((startState, [])) #(estado, acoes)

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

def restart_game():
    global tick_counter, started, algs, d_pos, b_pos, squares, saved_squares
    tick_counter = 0
    started = False
    algs = []
    d_pos = (-1, -1)
    b_pos = (-1, -1)
    squares = saved_squares
    
def exec_movements(positions_d, positions_b, d_pos, b_pos):
    global tick_counter
    pygame.time.wait(500)

    if tick_counter >= len(positions_d) and tick_counter >= len(positions_b):
        return False, d_pos, b_pos

    if tick_counter < len(positions_d):
        d_pos = move_player_key(positions_d[tick_counter], d_pos)
    if tick_counter < len(positions_b):
        b_pos = move_player_key(positions_b[tick_counter], b_pos)
    tick_counter = tick_counter + 1
    return True, d_pos, b_pos

def init_game(player_pos, algs):
    global started, saved_squares, d_pos, b_pos
    started = True
    saved_squares = squares
    if "d" in algs:
        d_pos = player_pos
    if "b" in algs:
        b_pos = player_pos    

def is_goal_state(player_pos):
    return squares[player_pos[0]][player_pos[1]] == "goal"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x, y = pos[0]//square_size, pos[1]//square_size
            if event.button == 3:
                squares[x][y] = "goal"
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

        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            positions_d = depth_first_search(player_pos)
            positions_b = bredth_first_search(player_pos)
            algs.append("b")
            algs.append("d")
            init_game(player_pos, algs)
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

        elif event.type == pygame.KEYDOWN:
            player_pos = move_player_key(event.key, player_pos)


    if started:
        started, d_pos, b_pos = exec_movements(positions_d, positions_b, d_pos, b_pos)

    if is_goal_state(d_pos) and is_goal_state(b_pos):
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
            elif (x, y) == d_pos:
                color = purple
            elif (x, y) == b_pos:
                color = yellow
            pygame.draw.rect(screen, color, (col, row, square_size-1, square_size-1))

    pygame.display.flip()