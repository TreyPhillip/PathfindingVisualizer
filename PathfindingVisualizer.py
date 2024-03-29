import math
import heapq
import pygame
import time

# TODO
# Add Popup windows/menus
# add options to pre-genterate a maze for the user
# resize window to add more nodes

# tuples for RGB values of the screen and different node states. subject to change while searching for best clarity
# white for the default nodes
# Grey for the walls or obstacles
# black for node margins
# Orange for nodes in the open set
# green for start node
# red for end node
# blue for the closed set
# yellow for the best path
NODE_COLOUR = (255, 255, 255)
WALL_COLOUR = (47,79,79)
MARGIN_COLOUR = (0,0,0)
OPEN_COLOUR = (255,178,102)
START_COLOUR = (0, 255, 0)
CLOSED_COLOUR = (82, 191, 255)
END_COLOUR = (213, 50, 80)
BEST_PATH_COLOUR = (243, 255, 82)

WIDTH = 20
HEIGHT = 20
MARGIN = 2

SCREEN_SIZE = (883, 883)

# start, end and current nodes for referencing 
start = None
current = None
end = None

# open and closed set. Open is a min heap using heapq
# closed is regular list
open = []
closed = []
# initialize empty grid
grid = []
# boolean to check if the program has already been run,
#  if it has, will reset only certain nodes to be rerun
rerun = False
# boolean to check if the program has been ended
done = False

# node class
class Node:
    # initialize node attributes
    def __init__(self, row, col, width, height):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.height = height
        self.colour = NODE_COLOUR
        self.parent = None
        self.gcost = math.inf
        self.hcost = 0
        self.fcost = 0
    # return position of self. grid[i][i].getMyPosition
    def getMyPosition(self):
        return self.row, self.col
    # node draws itself
    def draw(self, display):
        pygame.draw.rect(display, self.colour,
        [(MARGIN + WIDTH) * self.col + MARGIN,
         (MARGIN + HEIGHT) * self.row + MARGIN, WIDTH, HEIGHT])
        pygame.display.update()
    # used when Python compares one node against another in a heap
    def __lt__(self, other):
        # if self.fcost == other.fcost:
        #     return self.hcost > other.hcost
        return self.fcost < other.fcost
    # get neighbors of self on provided grid
    #TODO enable diagonal movement?
    def getNeighbors(self, grid):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for direction in directions:
            newRow = (self.row + direction[0])
            newCol = (self.col + direction[1])
            if newRow > -1 and newCol > -1 and newRow < 40 and newCol < 40:
                neighbor = grid[newRow][newCol]
                if neighbor.isWall() == False:
                    result.append(neighbor)
        # result = [item for item in result if item.col > -1 and item.row > -1]
        return result
    # set of methods to change Node colour based on node type
    def makeStart(self):
        self.colour = START_COLOUR
    def makeEnd(self):
        self.colour = END_COLOUR
    def makeWall(self):
        self.colour = WALL_COLOUR
    def makeOpen(self):
        self.colour = OPEN_COLOUR
    def makeClosed(self):
        self.colour = CLOSED_COLOUR
    def makeBest(self):
        self.colour = BEST_PATH_COLOUR
    # set of methods to chek if the node is in a particular state
    def isStart(self):
        return self.colour == START_COLOUR
    def isEnd(self):
        return self.colour == END_COLOUR
    def isWall(self):
        return self.colour == WALL_COLOUR
    def isOpen(self):
        return self.colour == OPEN_COLOUR
    def isClosed(self):
        return self.colour == CLOSED_COLOUR
    def isBest(self):
        return self.colour == BEST_PATH_COLOUR
    #reset node to default white
    def reset(self):
        self.colour = NODE_COLOUR

# get position of node at mouse position
def getPosition():
    position = pygame.mouse.get_pos()
    column = position[0] // (WIDTH + MARGIN)
    row = position[1] // (HEIGHT + MARGIN)
    coords = (row, column)
    return coords

