def calcular_custos_do_caminho(adj_matrix, path):
    total_toll = 0
    total_fuel = 0
    total_distance = 0

    for i in range(len(path) - 1):
        origem = path[i]
        destino = path[i + 1]
        custos = adj_matrix[origem][destino]

        if custos is None:
            return None, None, None
        
        total_toll += custos['toll']
        total_fuel += custos['fuel']
        total_distance += custos['distance_km']

    return total_toll, total_fuel, total_distance

def encontrar_todos_os_caminhos(adj_matrix, start_city, end_city, path=None, limite=3):
    if path is None:
        path = []

    if len(path) > limite:
        return []

    path = path + [start_city]

    if start_city == end_city:
        return [path]

    if start_city not in adj_matrix:
        return []

    paths = []

    for city in adj_matrix[start_city].keys():
        if city not in path:
            newpaths = encontrar_todos_os_caminhos(adj_matrix, city, end_city, path, limite)
            for newpath in newpaths:
                paths.append(newpath)

    return paths
