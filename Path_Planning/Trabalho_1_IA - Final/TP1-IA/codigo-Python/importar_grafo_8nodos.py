import csv

graph = {
    'A': [('B', 5), ('F', 3)],
    'B': [('A', 5), ('C', 2), ('G', 3)],
    'C': [('B', 2), ('D', 6), ('H', 10)],
    'D': [('C', 6), ('E', 3)],
    'E': [('D', 3), ('F', 8), ('H', 5)],
    'F': [('A', 3), ('E', 8), ('G', 7)],
    'G': [('B', 3), ('F', 5), ('H', 2)],
    'H': [('C', 3), ('E', 5), ('G', 2)]
}

csv_file = 'grafo.csv'


def salvar_grafo_em_csv(graph, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(['source', 'target', 'weight'])  

        for origem, conexoes in graph.items():
            for destino, peso in conexoes:
                escritor.writerow([origem, destino, peso])


def import_graph(filename):
    graph = {}

    with open(filename, mode='r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor) 

        for linha in leitor:
            origem, destino, peso = linha
            peso = int(peso)

            if origem not in graph:
                graph[origem] = []
            graph[origem].append((destino, peso))

    return graph


salvar_grafo_em_csv(graph, csv_file)
print(f"Grafo salvo em {csv_file}!")

novo_grafo = import_graph(csv_file)
print("Grafo importado do CSV:")
print(novo_grafo)