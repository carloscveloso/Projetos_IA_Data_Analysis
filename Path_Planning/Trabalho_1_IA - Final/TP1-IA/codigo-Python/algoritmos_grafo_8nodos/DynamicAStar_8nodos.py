import heapq

def DynamicAStar(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))  
    came_from = {}  
    g_score = {start: 0}  
    f_score = {start: heuristica(start, goal)} 

    while open_set:
        _, current = heapq.heappop(open_set)  
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]

        for neighbor, cost in graph.get(current, []):
            tentative_g = g_score[current] + cost  

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristica(neighbor, goal)
                came_from[neighbor] = current
                heapq.heappush(open_set, (f_score[neighbor], neighbor))  

    return None, float('inf')  


def heuristica(nodo, goal):
    return abs(ord(goal[0]) - ord(nodo[0]))  