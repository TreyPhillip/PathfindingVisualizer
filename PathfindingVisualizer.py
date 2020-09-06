import math
import heapq
import pygame
import time

# colours
# standard node color and obstacle color
WHITE = (255, 255, 255)
GREY = (105,105,105)
BLACK = (0,0,0)
# open set
ORANGE = (255,178,102)
# start node
GREEN = (0, 255, 0)
# end node
BLUE = (50, 153, 213)
# closed set
RED = (213, 50, 80)

WIDTH = 20
HEIGHT = 20
MARGIN = 2

SCREEN_SIZE = (883, 883)

# TODO
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
        self.gcost = 10
        self.hcost = 0
        self.fcost = 0

    def getMyPosition(self):
        return self.row, self.col

    def draw(self, display):
        pygame.draw.rect(display, self.colour, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return self.fcost < other.fcost

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

def getCostForNeighbors(neighbors):
    for neighbor in neighbors:
        getManhattanDistance(neighbor.row, neighbor.col)

def getPosition():
    position = pygame.mouse.get_pos()
    column = position[0] // (WIDTH + MARGIN)
    row = position[1] // (HEIGHT + MARGIN)
    coords = (row, column)
    return coords

def draw():
    for row in range(40):
        for column in range(40):
            colour = WHITE
            if grid[row][column].colour == GREY:
                colour = GREY
            if grid[row][column].colour == GREEN:
                colour = GREEN
            if grid[row][column].colour == BLUE:
                colour = BLUE
            if grid[row][column].colour == ORANGE:
                colour = ORANGE
            if grid[row][column].colour == RED:
                colour = RED
            pygame.draw.rect(
                display, colour, 
                [(MARGIN + WIDTH) * column + MARGIN, 
                 (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

def getManhattanDistance(pt1, pt2):
    distance = 0
    for i in range(len(pt1)):
        distance += abs(pt1[i] - pt2[i])
    return distance

# create grid
grid = [] 
for x in range(40):
    grid.append([])
    for y in range(40):
        node = Node(x, y, MARGIN)
        grid[x].append(node)

pygame.init()
display = pygame.display.set_mode((883, 883))
pygame.display.set_caption('Pathfinding Visualizer')
done = False
clock = pygame.time.Clock()

# use Binary heap for open and closed nodes
start = None
current = None
end = None
# Create open set of nodes that are current canadites for examination
# Begins with only the starting node inside
open = []
# Create closed set of nodes that have already been examined
closed = []
# heapq.heapify(open)
# heapq.heappush(open, )

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif pygame.mouse.get_pressed()[0]:
            row, col = getPosition()
            grid[row][col].colour = GREY
            print("Grid coordinates: ", row, col)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:    
                if not start:
                    row, col = getPosition()
                    start = grid[row][col]
                    grid[row][col].colour = GREEN
                    heapq.heappush(open, start)
            elif event.key == pygame.K_e:
                if not end:
                    row, col = getPosition()
                    end = grid[row][col]
                    grid[row][col].colour = BLUE           
            elif event.key == pygame.K_SPACE:
                if not open:
                    print("select a start node")
                elif not end:
                    print("select an end node")
                else:
                    while current != end:   
                        endLocation = end.getMyPosition()           
                        print("not at end node. Searching...")
                        # get the best node from open set 
                        # and make that current node
                        current = heapq.heappop(open)
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
                            if neighbor.colour != BLUE and neighbor.colour != GREEN and neighbor.colour != RED:
                                neighbor.colour = ORANGE
                            heapq.heappush(open, neighbor)
                    print("FOUND YOU")
    display.fill(BLACK)
    # draw
    draw()
    clock.tick(60)
    pygame.display.flip()



# Nodes have F value with is the addition of the G value and H value
# G value


# each node keeps a pointer to its parent node
#
# get manhattan distance for nodes to end node
#
pygame.quit()
