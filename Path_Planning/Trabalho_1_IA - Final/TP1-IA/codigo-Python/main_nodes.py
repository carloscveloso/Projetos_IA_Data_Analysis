from algoritmos_grafo_8nodos.AStar_8nodos import A_estrela
from algoritmos_grafo_8nodos.DynamicAStar_8nodos import DynamicAStar
from algoritmos_grafo_8nodos.AnytimeDStar_8nodos import AnytimeDStar
from importar_grafo_8nodos import import_graph

def main_nodes():    
    graph = import_graph('grafo.csv')

    print("\n=== Escolha o Algoritmo ===")
    print("1 - A*")
    print("2 - Dynamic A*")
    print("3 - Anytime D*")

    escolha = input("Digite o número do algoritmo: ").strip()
    inicio = input("Digite o nodo inicial: ").strip().upper()
    fim = input("Digite o nodo final: ").strip().upper()

    if escolha == "1":
        caminho, custo = A_estrela(graph, inicio, fim)
    elif escolha == "2":
        caminho, custo = DynamicAStar(graph, inicio, fim)
    elif escolha == "3":
        caminho, custo = AnytimeDStar(graph, inicio, fim)
    else:
        print("Opção inválida!")
        return

    if caminho:
        print(f"\nCaminho encontrado: {' -> '.join(caminho)}")
        print(f"Custo total: {custo}")
    else:
        print("\nNenhum caminho encontrado.")


if __name__ == "__main__":
    main_nodes()