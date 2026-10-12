from collections import deque

class A_estrela:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
        
    def get_neighbors(self, city):
         # Verifica se a cidade está no dicionário e retorna seus vizinhos
        if city not in self.adjacency_matrix:
            print(f"Erro: cidade {city} não encontrada no grafo.")
            return []

        # Retorna os vizinhos (cidade destino, atributos)
        return [(neighbor, costs) for neighbor, costs in self.adjacency_matrix[city].items()]
    
    def h(self, city):
        return 1  

    def a_star_algorithm(self, start_city, goal_city):
        open_list = set([start_city])
        closed_list = set([])
        parents = {start_city: start_city}
        g_toll = {start_city: 0}
        g_fuel = {start_city: 0}
        g_distance_km = {start_city: 0}

        def total_cost(city):
            return g_toll[city] + g_fuel[city] + g_distance_km[city]


        while open_list:
            n = None

            for city in open_list:
                if n is None or (g_toll[city] + self.h(city)) < (g_toll[n] + self.h(n)):
                    n = city

            if n is None:
                print('Caminho não encontrado!')
                return None, float('inf'), float('inf'), float('inf')

            if n == goal_city:
                path = []
                total_toll = g_toll[n]
                total_fuel = g_fuel[n]
                total_distance_km = g_distance_km[n]

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_city)
                path.reverse()

                total_cost = total_toll + total_fuel + total_distance_km

                return path, total_toll, total_fuel, total_distance_km, total_cost

            for neighbor, costs in self.get_neighbors(n):
                toll, fuel, distance_km = costs['toll'], costs['fuel'], costs['distance_km']
                if neighbor not in open_list and neighbor not in closed_list:
                    open_list.add(neighbor)
                    parents[neighbor] = n
                    
                    g_toll[neighbor] = g_toll[n] + toll
                    g_fuel[neighbor] = g_fuel[n] + fuel
                    g_distance_km[neighbor] = g_distance_km[n] + distance_km
                else:
                    # Verifica se é um caminho mais barato
                    if total_cost(neighbor) > total_cost(n) + toll + fuel + distance_km:
                        g_toll[neighbor] = g_toll[n] + toll
                        g_fuel[neighbor] = g_fuel[n] + fuel
                        g_distance_km[neighbor] = g_distance_km[n] + distance_km
                        parents[neighbor] = n
                        
                        if neighbor in closed_list:
                            closed_list.remove(neighbor)
                            open_list.add(neighbor)

            open_list.remove(n)
            closed_list.add(n)

        print('Caminho não encontrado!')
        return None, float('inf'), float('inf'), float('inf')
               