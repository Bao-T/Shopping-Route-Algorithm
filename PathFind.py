from PIL import Image, ImageDraw
import collections
import math
import sys
import pygame
import time

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
    for s in range(int(-pixel_size / 2), int((pixel_size / 2) + 1)):
        for t in range(int(-pixel_size / 2), int((pixel_size / 2) + 1)):
            #input()
            try:
                pixel_sample[0].append(map[x + t, y + s][0])
                pixel_sample[1].append(map[x + t, y + s][1])
                pixel_sample[2].append(map[x + t, y + s][2])
            except IndexError:
                print("IndexError: " + str((x+t,y+s)))

    color_average = (int(sum(pixel_sample[0]) / len(pixel_sample[0])),
                     int(sum(pixel_sample[1]) / len(pixel_sample[1])),
                     int(sum(pixel_sample[2]) / len(pixel_sample[2])))
    #print(color_average)
    return color_average

def reader(file, pixel_size):

    map = Image.open(file)
    size = map.size
    map = map.load()

    graph = collections.defaultdict(set)
    graphw = collections.defaultdict(set)

    nogo = []
    # Adding white colour to the nogo zone
    for R in range(240, 255):
        for G in range(240, 255):
            for B in range(240, 255):
                RGB = (R, G, B)
                nogo.append(RGB)

    y = 2 * pixel_size
    print("Image len(x): " + str(size[0]))
    print("Image len(y): " + str(size[1]))

    while y < (size[1] - (2 * pixel_size)):
        y += pixel_size
        x = 2 * pixel_size
        while x < (size[0] - (2 * pixel_size)):
            x += pixel_size
            #print(x,y)
            pixel = avergae_pixl(x, y, pixel_size, map)   #map[x, y]
            up = avergae_pixl(x, y - pixel_size, pixel_size, map)            #map[x, y - 1]
            down = avergae_pixl(x, y + pixel_size, pixel_size, map) #map[x, y + 1]
            left = avergae_pixl(x - pixel_size, y, pixel_size, map) #map[x - 1, y]
            right = avergae_pixl(x + pixel_size, y, pixel_size, map) #map[x + 1, y]
            up_left = avergae_pixl(x - pixel_size, y - pixel_size, pixel_size, map) #map[x - 1, y - 1]
            up_right = avergae_pixl(x + pixel_size, y - pixel_size, pixel_size, map) #map[x + 1, y - 1]
            down_left = avergae_pixl(x - pixel_size, y + pixel_size, pixel_size, map) #map[x - 1, y + 1]
            down_right = avergae_pixl(x + pixel_size, y + pixel_size, pixel_size, map) #map[x + 1, y + 1]
            surr = int(pixel_size)
            if pixel not in nogo:
                if up not in nogo:
                    # print("up added")
                    graph[(x, y)].add((x, y - surr))
                    graph[(x, y - surr)].add((x, y))
                    graphw[(x, y), (x, y - surr)] = 1
                    graphw[(x, y - surr), (x, y)] = 1

                if down not in nogo:
                    # print("down added")
                    graph[(x, y)].add((x, y + surr))
                    graph[(x, y + surr)].add((x, y))
                    graphw[(x, y), (x, y + surr)] = 1
                    graphw[(x, y + surr), (x, y)] = 1

                if left not in nogo:
                    # print("left added")
                    graph[(x, y)].add((x - surr, y))
                    graph[(x - surr, y)].add((x, y))
                    graphw[(x, y), (x - surr, y)] = 1
                    graphw[(x - surr, y), (x, y)] = 1

                if right not in nogo:
                    # print("right added")
                    graph[(x, y)].add((x + surr, y))
                    graph[(x + surr, y)].add((x, y))
                    graphw[(x, y), (x + surr, y)] = 1
                    graphw[(x + surr, y), (x, y)] = 1
                '''
                if up_right not in nogo:
                    graph[(x, y)].add((x + pixel_size, y - pixel_size))
                    graph[(x + pixel_size, y - pixel_size)].add((x, y))
                    graphw[(x, y), (x + pixel_size, y - pixel_size)] = 1
                    graphw[(x + pixel_size, y - pixel_size), (x, y)] = 1

                if up_left not in nogo:
                
                    graph[(x, y)].add((x - pixel_size, y - pixel_size))
                    graph[(x - pixel_size, y - pixel_size)].add((x, y))
                    graphw[(x, y), (x - pixel_size, y - pixel_size)] = 1
                    graphw[(x - pixel_size, y - pixel_size), (x, y)] = 1

                if down_right not in nogo:
                    graph[(x, y)].add((x + pixel_size, y + pixel_size))
                    graph[(x + pixel_size, y + pixel_size)].add((x, y))
                    graphw[(x, y), (x + pixel_size, y + pixel_size)] = 1
                    graphw[(x + pixel_size, y + pixel_size), (x, y)] = 1

                if down_left not in nogo:
                    graph[(x, y)].add((x - pixel_size, y + pixel_size))
                    graph[(x - pixel_size, y + pixel_size)].add((x, y))
                    graphw[(x, y), (x - pixel_size, y + pixel_size)] = 1
                    graphw[(x - pixel_size, y + pixel_size), (x, y)] = 1
                '''
    print(graph)
    print(graphw)
    return graph, graphw

