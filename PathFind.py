from PIL import Image, ImageDraw
import collections
import math
import sys
import pygame
import time
import random

#pygame.mixer.init()


'''
sound1 = pygame.mixer.Sound("computor.wav")
sound2 = pygame.mixer.Sound("proess 2.wav")
'''
def findCost(curCartWeight,nextDistance,trafficLvl,nextNumItems,condition):
    #curCartWeight and condition are updated for each node traversal. The cost is accumulated based on how much travel is still needed
    cost = 0
    #Defined weights to calculate cost
    w1 = .6
    w2 = .2
    w3 = .2
    #Cost calculations
    cost += w1*curCartWeight * nextDistance * trafficLvl
    cost += w2*nextNumItems *curCartWeight *condition #if next node has many items, we can include the time spent in that department
    cost += w3*condition *nextDistance*trafficLvl



def avergae_pixl(x, y, pixel_size, map):

    pixel_sample = [[],[],[]]

    color_sample = collections.defaultdict(set)
    commonRGB = (0,0,0)
    common = 0


    #Finding the most common colour in one pixel area
    surr = int(pixel_size / 2)

    for s in range(-surr, surr + 1):
        for t in range(-surr, surr + 1):
            #input()
            try:
                if map[x + t, y + s] in color_sample:
                    color_sample[map[x + t, y + s]] += 1
                    if color_sample[map[x + t, y + s]] > common:
                        common = color_sample[map[x + t, y + s]]
                        commonRGB = map[x + t, y + s]
                else:
                    color_sample[map[x + t, y + s]] = 1
            except IndexError:
                pass
                #print("IndexError: " + str((x+t,y+s)))

    return commonRGB

def colors():
    colo = {}
    area = 5

    walkable = []

    red = (240, 26, 36)
    blue = (63, 71, 204)
    purple = (163, 72, 167)
    green = (37, 175, 79)
    orange = (255, 127, 38)
    white = (255, 255, 255)
    yellow = (255, 242, 0)

    redArea = []
    greenArea = []
    blueArea = []
    purpleArea = []
    orangeArea = []
    whiteArea = []
    yellowArea = []

    for R in range(red[0]-area, red[0]+area):
        for G in range(red[1]-area, red[1]+area):
            for B in range(red[2]-area, red[2]+area):
                RGB = (R, G, B)
                redArea.append(RGB)
                walkable.append(RGB)

    for R in range(green[0] - 2*area, green[0] + 2*area):
        for G in range(green[1] - 2*area, green[1] + 2*area):
            for B in range(green[2] - 2*area, green[2] + 2*area):
                RGB = (R, G, B)
                greenArea.append(RGB)
                walkable.append(RGB)

    for R in range(blue[0] - area, blue[0] + area):
        for G in range(blue[1] - area, blue[1] + area):
            for B in range(blue[2] - area, blue[2] + area):
                RGB = (R, G, B)
                blueArea.append(RGB)
                walkable.append(RGB)

    for R in range(purple[0] - area, purple[0] + area):
        for G in range(purple[1] - area, purple[1] + area):
            for B in range(purple[2] - area, purple[2] + area):
                RGB = (R, G, B)
                purpleArea.append(RGB)
                walkable.append(RGB)

    for R in range(orange[0]-area, orange[0]+area):
        for G in range(orange[1]-area, orange[1]+area):
            for B in range(orange[2]-area, orange[2]+area):
                RGB = (R, G, B)
                orangeArea.append(RGB)
                walkable.append(RGB)

    for R in range(white[0]-area, white[0]):
        for G in range(white[1]-area, white[1]):
            for B in range(white[2]-area, white[2]):
                RGB = (R, G, B)
                whiteArea.append(RGB)
                walkable.append(RGB)

    for R in range(yellow[0]-area, yellow[0] + area):
        for G in range(yellow[1]-area, yellow[1] + area):
            for B in range(yellow[2]-area, yellow[2] + area):
                RGB = (R, G, B)
                yellowArea.append(RGB)
                walkable.append(RGB)

    colo = {"orange":orangeArea,
            "purple":purpleArea,
            "red":redArea,
            "blue":blueArea,
            "green":greenArea,
            "white":whiteArea,
            "yellow":yellowArea
              }

    return colo, walkable

def depCenters(depLocations):
    centers = collections.defaultdict()
    for color in depLocations:
        x = 0
        y = 0
        for coord in depLocations[color]:
            x += coord[0]
            y += coord[1]
        if len(depLocations[color]) > 0:
            center = (int(x/len(depLocations[color])),int(y/len(depLocations[color])))
            centers[color] = center
    return centers


