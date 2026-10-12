def calcular_custos_do_caminho_viana(adj_matrix, path):
    total_distance = 0
    total_duration = 0
    total_unlevel = 0

    for i in range(len(path) - 1):
        origem = path[i]
        destino = path[i + 1]

        if destino not in adj_matrix.get(origem, {}):
            return None, None, None

        custos = adj_matrix[origem][destino]
        total_distance += custos.get('distance_meters', 0)
        total_duration += custos.get('duration_minutes', 0)
        total_unlevel += custos.get('unlevel_percent', 0)

    return total_distance, total_duration, total_unlevel

def encontrar_todos_os_caminhos_viana(adj_matrix, start_city, end_city, path=None, limite=10):
    if path is None:
        path = []

    if len(path) > limite:
        return []

    path = path + [start_city]

    if start_city == end_city:
        return [path]

    if start_city not in adj_matrix:
        print(f"{start_city} não está no grafo.")
        return []

    paths = []

    for vizinho in adj_matrix[start_city]:
        if vizinho not in path:
            novos_caminhos = encontrar_todos_os_caminhos_viana(adj_matrix, vizinho, end_city, path, limite)
            paths.extend(novos_caminhos)

    return paths