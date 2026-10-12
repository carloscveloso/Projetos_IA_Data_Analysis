import heapq
import math
import numpy as np

class DynamicAStar:
    def __init__(self, adjacency_matrix, cities):
        self.graph = adjacency_matrix
        self.cities = cities
        self.g = {}
        self.rhs = {}
        self.U = []
        self.km = 0
        self.goal = None
        self.cost_updates = {}
        self.city_coords = self._extract_coords()

    def _extract_coords(self):
        coords = {}
        for city in self.cities:
            neighbors = self.graph.get(city, {})
            for neighbor, data in neighbors.items():
                lat = data.get('intersect_lat')
                lon = data.get('intersect_lon')
                if lat is not None and lon is not None and not np.isnan(lat) and not np.isnan(lon):
                    coords[city] = (lat, lon)
                    break
        return coords

    def heuristic(self, a, b):
        coord1 = self.city_coords.get(a)
        coord2 = self.city_coords.get(b)
        if not coord1 or not coord2:
            return 0  

        lat1, lon1 = coord1
        lat2, lon2 = coord2
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371000  
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)

        a = math.sin(d_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def update_graph(self, origin, destination, new_costs):
        if origin in self.graph and destination in self.graph[origin]:
            for key in ['unlevel_percent', 'duration_minutes', 'distance_meters']:
                if key in new_costs:
                    self.graph[origin][destination][key] = new_costs[key]
                    self.graph[destination][origin][key] = new_costs[key]
                    self.cost_updates[(origin, destination, key)] = new_costs[key]
                    self.cost_updates[(destination, origin, key)] = new_costs[key]

    def key(self, city):
        min_g_rhs = min(self.g.get(city, float('inf')), self.rhs.get(city, float('inf')))
        return (min_g_rhs + self.heuristic(city, self.goal), min_g_rhs)

    def update_vertex(self, city):
        if city != self.goal:
            min_rhs = float('inf')
            for neighbor in self.graph.get(city, {}):
                cost = self.get_cost(city, neighbor)
                min_rhs = min(min_rhs, self.g.get(neighbor, float('inf')) + cost)
            self.rhs[city] = min_rhs

        for i, (_, c) in enumerate(self.U):
            if c == city:
                self.U.pop(i)
                heapq.heapify(self.U)
                break

        if self.g.get(city, float('inf')) != self.rhs.get(city, float('inf')):
            heapq.heappush(self.U, (self.key(city), city))

    def compute_shortest_path(self):
        while self.U:
            k_old, u = heapq.heappop(self.U)
            g_u = self.g.get(u, float('inf'))
            rhs_u = self.rhs.get(u, float('inf'))

            if g_u > rhs_u:
                self.g[u] = rhs_u
                for neighbor in self.graph.get(u, {}):
                    self.update_vertex(neighbor)
            else:
                self.g[u] = float('inf')
                self.update_vertex(u)
                for neighbor in self.graph.get(u, {}):
                    self.update_vertex(neighbor)

    def get_cost(self, from_city, to_city):
        edge = self.graph[from_city][to_city]
        cost_unlevel = self.cost_updates.get((from_city, to_city, 'unlevel_percent'), edge.get('unlevel_percent', 0))
        cost_duration = self.cost_updates.get((from_city, to_city, 'duration_minutes'), edge.get('duration_minutes', 0))
        cost_distance = self.cost_updates.get((from_city, to_city, 'distance_meters'), edge.get('distance_meters', float('inf')))
        return cost_unlevel + cost_duration + cost_distance

    def find_path(self, start, goal):
        self.goal = goal
        self.g = {city: float('inf') for city in self.cities}
        self.rhs = {city: float('inf') for city in self.cities}
        self.rhs[goal] = 0
        self.U = []
        heapq.heappush(self.U, (self.key(goal), goal))
        self.compute_shortest_path()
        return self.extract_path(start)

    def extract_path(self, start):
        current = start
        path = [current]
        total_unlevel = total_duration = total_distance = 0.0

        while current != self.goal:
            min_cost = float('inf')
            next_city = None

            for neighbor in self.graph.get(current, {}):
                cost = self.get_cost(current, neighbor) + self.g.get(neighbor, float('inf'))
                if cost < min_cost:
                    min_cost = cost
                    next_city = neighbor
                    best_edge = self.graph[current][neighbor]

            if next_city is None:
                return None  

            total_unlevel += best_edge.get('unlevel_percent', 0)
            total_duration += best_edge.get('duration_minutes', 0)
            total_distance += best_edge.get('distance_meters', 0)
            current = next_city
            path.append(current)

        total_cost = total_unlevel + total_duration + total_distance
        return path, total_unlevel, total_duration, total_distance, total_cost