# set of action to take on mouse LEFT click
# checks to see if node is start or end to allow replacing of them
# then turns clicked nodes into walls
def placeWalls(start, end, grid):
    row, col = getPosition()
    if grid[row][col].isStart():
        start = None
        grid[row][col].makeWall()
    elif grid[row][col].isEnd():
        end = None
        grid[row][col].makeWall()
    else:
        grid[row][col].makeWall()

# set of action to take on mouse RIGHT click
# checks to see if node is start or end to allow replacing of them
# then resets clicked node
def resetNode(start, end, grid):
    row, col = getPosition()
    if grid[row][col].isStart():
        start = None
        grid[row][col].reset()
    elif grid[row][col].isEnd():
        end = None
        grid[row][col].reset()
    else:
        grid[row][col].reset()

# draw nodes on screen and draw colors based on class method returns
def draw():
    for row in range(40):
        for column in range(40):
            colour = NODE_COLOUR
            if grid[row][column].isWall():
                colour = WALL_COLOUR
            if grid[row][column].isStart():
                colour = START_COLOUR
            if grid[row][column].isEnd():
                colour = END_COLOUR
            if grid[row][column].isOpen():
                colour = OPEN_COLOUR
            if grid[row][column].isClosed():
                colour = CLOSED_COLOUR
            if grid[row][column].isBest():
                colour = BEST_PATH_COLOUR
            pygame.draw.rect(
                display, colour,
                [(MARGIN + WIDTH) * column + MARGIN,
                 (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

# starting from end node follow parents to start node for best path
def drawShortestPath(grid, end):
    last = end
    for x in range(40):
        for y in range(40):
            if last.parent == start:
                break
            lastx, lasty = last.getMyPosition()
            cameFrom = grid[lastx][lasty].parent
            cfx, cfy = cameFrom.getMyPosition()
            if not grid[cfx][cfy].isStart():
                grid[cfx][cfy].makeBest()
            grid[cfx][cfx].draw(display)
            last = cameFrom

# reset the grid completely
def resetGrid(grid):
    for x in range(40):
        for y in range(40):
            grid[x][y].reset()
            grid[x][y].parent = None
            grid[x][y].hcost = 0
            grid[x][y].gcost = math.inf
            grid[x][y].fcost = 0

# reset the grid keeping the walls, start and end nodes
def resetForReRun(grid):
    for x in range(40):
        for y in range(40):
            if grid[x][y].isStart() or grid[x][y].isEnd() or grid[x][y].isWall():
                grid[x][y].parent = None
                grid[x][y].hcost = 0
                grid[x][y].gcost = math.inf
                grid[x][y].fcost = 0
            else:
                grid[x][y].reset()
                grid[x][y].parent = None
                grid[x][y].hcost = 0
                grid[x][y].gcost = math.inf
                grid[x][y].fcost = 0

# get the "manhattan distance" between two coordinates
# the absolute value of value 1 in the first coords 
# subtracted by the first value in the other 
# then the same for the second values
#then returning the sum of the resulting values
def getManhattanDistance(pt1, pt2):
    distance = 0
    for i in range(len(pt1)):
        distance += abs(pt1[i] - pt2[i])
    return distance

# starting from start node, evaluate neighboring nodes to 
# find best path to end node
#* algorithm is A*. This algorithm knows the 
#* location of the end node and makes its decision with another 
#* function that gets a heuristic for the distance between the 
#* current node and the end node. gives each node it discovers
#* a value of the distance from the start to the current node plus the heuristic
#* then, it chooses the current cheapest node, repeating untill end is found

def algorithm(grid, current, start, end):
    if not start:
        print("select a start node")
        return
    elif not end:
        print("select an end node")
        return
    start.gcost = 0
    start.fcost = getManhattanDistance(start.getMyPosition(), end.getMyPosition())
    heapq.heappush(open, start)
    if open:
        while open[0] != end:
            # get the best node from open set
            # and make that current node
            current = heapq.heappop(open)
            if not current.isStart() and not current.isEnd():
                current.makeClosed()
                current.draw(display)
            closed.append(current)
            neighbors = current.getNeighbors(grid)
            for neighbor in neighbors:
                cost = None
                cost = current.gcost + 10
                if neighbor in open and cost < neighbor.gcost:
                    neighbor.reset()
                    i = open.index(neighbor)
                    open[i] = open[-1]
                    open.pop()
                    heapq.heapify(open)
                if neighbor in closed and cost < neighbor.gcost:
                    closed.remove(neighbor)
                    neighbor.reset()
                if neighbor not in open and neighbor not in closed:
                    neighbor.gcost = cost        
                    neighbor.hcost = getManhattanDistance(neighbor.getMyPosition(), end.getMyPosition())
                    neighbor.fcost = neighbor.gcost + neighbor.hcost 
                    neighbor.parent = current
                    if not neighbor.isEnd():
                        neighbor.makeOpen()
                        neighbor.draw(display)
                    print("Neighbors for current. FCOST: ", neighbor.fcost)
                    heapq.heappush(open, neighbor) 
            if not open:
                    print("connot find end node")
                    return                
        drawShortestPath(grid, end)     
        print("FOUND YOU")  

# initialize the grid with Node objects
for x in range(40):
    grid.append([])
    for y in range(40):
        node = Node(x, y, WIDTH, HEIGHT)
        grid[x].append(node)

# init function for pygame
pygame.init()

# create display and set size. Currently using
#  883 x 883 as it fits 40 x 40 20 x 20 px squares
display = pygame.display.set_mode((883, 883))

# set caption of the display
pygame.display.set_caption('Pathfinding Visualizer - S for Start node - E for End - Left Click for wall - Right Click for reset selected - R reset all - SPACE to run')
clock = pygame.time.Clock()

# check for inputs and execute tasks based on said inputs
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        # exit game 
        if event.type == pygame.QUIT:
            done = True
        # place walls
        elif pygame.mouse.get_pressed()[0]:
            placeWalls(start, end, grid)

        # reset selected node
        elif pygame.mouse.get_pressed()[2]:
            resetNode(start, end, grid)

        # keypress events
        elif event.type == pygame.KEYDOWN:
            # check if the start node has been placed if not, 
            # set node to star if it has been placed, remove 
            # the current node and place it in new location.
            if event.key == pygame.K_s:    
                row, col = getPosition()
                if not start:   
                    start = grid[row][col]
                    grid[row][col].makeStart()                 
                else:
                    for x in range(40):
                        for y in range(40):
                            if grid[x][y].isStart():
                                start = None
                                grid[x][y].reset()
                    if grid[row][col].isEnd():
                        end = None
                        start = grid[row][col]
                        grid[row][col].makeStart()
                    else:
                        start = grid[row][col]
                        grid[row][col].makeStart()
            elif event.key == pygame.K_e:
                row, col = getPosition()
                if not end:
                    end = grid[row][col]
                    grid[row][col].makeEnd()
                elif end:
                    for x in range(40):
                        for y in range(40):
                            if grid[x][y].isEnd():
                                end = None
                                grid[x][y].reset()
                            elif grid[row][col].isStart():
                                start = None
                                end = grid[row][col]
                                grid[row][col].makeEnd()
                            else:
                                end = grid[row][col]
                                grid[row][col].makeEnd()
            elif event.key == pygame.K_r:
                start = None
                end = None
                current = None
                closed = []
                open = []
                resetGrid(grid)
                rerun = False
            elif event.key == pygame.K_SPACE:
                if not rerun:
                    algorithm(grid, current, start, end)
                    rerun = True
                else:
                    current = None
                    closed = []
                    open = []
                    resetForReRun(grid)
                    draw()
                    pygame.display.update()
                    algorithm(grid, current, start, end)
    display.fill(MARGIN_COLOUR)
    # draw
    draw()
    pygame.display.update()

#quit fuction for pygame
pygame.quit()