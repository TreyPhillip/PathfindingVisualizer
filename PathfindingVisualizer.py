import math
import heapq
import pygame
import time

# colours
# white for the default nodes
# Grey fo the walls or obstacles
# black for node margins
# Orange for nodes int the 
WHITE = (255, 255, 255)
GREY = (105,105,105)
BLACK = (0,0,0)
ORANGE = (255,178,102)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
RED = (213, 50, 80)

WIDTH = 20
HEIGHT = 20
MARGIN = 2

SCREEN_SIZE = (883, 883)

start = None
current = None
end = None
open = []
closed = []
# create grid
grid = [] 

# node class
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.colour = WHITE
        self.parent = None
        self.gcost = 1
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
        return self.fcost < other.fcost
    # get neighbors of self on provided grid
    def getNeighbors(self, grid):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for direction in directions:
            newRow = (self.row + direction[0])
            newCol = (self.col + direction[1])
            if newRow > -1 and newCol > -1 and newRow < 40 and newCol < 40:
                neighbor = grid[newRow][newCol]
                result.append(neighbor)
        # result = [item for item in result if item.col > -1 and item.row > -1]
        return result
    # set of methods to change Node colour based on node type
    def makeStart(self):
        self.colour = GREEN
    def makeEnd(self):
        self.colour = BLUE
    def makeWall(self):
        self.colour = GREY
    def makeOpen(self):
        self.colour = ORANGE
    def makeClosed(self):
        self.colour = RED
    # set of methods to chek if the node is in a particular state
    def isStart(self):
        return self.colour == GREEN
    def isEnd(self):
        return self.colour == BLUE
    def isWall(self):
        return self.colour == GREY
    def isOpen(self):
        return self.colour == ORANGE
    def isClosed(self):
        return self.colour == RED
    #reset node to default white
    def reset(self):
        self.colour = WHITE

#! unused mothod for now. once algorithm is complete may implement
def getCostForNeighbors(neighbors):
    for neighbor in neighbors:
        getManhattanDistance(neighbor.row, neighbor.col)

# get position of node at mouse position
def getPosition():
    position = pygame.mouse.get_pos()
    column = position[0] // (WIDTH + MARGIN)
    row = position[1] // (HEIGHT + MARGIN)
    coords = (row, column)
    return coords

# set of action to take on mouse click
# checks to see if node is start or end to allow replacing of them
# then turns clicked nodes into walls
def mouseClick(start, end, grid):
    row, col = getPosition()
    if grid[row][col] == start:
        start = None
        grid[row][col].reset()
    if grid[row][col] == end:
        end = None
    grid[row][col].makeWall()
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
                colour = BLUE
            if grid[row][column].isOpen():
                colour = ORANGE
            if grid[row][column].isClosed():
                colour = RED
            pygame.draw.rect(
                display, colour, 
                [(MARGIN + WIDTH) * column + MARGIN, 
                 (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

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

# TODO: write comments once algorithm is complete
def algorithm(grid, current, start, end):
    heapq.heappush(open, start)
    if not open:
        print("select a start node")
    elif not end:
        print("select an end node")
    else:
        while open[0] != end:   
            cost = None
            endLocation = end.getMyPosition()           
            print("not at end node. Searching...")
            # get the best node from open set 
            # and make that current node
            current = heapq.heappop(open)
            print(current.fcost, "best node chosen")
            if current.colour != BLUE and current.colour != GREEN:
                current.colour = RED                      
            heapq.heappush(closed, current)
            # get neighbors for current node
            neighbors = current.getNeighbors(grid)
            # get F cost for each neighbor
            for neighbor in neighbors:
                neighbor.gcost += current.gcost
                neighbor.hcost = getManhattanDistance(neighbor.getMyPosition(), endLocation)
                neighbor.fcost = neighbor.gcost + neighbor.hcost
                print("printing neighbor", neighbor.fcost)
                if neighbor.colour != BLUE and neighbor.colour != GREEN and neighbor.colour != RED:                              
                    neighbor.colour = ORANGE
                cost = current.gcost + neighbor.gcost
                if neighbor in open and cost < neighbor.gcost:
                    index = open.index(neighbor)
                    open[i] = open[-1]
                    open.pop()
                    heapq.heapify(open)
                heapq.heappush(open, neighbor)
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
pygame.display.set_caption('Pathfinding Visualizer')
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif pygame.mouse.get_pressed()[0]:
            mouseClick(start, end, grid)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:    
                if not start:
                    row, col = getPosition()
                    start = grid[row][col]
                    grid[row][col].makeStart()
            elif event.key == pygame.K_e:
                if not end:
                    row, col = getPosition()
                    end = grid[row][col]
                    grid[row][col].makeEnd()           
            elif event.key == pygame.K_SPACE:
                algorithm(grid, current, start, end)
    display.fill(BLACK)
    # draw
    draw()
    clock.tick(60)
    pygame.display.update()
pygame.quit()