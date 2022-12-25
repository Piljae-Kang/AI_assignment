############# Write Your Library Here ###########

import queue
from turtle import circle, distance
from maze import Maze
import math

################################################


def search(maze, func):
    return {
        "bfs": bfs,
        "dfs":dfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


def bfs(maze):
    """
    [Problem 01] 제시된 stage1 맵 세 가지를 BFS Algorithm을 통해 최단 경로를 return하시오.
    """
    start_point=maze.startPoint()
    path=[]
    ####################### Write Your Code Here ################################

    current_point = start_point
    end_point = None
    queue = []
    queue.append(current_point)
    demension = maze.getDimensions()
    visited = [[-1 for j in range(demension[1])] for i in range(demension[0])]
    visited[current_point[0]][current_point[1]] = 0
    found = False

    while not len(queue) == 0:

        if found:
            break

        current_point = queue.pop(0)
        neighbors = maze.neighborPoints(current_point[0], current_point[1])

        for point in neighbors:

            if visited[point[0]][point[1]] == -1:
                if maze.choose_move(point[0], point[1]):
                    visited[point[0]][point[1]] = visited[current_point[0]][current_point[1]] + 1

                    if point == maze.circlePoints()[0]:
                        end_point = point
                        found = True
                        break

                    queue.append(point)

    back_p = end_point
    path.append(back_p)
    while True:
        if back_p == start_point:
            break
        
        neighbors = maze.neighborPoints(back_p[0], back_p[1])

        for point in neighbors:
            if(visited[point[0]][point[1]] == visited[back_p[0]][back_p[1]] -1):
                back_p = point
                path.insert(0, back_p)
                break
    

    return path

    ############################################################################


def dfs(maze):
    """
    [Problem 02] 제시된 stage1 맵 세 가지를 DFS Algorithm을 통해 최단 경로를 return하시오.
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################

    current_point = start_point
    end_point = None
    stack = []
    stack.append(current_point)

    demension = maze.getDimensions()
    visited = [[-1 for j in range(demension[1])] for i in range(demension[0])]
    visited[current_point[0]][current_point[1]] = 0
    found = False

    while not len(stack) ==0:

        if found:
            break

        current_point = stack.pop()

        neighbors = maze.neighborPoints(current_point[0], current_point[1])

        count = 0
        for point in neighbors:
            if visited[point[0]][point[1]] == -1:
                visited[point[0]][point[1]] = visited[current_point[0]][current_point[1]] + 1
                stack.append(point)

                if point == maze.circlePoints()[0]:
                        end_point = point
                        found = True
                        break

    back_p = end_point
    path.append(back_p)
    while True:
        if back_p == start_point:
            break
        
        neighbors = maze.neighborPoints(back_p[0], back_p[1])

        for point in neighbors:
            if(visited[point[0]][point[1]] == visited[back_p[0]][back_p[1]] -1):
                back_p = point
                path.insert(0, back_p)
                break

    return path

    ############################################################################



def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_minumum(open):

    minumum_index = -1

    for i in range(len(open)):
        if minumum_index == -1:
            minumum_index = i
        else:
            if open[i][1] < open[minumum_index][1]:
                minumum_index = i

    return minumum_index

def find_index(open, point):

    for i in range(len(open)):
        if open[i][0] == point:
            return i
    
    return -1

def in_closed(open, point):

    for open_list in open:
        if open_list[0] == point:
            return True

    return False


def astar(maze):
    """
    [Problem 03] 제시된 stage1 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 위에서 정의한 manhattan_dist function을 사용할 것.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################

    end_point = maze.circlePoints()[0]

    open = []
    closed = []
    h = manhattan_dist(start_point, end_point)
    g = 0
    expended_point = start_point # [0]: f, [1] : g, [2] : h, [3]: point
    expended_g = 0
    found = False

    while True:

        neighbors = maze.neighborPoints(expended_point[0], expended_point[1])
       

        for point in neighbors:

            if in_closed(closed, point):
                continue

            g = expended_g + 1
            h = manhattan_dist(point, end_point)
            open.append([point, g + h, g, h, expended_point])

            if point == end_point:
                found = True
                closed.append([point, g + h, g, h, expended_point])
                break

        if found == True:
            break

        minimum_index = find_minumum(open)

        if minimum_index == -1:
            print("didn't find endpoint")
            return path
       
        closed.append(open[minimum_index])
        expended_point = open[minimum_index][0]
        expended_g = open[minimum_index][2]
        del open[minimum_index]

    index = len(closed)-1

    while True:

        current_point = closed[index][0]
        path.insert(0, current_point)
        previous_point = closed[index][4]

        if previous_point == start_point:
            path.insert(0, previous_point)
            break

        index = find_index(closed, previous_point)

    return path


    ############################################################################



def stage2_heuristic(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2       #Euclidean Distance로 heuristic 함수 설정

def minimum_point(start_point, points):
    
    min_distance = -1
    min_point = None
    for point in points:
        if min_distance == -1:
            min_distance = stage2_heuristic(start_point, point)
            min_point = point
        else:
            distance = stage2_heuristic(start_point, point)
            if distance < min_distance:
                min_distance = distance
                min_point = point
            

    return min_point
         

def astar_four_circles(maze):
    """
    [Problem 04] 제시된 stage2 맵 세 가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 직접 정의할것 )
    """
    start_point = maze.startPoint()
    path = []
    single_path = []
    ####################### Write Your Code Here ################################

    circle_points = maze.circlePoints()

    while True:


        end_point = minimum_point(start_point, circle_points)
        circle_points.remove(end_point)

        open = []
        closed = []
        h = stage2_heuristic(start_point, end_point)
        g = 0
        expended_point = start_point # [0]: f, [1] : g, [2] : h, [3]: point
        found = False

        while True:

            neighbors = maze.neighborPoints(expended_point[0], expended_point[1])

            for point in neighbors:

                if in_closed(closed, point):
                    continue

                g = expended_point[1] + 1
                h = manhattan_dist(point, end_point)
                open.append([point, g + h, g, h, expended_point])

                if point == end_point:
                    found = True
                    closed.append([point, g + h, g, h, expended_point])
                    break

            if found == True:
                break

            minimum_index = find_minumum(open)

            if minimum_index == -1:
                print("didn't find endpoint")
                return path
        
            closed.append(open[minimum_index])
            expended_point = open[minimum_index][0]
            del open[minimum_index]

        index = len(closed)-1

        while True:

            current_point = closed[index][0]
            single_path.insert(0, current_point)
            previous_point = closed[index][4]

            if previous_point == start_point:
                single_path.insert(0, previous_point)
                break

            index = find_index(closed, previous_point)
        
        start_point = end_point

        if len(path) == 0:
            path = single_path
        else:
            path += single_path[1:]
        
        single_path = []

        if len(circle_points) == 0:
            break
            
    return path

    ############################################################################

def distance_points(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 

def mst(start_point, circles_points, visited):

    cost = 0

    circles_points.remove(start_point)
    current_point = start_point
    for point in visited:
        circles_points.remove(point)

    
    
    while len(circles_points) != 0:
        min_cost = -1
        min_point = None
        for point in circles_points:
            if min_cost == -1:
                min_cost = distance_points(current_point, point)
                min_point = point
            elif distance_points(current_point, point) < min_cost:
                min_cost = distance_points(current_point, point)
                min_point = point

        cost += min_cost
        current_point = min_point
        circles_points.remove(current_point)

    return cost


def stage3_heuristic(point, maze, visited):


    circles_points = maze.circlePoints()

    min_distance = -1
    min_point = None
    for c_p in circles_points:
        if c_p not in visited:
            if min_distance == -1:
                min_distance = distance_points(point, c_p)
                min_point = c_p
            elif distance_points(point, c_p) < min_distance:
                min_distance = distance_points(point, c_p)
                min_point = c_p
    


    return 10 * min_distance + mst(min_point, circles_points, visited)



def astar_many_circles(maze):
    """
    [Problem 04] 제시된 stage3 맵 다섯 가지를 A* Algorithm을 통해 최단 경로를 return하시오.
    (Heuristic Function은 직접 정의 하고, minimum spanning tree를 활용하도록 한다.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################



    circlePoints = maze.circlePoints()
    open = []
    closed = []
    visited = []
    h = stage3_heuristic(start_point, maze, visited)
    g = 0
    expended_point = start_point # [0]: f, [1] : g, [2] : h, [3]: point
    expended_g = 0
    found = False

    while len(visited) != len(circlePoints):

        open = []
        closed = []

        h = stage3_heuristic(start_point, maze, visited)
        g = 0
        
        #expended_point = start_point # [0]: f, [1] : g, [2] : h, [3]: point
        expended_g = 0
        found = False

        while True:

            neighbors = maze.neighborPoints(expended_point[0], expended_point[1])

            #print(neighbors)

            for point in neighbors:

                if in_closed(closed, point):
                    continue

                

                g = expended_g + 1
                h = stage3_heuristic(point, maze, visited)
                open.append([point, g + h, g, h, expended_point])

                

                if point in circlePoints and point not in visited:

                    

                    found = True
                    closed.append([point, g + h, g, h, expended_point])
                    visited.append(point)
                    expended_point = point
                    break


            
            if found == True:
                break

            

            minimum_index = find_minumum(open)

            if minimum_index == -1:
                print("didn't find endpoint")
                return path
        
            closed.append(open[minimum_index])
            expended_point = open[minimum_index][0]
            expended_g = open[minimum_index][2]
            del open[minimum_index]
        
        index = len(closed)-1

        path_tmp = []

        while True:

            current_point = closed[index][0]
            path_tmp.insert(0, current_point)
            previous_point = closed[index][4]

            if previous_point == start_point:
                path_tmp.insert(0, previous_point)
                break

            index = find_index(closed, previous_point)
        
        
        start_point = expended_point

        if len(path) == 0:
            path += path_tmp
        else:
            path += path_tmp[1:]
    

    return path


    ############################################################################
