import math
import heapq
import pygame

# colours
# standard node color and obstacle color
WHITE = (255, 255, 255)
GREY = (105,105,105)
BLACK = (0,0,0)
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
        self.cost = 10

    def getMyPosition(self):
        return self.row, self.col

    def draw(self, display):
        pygame.draw.rect(display, self.colour, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False

    def getNeighbors(self, grid):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for direction in directions:
            newRow = (self.row + direction[0])
            newCol = (self.col + direction[1])
            neighbor = Node(newRow, newCol, MARGIN)
            # neighbor = [self.row + direction[0], self.col + direction[1]]
            print(neighbor)
            if neighbor.row >= - 1 and neighbor.row >= -1:
                print("ye its here")
                result.append(neighbor)
        return result


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
            pygame.draw.rect(display,
                             colour,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

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
open = []
closed = []
# heapq.heapify(open)
# heapq.heappush(open, )

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:    
                position = pygame.mouse.get_pos()
                column = position[0] // (WIDTH + MARGIN)
                row = position[1] // (HEIGHT + MARGIN)
                start = Node(row, column, MARGIN)
                heapq.heappush(open, start)
                print(open[0].colour)
                grid[row][column].colour = GREEN
            if event.key == pygame.K_e:
                position = pygame.mouse.get_pos()
                column = position[0] // (WIDTH + MARGIN)
                row = position[1] // (HEIGHT + MARGIN)
                grid[row][column].colour = BLUE
            if event.key == pygame.K_SPACE:
                if not open:
                        print("select a start node")
                elif open[0].colour != BLUE:                  
                    print("not at end node. Searching...")
                    current = heapq.heappop(open)
                    heapq.heappush(closed, current)
                    neighbors = current.getNeighbors(grid)
                    # for neighbor in neighbors:
                    #     print(neighbor)
        
        elif pygame.mouse.get_pressed()[0]:
            position = pygame.mouse.get_pos()
            column = position[0] // (WIDTH + MARGIN)
            row = position[1] // (HEIGHT + MARGIN)
            grid[row][column].colour = GREY
            print("Click ", position, "Grid coordinates: ", row, column)


    display.fill(BLACK)

    # draw
    draw()
    clock.tick(60)
    pygame.display.flip()



# Nodes have F value with is the addition of the G value and H value
# G value
# Create open set of nodes that are current canadites for examination
# Begins with only the starting node inside
# Create closed set of nodes that have already been examined
# each node keeps a pointer to its parent node
#
# get manhattan distance for nodes to end node
#
pygame.quit()
