import heapq

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

    def heuristic(self, a, b):
        if a in self.graph and b in self.graph[a]:
            return self.graph[a][b].get('distance_km', float('inf'))
        return float('inf')

    def update_graph(self, origin, destination, new_costs):
        if origin in self.graph and destination in self.graph[origin]:
            for key in ['toll', 'fuel', 'distance_km']:
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
        cost_toll = self.cost_updates.get((from_city, to_city, 'toll'), edge.get('toll', 0))
        cost_fuel = self.cost_updates.get((from_city, to_city, 'fuel'), edge.get('fuel', 0))
        cost_distance = self.cost_updates.get((from_city, to_city, 'distance_km'), edge.get('distance_km', float('inf')))
        return cost_toll + cost_fuel + cost_distance

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
        total_toll = total_fuel = total_distance = 0.0

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
                return None  # Sem caminho

            total_toll += best_edge.get('toll', 0)
            total_fuel += best_edge.get('fuel', 0)
            total_distance += best_edge.get('distance_km', 0)
            current = next_city
            path.append(current)

        total_cost = total_toll + total_fuel + total_distance
        
        return path, total_toll, total_fuel, total_distance, total_cost