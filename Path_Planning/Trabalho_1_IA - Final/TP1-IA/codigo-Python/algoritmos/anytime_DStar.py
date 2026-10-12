import heapq

class AnytimeDStar:
    def __init__(self, adjacency_matrix, cities, toll_weight=1.0, fuel_weight=1.0, distance_weight=1.0, epsilon=0.5):
        self.adjacency_matrix = adjacency_matrix
        self.cities = cities
        self.toll_weight = toll_weight
        self.fuel_weight = fuel_weight
        self.distance_weight = distance_weight
        self.epsilon = epsilon  

    def heuristic(self, city1, city2):
        if city1 in self.adjacency_matrix and city2 in self.adjacency_matrix[city1]:
            return self.adjacency_matrix[city1][city2].get('distance_km', 0)
        return 0

    def calculate_cost(self, costs):
        return (self.toll_weight * costs['toll'] +
                self.fuel_weight * costs['fuel'] +
                self.distance_weight * costs['distance_km'])

    def update_edge_costs(self, city_a, city_b, new_costs):
        for key in ['toll', 'fuel', 'distance_km']:
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
        total_toll = 0
        total_fuel = 0
        total_distance = 0

        while current in came_from:
            prev = came_from[current]
            costs = self.adjacency_matrix[prev][current]
            total_toll += costs['toll']
            total_fuel += costs['fuel']
            total_distance += costs['distance_km']
            path.append(prev)
            current = prev

        path.reverse()
        total_cost = total_toll + total_fuel + total_distance
        return path, total_toll, total_fuel, total_distance, total_cost

    def refine_path(self, start_city, end_city, min_epsilon=1.0, step=0.5):
        """Refina o caminho gradualmente reduzindo o epsilon."""
        current_epsilon = self.epsilon
        best_path = None

        while current_epsilon >= min_epsilon:
            self.epsilon = current_epsilon
            path_info = self.find_path(start_city, end_city)
            if path_info:
                best_path = path_info
            current_epsilon -= step

        return best_path