def test(graph):
    while True:
        x = input("Give x: ")
        y = input("Give y: ")

        for connection in graph[x + "," + y]:
            print(connection)


def dijkstra(graph, graphw, start):
    print(graph)
    unvisited = []
    dist = collections.defaultdict()
    prev = collections.defaultdict()

    # Setting distances to infinity and intializing previous nodes to
    for node in graph:
        # print(node)
        dist[node] = math.inf
        prev[node] = None
        unvisited.append(node)
    '''
    if start in graph.keys():
        dist[start] = 0
    else:
        startx = start[0]
        starty = start[1]
        for x in range(10):
            for y in range(10):
                if (startx + x, starty + y) in graph.keys():
                    start = (startx + x, starty + y)
    
    '''
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
            '''
            # print(line)
            # print(graphw[line])
            # print(line)
            #print(neigh)
            #print(dist[min_node])
            #print(graphw[line])
            '''
            test = dist[min_node] + graphw[line]
            # Checking if the path is shorter
            if test < dist[neigh]:
                dist[neigh] = test
                prev[neigh] = min_node
    # print(dist)
    # print(prev)
    return dist, prev


def pathfinder(prev, end, map):
    path = []
    next = end
    red = (255, 0, 0)
    colour = (0, 0, 0)
    count = 0
    try:
        while prev[next]:
            colour[0] += 10
            colour[1] += 10
            colour[2] += 10
            path.append(next)
            #time.sleep(5)
            pygame.draw.circle(map, colour, next, 5)
            next = prev[next]
        path.append(next)
        #print(path)
        input()
    except KeyError:
        print("No path.")
        input()

def router():
    while True:
        data = reader("map.jpg")

        print("--Give starting location--")
        x = int(input("Give x: "))
        y = int(input("Give y: "))
        if x == "stop" or y == "stop":
            quit(0)

        start = (x, y)
        solution = dijkstra(data[0], data[1], start)
        while True:
            print("--Give target location--")
            x = int(input("Give x: "))
            y = int(input("Give y: "))
            end = (x, y)

            distance = solution[0]
            prev = solution[1]
            pathfinder(prev, end)
            # print(distance[end])

def main():

    pixel_size = 20
    file = "colormap.jpg"
    data = reader(file, pixel_size)
    map = Image.open(file)
    size = map.size
    width = size[0]
    height = size[1]
    red = (255, 0, 0)

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
            pygame.draw.circle(map, red, start, 5)
        if end != None:
            pygame.draw.circle(map, red, end, 5)

            startx = start[0]
            starty = start[1]
            endx = end[0]
            endy = end[1]

            #Finding the nearest large pixel
            for x in range(int(-pixel_size/2),int(pixel_size/2)):
                for y in range(int(-pixel_size/2),int(pixel_size/2)):
                    if (startx + x, starty + y) in data[0].keys():
                        start = (startx + x, starty + y)
                    if (endx + x, endy + y) in data[0].keys():
                        end = (endx + x, endy + y)
            solution = dijkstra(data[0], data[1], start)
            prev = solution[1]
            path = []
            next = end
            end = None
            col = (0, 0 , 0)
            count = 0
            try:
                while prev[next]:
                    count += 5
                    if count > 255:
                        count = 0
                    col = (count, 0, 0)
                    #print(next)
                    path.append(next)
                    #print(next)
                    pygame.draw.circle(map, red, next, 7)
                    next = prev[next]
                path.append(next)
                #print(path)
            except KeyError:
                print("No path.")

        pygame.display.update()
        window.blit(map, (0, 0))
main()