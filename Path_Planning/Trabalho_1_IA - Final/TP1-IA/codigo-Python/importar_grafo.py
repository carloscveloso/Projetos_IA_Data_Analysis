import pandas as pd
import numpy as np

# Função para importar o CSV para uma matriz de adjacência com três variáveis
def importar_grafo(csv_file):
    # Carregar o CSV (ajuste conforme necessário se o delimitador for diferente)
    df = pd.read_csv(csv_file, delimiter=',')
    df.columns = df.columns.str.strip()

    df["origin_city"] = df["origin_city"].str.strip()
    df["destination_city"] = df["destination_city"].str.strip()

    df["toll"] = pd.to_numeric(df["toll"], errors='coerce').astype(np.float64)
    df["fuel"] = pd.to_numeric(df["fuel"], errors='coerce').astype(np.float64)
    df["distance_km"] = pd.to_numeric(df["distance_km"], errors='coerce').astype(np.float64)

    df = df.fillna({
        "toll": np.nan,
        "fuel": np.nan,
        "distance_km": np.nan
    })

    # Criar lista única de cidades
    cities = sorted(set(df["origin_city"].tolist() + df["destination_city"].tolist()))
    
     # Inicializar a matriz de adjacência
    adj_matrix = {}
    
    
    # Preencher a matriz de adjacência com base nos dados
    for _, row in df.iterrows():
        origin_city = row["origin_city"]
        destination_city = row["destination_city"]
        toll = row["toll"]
        fuel = row["fuel"]
        distance_km = row["distance_km"]

        # Verifica se a cidade de origem já está no dicionário
        if origin_city not in adj_matrix:
            adj_matrix[origin_city] = {}

        # Adiciona o destino com os valores correspondentes
        adj_matrix[origin_city][destination_city] = {
            'toll': toll,
            'fuel': fuel,
            'distance_km': distance_km
        }

        # Adicionar também a ligação inversa para a simetria
        if destination_city not in adj_matrix:
            adj_matrix[destination_city] = {}

        adj_matrix[destination_city][origin_city] = {
            'toll': toll,
            'fuel': fuel,
            'distance_km': distance_km
        }


    return adj_matrix, cities