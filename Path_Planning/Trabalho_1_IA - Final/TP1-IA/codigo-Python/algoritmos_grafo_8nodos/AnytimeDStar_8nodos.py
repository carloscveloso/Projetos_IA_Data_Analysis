import heapq
import time

def AnytimeDStar(graph, start, goal, tempo_limite=2.0):
    melhor_caminho = None
    melhor_custo = float('inf')
    inicio_tempo = time.time()
    fator = 1.5  

    while time.time() - inicio_tempo < tempo_limite:
        caminho, custo = busca_heuristica(graph, start, goal, fator)

        if caminho and custo < melhor_custo:
            melhor_caminho = caminho
            melhor_custo = custo
        
        fator *= 0.8  

    return melhor_caminho, melhor_custo

def busca_heuristica(graph, start, goal, fator):
    open_set = []
    heapq.heappush(open_set, (0, start))  
    came_from = {}  
    g_score = {start: 0}  

    def heuristica(nodo):
        return abs(ord(goal[0]) - ord(nodo[0])) * fator  

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
                came_from[neighbor] = current
                priority = tentative_g + heuristica(neighbor)  
                heapq.heappush(open_set, (priority, neighbor))

    return None, float('inf')  