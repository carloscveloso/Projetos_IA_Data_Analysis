import heapq

def heuristica(nodo, goal):
    return 0  

def A_estrela(graph, start, goal):
    open_set = [(0, start)] 
    came_from = {}           
    cost_so_far = {start: 0}  
    
    while open_set:
        current_cost, current = heapq.heappop(open_set)  

        if current == goal:  
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            path.reverse()
            return path, cost_so_far[goal]

        for neighbor, weight in graph.get(current, []):
            new_cost = cost_so_far[current] + weight  
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristica(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))  
                came_from[neighbor] = current  

    return None, float('inf')  