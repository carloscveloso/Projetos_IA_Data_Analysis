import heapq
import math
import numpy as np

class AnytimeDStar:
    def __init__(self, adjacency_matrix, cities, 
                 unlevel_weight=1.0, duration_weight=1.0, distance_weight=1.0, epsilon=0.5):
        self.adjacency_matrix = adjacency_matrix
        self.cities = cities
        self.unlevel_weight = unlevel_weight
        self.duration_weight = duration_weight
        self.distance_weight = distance_weight
        self.epsilon = epsilon
        self.city_coords = self._extract_coords()

    def _extract_coords(self):
        coords = {}
        for city in self.cities:
            neighbors = self.adjacency_matrix.get(city, {})
            for neighbor, data in neighbors.items():
                lat = data.get('intersect_lat')
                lon = data.get('intersect_lon')
                if lat is not None and lon is not None and not np.isnan(lat) and not np.isnan(lon):
                    coords[city] = (lat, lon)
                    break
        return coords

    def heuristic(self, city1, city2):
        coord1 = self.city_coords.get(city1)
        coord2 = self.city_coords.get(city2)

        if not coord1 or not coord2:
            return 0

        lat1, lon1 = coord1
        lat2, lon2 = coord2
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def calculate_cost(self, costs):
        return (self.unlevel_weight * costs.get('unlevel_percent', 0) +
                self.duration_weight * costs.get('duration_minutes', 0) +
                self.distance_weight * costs.get('distance_meters', 0))

    def update_edge_costs(self, city_a, city_b, new_costs):
        for key in ['unlevel_percent', 'duration_minutes', 'distance_meters']:
            if key in new_costs:
                self.adjacency_matrix[city_a][city_b][key] = new_costs[key]
                self.adjacency_matrix[city_b][city_a][key] = new_costs[key]

    def find_path(self, start_city, end_city):
        open_list = []
        heapq.heappush(open_list, (0, start_city))
        came_from = {}
        g_score = {city: float('inf') for city in self.cities}
        f_score = {city: float('inf') for city in self.cities}
        g_score[start_city] = 0
        f_score[start_city] = self.epsilon * self.heuristic(start_city, end_city)

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == end_city:
                return self.reconstruct_path(came_from, current)

            for neighbor, costs in self.adjacency_matrix.get(current, {}).items():
                tentative_g = g_score[current] + self.calculate_cost(costs)

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.epsilon * self.heuristic(neighbor, end_city)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None

    def reconstruct_path(self, came_from, current):
        path = [current]
        total_unlevel = 0
        total_duration = 0
        total_distance = 0

        while current in came_from:
            prev = came_from[current]
            costs = self.adjacency_matrix[prev][current]
            total_unlevel += costs.get('unlevel_percent', 0)
            total_duration += costs.get('duration_minutes', 0)
            total_distance += costs.get('distance_meters', 0)
            path.append(prev)
            current = prev

        path.reverse()
        total_cost = total_unlevel + total_duration + total_distance
        return path, total_distance, total_duration, total_unlevel, total_cost

    def refine_path(self, start_city, end_city, min_epsilon=1.0, step=0.5):
        current_epsilon = self.epsilon
        best_path = None

        while current_epsilon >= min_epsilon:
            self.epsilon = current_epsilon
            path_info = self.find_path(start_city, end_city)
            if path_info:
                best_path = path_info
            current_epsilon -= step

        return best_path