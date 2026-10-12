import math
import numpy as np
from collections import deque

class A_estrela:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
        self.city_coords = self._extract_coords()  

    def _extract_coords(self):
        coords = {}
        for city in self.cities:
            neighbors = self.adjacency_matrix.get(city, {})
            for neighbor, data in neighbors.items():
                lat = data.get('intersect_lat')
                lon = data.get('intersect_lon')
                if not np.isnan(lat) and not np.isnan(lon):
                    coords[city] = (lat, lon)
                    break
        return coords

    def get_neighbors(self, city):
        if city not in self.adjacency_matrix:
            print(f"Erro: cidade {city} não encontrada no grafo.")
            return []
        return [(neighbor, costs) for neighbor, costs in self.adjacency_matrix[city].items()]

    def h(self, city, goal_city):
        coord1 = self.city_coords.get(city)
        coord2 = self.city_coords.get(goal_city)

        if not coord1 or not coord2:
            return 0  

        lat1, lon1 = coord1
        lat2, lon2 = coord2
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    def a_star_algorithm(self, start_city, goal_city):
        open_list = set([start_city])
        closed_list = set([])
        parents = {start_city: start_city}

        g_unlevel = {start_city: 0}
        g_duration = {start_city: 0}
        g_distance = {start_city: 0}

        def total_cost(city):
            return g_unlevel[city] + g_duration[city] + g_distance[city]

        while open_list:
            n = None
            for city in open_list:
                if n is None or (total_cost(city) + self.h(city, goal_city)) < (total_cost(n) + self.h(n, goal_city)):
                    n = city

            if n is None:
                print('Caminho não encontrado!')
                return None, float('inf'), float('inf'), float('inf'), float('inf')

            if n == goal_city:
                path = []
                total_unlevel = g_unlevel[n]
                total_duration = g_duration[n]
                total_distance = g_distance[n]

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_city)
                path.reverse()

                total = total_unlevel + total_duration + total_distance
                return path, total_distance, total_duration, total_unlevel, total

            for neighbor, costs in self.get_neighbors(n):
                unlevel = costs.get('unlevel_percent', 0)
                duration = costs.get('duration_minutes', 0)
                distance = costs.get('distance_meters', 0)

                if neighbor not in open_list and neighbor not in closed_list:
                    open_list.add(neighbor)
                    parents[neighbor] = n
                    g_unlevel[neighbor] = g_unlevel[n] + unlevel
                    g_duration[neighbor] = g_duration[n] + duration
                    g_distance[neighbor] = g_distance[n] + distance
                else:
                    if total_cost(neighbor) > total_cost(n) + unlevel + duration + distance:
                        g_unlevel[neighbor] = g_unlevel[n] + unlevel
                        g_duration[neighbor] = g_duration[n] + duration
                        g_distance[neighbor] = g_distance[n] + distance
                        parents[neighbor] = n

                        if neighbor in closed_list:
                            closed_list.remove(neighbor)
                            open_list.add(neighbor)

            open_list.remove(n)
            closed_list.add(n)

        print('Caminho não encontrado!')
        return None, float('inf'), float('inf'), float('inf'), float('inf')