def reader(file, pixel_size):

    map = Image.open(file)
    size = map.size
    map = map.load()

    graph = collections.defaultdict(set)
    graphw = collections.defaultdict(set)

    #Colo has all the accessible area colors
    colo = colors()

    depLocations = {
        "red":[],
        "green":[],
        "blue":[],
        "purple":[],
        "yellow":[]
    }

    #Size of image
    print("Image len(x): " + str(size[0]))
    print("Image len(y): " + str(size[1]))

    count = 0
    full = size[1]
    y = 0
    while y < (size[1] - (2 * pixel_size)):
        y += pixel_size
        x = 0
        # Loading screen...
        cur = y
        count += 1
        percent = int((cur / full) * 100)
        if count % 5 == 0:
            print("Loading: " + str(percent) + "%...")

        while x < (size[0] - (2 * pixel_size)):
            x += pixel_size

            pixel = avergae_pixl(x, y, pixel_size, map)

            up = avergae_pixl(x, y - pixel_size, pixel_size, map)
            down = avergae_pixl(x, y + pixel_size, pixel_size, map)
            left = avergae_pixl(x - pixel_size, y, pixel_size, map)
            right = avergae_pixl(x + pixel_size, y, pixel_size, map)

            up_left = avergae_pixl(x - pixel_size, y - pixel_size, pixel_size, map)
            up_right = avergae_pixl(x + pixel_size, y - pixel_size, pixel_size, map)
            down_left = avergae_pixl(x - pixel_size, y + pixel_size, pixel_size, map)
            down_right = avergae_pixl(x + pixel_size, y + pixel_size, pixel_size, map)

            surr = int(pixel_size)

            if pixel in colo[1]:
                if up in colo[1]:
                    # print("up added")
                    graph[(x, y)].add((x, y - surr))
                    graph[(x, y - surr)].add((x, y))
                    graphw[(x, y), (x, y - surr)] = 1
                    graphw[(x, y - surr), (x, y)] = 1

                if down in colo[1]:
                    # print("down added")
                    graph[(x, y)].add((x, y + surr))
                    graph[(x, y + surr)].add((x, y))
                    graphw[(x, y), (x, y + surr)] = 1
                    graphw[(x, y + surr), (x, y)] = 1

                if left in colo[1]:
                    # print("left added")
                    graph[(x, y)].add((x - surr, y))
                    graph[(x - surr, y)].add((x, y))
                    graphw[(x, y), (x - surr, y)] = 1
                    graphw[(x - surr, y), (x, y)] = 1

                if right in colo[1]:
                    # print("right added")
                    graph[(x, y)].add((x + surr, y))
                    graph[(x + surr, y)].add((x, y))
                    graphw[(x, y), (x + surr, y)] = 1
                    graphw[(x + surr, y), (x, y)] = 1

                if up_left in colo[1]:
                    graph[(x, y)].add((x - surr, y - surr))
                    graph[(x - surr, y - surr)].add((x, y))
                    graphw[(x, y), (x - surr, y - surr)] = math.sqrt(2)
                    graphw[(x - surr, y - surr), (x, y)] = math.sqrt(2)

                if down_right in colo[1]:
                    graph[(x, y)].add((x + surr, y + surr))
                    graph[(x + surr, y + surr)].add((x, y))
                    graphw[(x, y), (x + surr, y + surr)] = math.sqrt(2)
                    graphw[(x + surr, y + surr), (x, y)] = math.sqrt(2)

                if down_left in colo[1]:
                    graph[(x, y)].add((x - surr, y + surr))
                    graph[(x - surr, y + surr)].add((x, y))
                    graphw[(x, y), (x - surr, y + surr)] = math.sqrt(2)
                    graphw[(x - surr, y + surr), (x, y)] = math.sqrt(2)

                if up_right in colo[1]:
                    graph[(x, y)].add((x + surr, y - surr))
                    graph[(x + surr, y - surr)].add((x, y))
                    graphw[(x, y), (x + surr, y - surr)] = math.sqrt(2)
                    graphw[(x + surr, y - surr), (x, y)] = math.sqrt(2)

            if pixel in colo[0]["red"]:
                depLocations["red"].append((x,y))
            if pixel in colo[0]["green"]:
                depLocations["green"].append((x, y))
            if pixel in colo[0]["blue"]:
                depLocations["blue"].append((x,y))
            if pixel in colo[0]["purple"]:
                depLocations["purple"].append((x,y))
            if pixel in colo[0]["yellow"]:
                depLocations["yellow"].append((x, y))

    centers = depCenters(depLocations)
    return graph, graphw, centers

