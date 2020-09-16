import math
import heapq
import pygame
import time

# colours
# white for the default nodes
# Grey for the walls or obstacles
# black for node margins
# Orange for nodes in the open set
# green for start node
# red for end node
# blue for the closed set
# darker blue for the best path
WHITE = (255, 255, 255)
GREY = (47,79,79)
BLACK = (0,0,0)
ORANGE = (255,178,102)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
RED = (213, 50, 80)
DARK_BLUE = (65,105,225)

WIDTH = 20
HEIGHT = 20
MARGIN = 2

SCREEN_SIZE = (883, 883)

#start, end and current nodes for referencing 
start = None
current = None
end = None

# open and closed set. Open is a min heap using heapq
# closed is regular list
open = []
closed = []
# initialize empty grid
grid = []
# boolean to check if the program has been ended
done = False

# node class
class Node:
    # initialize node attributes
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.colour = WHITE
        self.parent = None
        self.gcost = math.inf
        self.hcost = 0
        self.fcost = 0
    # return position of self. grid[i][i].getMyPosition
    def getMyPosition(self):
        return self.row, self.col
    #! unused so far. may implement later
    def draw(self, display):
        pygame.draw.rect(display, self.colour, (self.x, self.y, self.width, self.width))
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
        self.colour = GREEN
    def makeEnd(self):
        self.colour = RED
    def makeWall(self):
        self.colour = GREY
    def makeOpen(self):
        self.colour = ORANGE
    def makeClosed(self):
        self.colour = BLUE
    def makeBest(self):
        self.colour = DARK_BLUE
    # set of methods to chek if the node is in a particular state
    def isStart(self):
        return self.colour == GREEN
    def isEnd(self):
        return self.colour == RED
    def isWall(self):
        return self.colour == GREY
    def isOpen(self):
        return self.colour == ORANGE
    def isClosed(self):
        return self.colour == BLUE
    def isBest(self):
        return self.colour == DARK_BLUE
    #reset node to default white
    def reset(self):
        self.colour = WHITE

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
def mouseClick(start, end, grid):
    row, col = getPosition()
    if grid[row][col].isStart():
        start = None
        grid[row][col].makeWall()
    elif grid[row][col].isEnd():
        end = None
        grid[row][col].makeWall()
    else:
        grid[row][col].makeWall()
    print("Grid coordinates: ", row, col)

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
    print("Grid coordinates: ", row, col)

# draw nodes on screen and draw colors based on class method returns
def draw():
    for row in range(40):
        for column in range(40):
            colour = WHITE
            if grid[row][column].isWall():
                colour = GREY
            if grid[row][column].isStart():
                colour = GREEN
            if grid[row][column].isEnd():
                colour = RED
            if grid[row][column].isOpen():
                colour = ORANGE
            if grid[row][column].isClosed():
                colour = BLUE
            if grid[row][column].isBest():
                colour = DARK_BLUE
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
            last = cameFrom

# reset the grid to be used again
def resetGrid():
    for x in range(40):
        for y in range(40):
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
#* algorithm is done in A* style. The algorithm knows the 
#* location of the end node and makes its decision with another 
#* function that gets a heuristic for the distance between the 
#* current node and the end node. gives each node it discovers
#* a value of the distance from the start to the current node plus the heuristic
#* then, it chooses the current cheapest node, repeating untill end is found
def algorithm(grid, current, start, end):
    start.gcost = 0
    start.fcost = getManhattanDistance(start.getMyPosition(), end.getMyPosition())
    heapq.heappush(open, start)
    if not open:
        print("select a start node")
    elif not end:
        print("select an end node")
    else:
        while open[0] != end:   
            # get the best node from open set 
            # and make that current node
            current = heapq.heappop(open)
            if not current.isStart() and not current.isEnd():
                current.makeClosed() 
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
                    print("Neighbors for current. FCOST: ", neighbor.fcost)
                    heapq.heappush(open, neighbor)  
        drawShortestPath(grid, end)     
        print("FOUND YOU")     

# initialize the grid with Node objects
for x in range(40):
    grid.append([])
    for y in range(40):
        node = Node(x, y, MARGIN)
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if pygame.mouse.get_pressed()[0]:
            mouseClick(start, end, grid)
        if pygame.mouse.get_pressed()[2]:
            resetNode(start, end, grid)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:    
                if not start:
                    row, col = getPosition()
                    start = grid[row][col]
                    grid[row][col].makeStart()
                elif start:
                    for x in range(40):
                        for y in range(40):
                            if grid[x][y].isStart():
                                start = None
                                grid[x][y].reset()
                            row, col = getPosition()
                            if grid[row][col].isEnd():
                                end = None
                                start = grid[row][col]
                                grid[row][col].makeStart()
                            else:
                                start = grid[row][col]
                                grid[row][col].makeStart()
            elif event.key == pygame.K_e:
                if not end:
                    row, col = getPosition()
                    end = grid[row][col]
                    grid[row][col].makeEnd()
                elif end:
                    for x in range(40):
                        for y in range(40):
                            if grid[x][y].isEnd():
                                end = None
                                grid[x][y].reset()
                            row, col = getPosition()
                            if grid[row][col].isStart():
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
                resetGrid()      
            elif event.key == pygame.K_SPACE:
                algorithm(grid, current, start, end)
    display.fill(BLACK)
    # draw
    draw()
    clock.tick(60)
    pygame.display.update()

#quit fuction for pygame
pygame.quit()