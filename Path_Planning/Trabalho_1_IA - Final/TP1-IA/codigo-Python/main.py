import os
import pandas as pd
import numpy as np
from algoritmos.aStar import A_estrela
from algoritmos.dynamic_aStar import DynamicAStar
from algoritmos.anytime_DStar import AnytimeDStar
from algoritmos.allPaths import calcular_custos_do_caminho, encontrar_todos_os_caminhos
from importar_grafo import importar_grafo

def main():
    csv_file = "cities_nodes_special.csv"
    print(f"Procurando o ficheiro no caminho: {os.path.abspath(csv_file)}")

    if not os.path.exists(csv_file):
        print(f"Erro ao abrir o ficheiro {csv_file}")
        return
    
    adj_matrix, cities = importar_grafo(csv_file)

    print("\nEscolha o algoritmo: ")
    print("1 - A*")
    print("2 - Dynamic A*")
    print("3 - Anytime D*")
    print("4 - All Paths")

    algoritmo = input("Digite o número do algoritmo desejado: ").strip()

    print("\nLista de cidades disponíveis: ")
    for i, city in enumerate(sorted(cities)):
        print(f"{i}: {city}")


    try:
        start_index = int(input("Escolha o número da cidade de origem: ").strip())
        end_index = int(input("Escolha o número da cidade de destino: ").strip())

        # Verificar se os índices estão dentro do intervalo válido
        if start_index < 0 or start_index >= len(cities) or end_index < 0 or end_index >= len(cities):
            print("Índice inválido. Por favor, escolha um número dentro da lista de cidades.")
            return

        start_city = cities[start_index]
        end_city = cities[end_index]
        
    except ValueError:
        print("Por favor, insira um número válido para as cidades.")
        return
    
    resultado = None

    if algoritmo == "1":
        algoritmo_escolhido = A_estrela(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.a_star_algorithm(start_city, end_city)
    
    elif algoritmo == "2":
        algoritmo_escolhido = DynamicAStar(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.find_path(start_city, end_city)
    
    elif algoritmo == "3":
        algoritmo_escolhido = AnytimeDStar(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.find_path(start_city, end_city)

    elif algoritmo == "4":
        print("\nA procurar todos os caminhos possíveis... isto pode demorar um pouco.")
        
        caminhos_encontrados = encontrar_todos_os_caminhos(adj_matrix, start_city, end_city)

        print(f"\nNúmero total de caminhos encontrados: {len(caminhos_encontrados)}")

        if not caminhos_encontrados:
            print(f"\nNenhum caminho encontrado entre {start_city} e {end_city}.")
            return

        todos_os_custos = []
        for caminho in caminhos_encontrados:
            portagens, combustivel, distancia = calcular_custos_do_caminho(adj_matrix, caminho)
            if portagens is not None:
                todos_os_custos.append((caminho, portagens, combustivel, distancia))

        if not todos_os_custos:
            print(f"\nTodos os caminhos encontrados estavam corrompidos ou inválidos.")
            return

        # Normalização das 3 variáveis
        max_toll = max(x[1] for x in todos_os_custos)
        max_fuel = max(x[2] for x in todos_os_custos)
        max_distance = max(x[3] for x in todos_os_custos)

        caminhos_com_score = []
        for caminho, port, comb, dist in todos_os_custos:
            norm_toll = port / max_toll if max_toll else 0
            norm_fuel = comb / max_fuel if max_fuel else 0
            norm_distance = dist / max_distance if max_distance else 0

            score = norm_toll + norm_fuel + norm_distance
            caminhos_com_score.append((caminho, port, comb, dist, score))

        # Ordenar pelo menor score (melhor equilíbrio entre as 3 variáveis)
        caminhos_com_score.sort(key=lambda x: x[4])

        print(f"\nTop 10 caminhos mais equilibrados (minimizando portagens, combustível e distância):")
        for i, (caminho, port, comb, dist, score) in enumerate(caminhos_com_score[:10], 1):
            print(f"\n{i}) {' -> '.join(caminho)}")
            print(f"Portagens: {port:.2f} | Combustível: {comb:.2f} | Distância: {dist:.2f} km | Score normalizado: {score:.4f}")

        melhor_caminho = caminhos_com_score[0]
        caminho, port, comb, dist, score = melhor_caminho

        print("\nMelhor caminho absoluto que minimiza as 3 variáveis:")
        print(f"{' -> '.join(caminho)}")
        print(f"Portagens: {port:.2f} | Combustível: {comb:.2f} | Distância: {dist:.2f} km | Score normalizado: {score:.4f}")
    
    else:
        print("Opção inválida! Escolha 1, 2, 3 ou 4.")
        return

    if algoritmo == "1":  # A*
        path, total_toll, total_fuel, total_distance, total_cost = resultado
        print(f"\nCaminho encontrado: {path}")
        print(f"Custo total de portagens: {total_toll}")
        print(f"Custo total de combustível: {total_fuel}")
        print(f"Distância total: {total_distance}")
        print(f"Custo total (portagens + combustível + distância): {total_cost}")


    elif algoritmo == "2":  # Dynamic A*
        path, total_toll, total_fuel, total_distance, total_cost = resultado
        print(f"\nCaminho encontrado: {path}")
        print(f"Custo total de portagens: {total_toll}")
        print(f"Custo total de combustível: {total_fuel}")
        print(f"Distância total: {total_distance}")
        print(f"Custo total (portagens + combustível + distância): {total_cost}")


    elif algoritmo == "3":  # Anytime D*
        path, total_toll, total_fuel, total_distance, total_cost = resultado
        print(f"\nCaminho encontrado: {path}")
        print(f"Custo total de portagens: {total_toll}")
        print(f"Custo total de combustível: {total_fuel}")
        print(f"Distância total: {total_distance}")
        print(f"Custo total (portagens + combustível + distância): {total_cost}")

if __name__ == "__main__":
    main()