def test(graph):
    while True:
        x = input("Give x: ")
        y = input("Give y: ")

        for connection in graph[x + "," + y]:
            print(connection)

def dijkstra(graph, graphw, start):
    unvisited = []
    unvisited = []
    dist = collections.defaultdict()
    prev = collections.defaultdict()

    # Setting distances to infinity and intializing previous nodes to
    for node in graph:
        # print(node)
        dist[node] = math.inf
        prev[node] = None
        unvisited.append(node)

    dist[start] = 0
    full = len(unvisited)
    count = 0
    while unvisited:
        count += 1
        cur = len(unvisited)
        #Loading screen...
        percent = int((1-(cur/full))*100)
        if count%1000 == 0:
            print("Loading: " + str(percent) + "%...")
        # Infinity
        min = math.inf

        # Finding the smallest distance from the univisited nodes
        for node in unvisited:
            if dist[node] <= min:
                min = dist[node]
                min_node = node
        unvisited.remove(min_node)
        # Iterating trough the paths
        # print("Parrent: " + str(min_node))
        for neigh in graph[min_node]:
            # print("Child: " + str(neigh))
            line = (min_node), (neigh)
            test = dist[min_node] + graphw[line]
            # Checking if the path is shorter
            if test < dist[neigh]:
                dist[neigh] = test
                prev[neigh] = min_node
    return dist, prev

def main():

###############################################################################################
    pixel_size = 20 #10
    print("Pixel size: " + str(pixel_size))
    file = "star.jpg"
    data = reader(file, pixel_size)
    map = Image.open(file)
    size = map.size
    width = size[0]
    height = size[1]
    red = (240, 26, 36)

    depLocations = data[2]
    green_di = dijkstra(data[0], data[1], depLocations["green"])
    blue_di = dijkstra(data[0], data[1], depLocations["blue"])
    red_di = dijkstra(data[0], data[1], depLocations["red"])
    purple_di = dijkstra(data[0], data[1], depLocations["purple"])
    yellow_di = dijkstra(data[0], data[1], depLocations["yellow"])

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CampusNavi")

    map = pygame.image.load(file).convert_alpha()
    window.blit(map, (0, 0))
    coord = None
    start = None
    end = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
                quit(0)

            #Determine starting and ending point
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                if start == None:
                    start = coord
                elif end == None and start != None:
                    end = coord

            #Clear map
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    map = pygame.image.load(file).convert_alpha()
                    window.blit(map, (0, 0))
                    start = None
                    end = None

        if start != None:
            pygame.draw.circle(map, red, start, int(pixel_size))
        if end != None:
            pygame.draw.circle(map, red, end, int(pixel_size))

            '''
            startx = start[0]
            starty = start[1]
            endx = end[0]
            endy = end[1]
            '''

            for dep in depLocations:

                for dep2 in depLocations:
                    newcol = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    startx = depLocations[dep][0]
                    starty = depLocations[dep][1]
                    endx = depLocations[dep2][0]
                    endy = depLocations[dep2][1]

                    #Finding the nearest large pixel
                    for x in range(int(-pixel_size/2),int(pixel_size/2)):
                        for y in range(int(-pixel_size/2),int(pixel_size/2)):
                            if (startx + x, starty + y) in data[0].keys():
                                start = (startx + x, starty + y)
                            if (endx + x, endy + y) in data[0].keys():
                                end = (endx + x, endy + y)

                    print("Staring location: (" + str(start[0]) + "," + str(start[1]) + ")")
                    print("Ending location: (" + str(end[0]) + "," + str(end[1]) + ")")

                    solution = dijkstra(data[0], data[1], start)

                    prev = solution[1]
                    path = []
                    next = end
                    print(next)
                    end = None
                    col = (0, 0 , 0)
                    count = 0
                    try:
                        steps = 1
                        while prev[next]:
                            steps += 1
                            path.append(next)

                            pygame.draw.circle(map, newcol, next, 7)
                            next = prev[next]
                        path.append(next)
                        print("Number of steps: " + str(steps))
                        #print(path)
                    except KeyError:
                        print("No path.")
                    pygame.display.update()
                    window.blit(map, (0, 0))
                    time.sleep(0.5)

        pygame.display.update()
        window.blit(map, (0, 0))
main()