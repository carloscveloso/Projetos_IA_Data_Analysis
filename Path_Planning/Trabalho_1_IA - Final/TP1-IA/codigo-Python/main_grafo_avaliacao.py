import os
import pandas as pd
import numpy as np
from algoritmos_viana.aStarViana import A_estrela
from algoritmos_viana.dynamic_aStarViana import DynamicAStar
from algoritmos_viana.anytime_DStarViana import AnytimeDStar
from algoritmos_viana.allPathsViana import calcular_custos_do_caminho_viana, encontrar_todos_os_caminhos_viana
from Importar_grafo_avaliacao import importar_grafo_viana

def main():
    csv_file = "viana_streets_network_named.csv"
    print(f"Procurando o ficheiro no caminho: {os.path.abspath(csv_file)}")

    if not os.path.exists(csv_file):
        print(f"Erro ao abrir o ficheiro {csv_file}")
        return

    adj_matrix, cities = importar_grafo_viana(csv_file)

    while True:
        print("\nEscolha o algoritmo: ")
        print("1 - A*")
        print("2 - Dynamic A*")
        print("3 - Anytime D*")
        print("4 - All Paths")
        print("0 - Sair")

        algoritmo = input("Digite o número do algoritmo desejado: ").strip()

        if algoritmo == "0":
            print("Programa terminado.")
            break

        print("\nLista de nós disponíveis: ")
        for i, city in enumerate(sorted(cities)):
            print(f"{i}: {city}")

        try:
            start_index = int(input("Escolha o número do nó de origem: ").strip())
            end_index = int(input("Escolha o número do nó de destino: ").strip())

            if start_index < 0 or start_index >= len(cities) or end_index < 0 or end_index >= len(cities):
                print("Índice inválido. Por favor, escolha um número dentro da lista.")
                continue

            start_city = cities[start_index]
            end_city = cities[end_index]

        except ValueError:
            print("Por favor, insira um número válido.")
            continue

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
            print("\nA procurar todos os caminhos possíveis... isto pode demorar.")
            caminhos_encontrados = encontrar_todos_os_caminhos_viana(adj_matrix, start_city, end_city)

            print(f"\nNúmero total de caminhos encontrados: {len(caminhos_encontrados)}")

            if not caminhos_encontrados:
                print(f"\nNenhum caminho encontrado entre {start_city} e {end_city}.")
                continue

            todos_os_custos = []
            for caminho in caminhos_encontrados:
                distancia, duracao, inclinacao = calcular_custos_do_caminho_viana(adj_matrix, caminho)
                if distancia is not None:
                    todos_os_custos.append((caminho, distancia, duracao, inclinacao))

            if not todos_os_custos:
                print("\nTodos os caminhos estavam corrompidos ou inválidos.")
                continue

            max_dist = max(x[1] for x in todos_os_custos)
            max_dur = max(x[2] for x in todos_os_custos)
            max_inc = max(x[3] for x in todos_os_custos)

            caminhos_com_score = []
            for caminho, dist, dur, inc in todos_os_custos:
                norm_dist = dist / max_dist if max_dist else 0
                norm_dur = dur / max_dur if max_dur else 0
                norm_inc = inc / max_inc if max_inc else 0

                score = norm_dist + norm_dur + norm_inc
                caminhos_com_score.append((caminho, dist, dur, inc, score))

            caminhos_com_score.sort(key=lambda x: x[4])

            print("\nTop 10 caminhos mais equilibrados (minimizando distância, duração e inclinação):")
            for i, (caminho, dist, dur, inc, score) in enumerate(caminhos_com_score[:10], 1):
                print(f"\n{i}) {' -> '.join(caminho)}")
                print(f"Distância: {dist:.2f} m | Duração: {dur:.2f} min | Inclinação: {inc:.2f}% | Score normalizado: {score:.4f}")

            melhor_caminho = caminhos_com_score[0]
            caminho, dist, dur, inc, score = melhor_caminho

            print("\nMelhor caminho absoluto:")
            print(f"{' -> '.join(caminho)}")
            print(f"Distância: {dist:.2f} m | Duração: {dur:.2f} min | Inclinação: {inc:.2f}% | Score normalizado: {score:.4f}")
            continue

        else:
            print("Opção inválida! Escolha 0, 1, 2, 3 ou 4.")
            continue

        if resultado:
            path, total_dist, total_dur, total_inc, total_cost = resultado
            print(f"\nCaminho encontrado: {path}")
            print(f"Distância total: {total_dist:.2f} m")
            print(f"Duração total: {total_dur:.2f} min")
            print(f"Inclinação total: {total_inc:.2f}%")
            print(f"Custo total (soma normalizada): {total_cost:.4f}")

if __name__ == "__main__":
    main()