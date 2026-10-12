import pandas as pd
import numpy as np

def importar_grafo_viana(csv_file):
    # Carrega o CSV
    df = pd.read_csv(csv_file, delimiter=',')
    df.columns = df.columns.str.strip()

    # Remove espaços em branco
    df["origin"] = df["origin"].astype(str).str.strip()
    df["destination"] = df["destination"].astype(str).str.strip()

    # Converte para float os valores relevantes
    df["distance_meters"] = pd.to_numeric(df["distance_meters"], errors='coerce').astype(np.float64)
    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors='coerce').astype(np.float64)
    df["unlevel_percent"] = pd.to_numeric(df["unlevel_percent"], errors='coerce').astype(np.float64)
    df["intersect_lon"] = pd.to_numeric(df["intersect_lon"], errors='coerce').astype(np.float64)
    df["intersect_lat"] = pd.to_numeric(df["intersect_lat"], errors='coerce').astype(np.float64)

    df = df.fillna({
        "distance_meters": np.nan,
        "duration_minutes": np.nan,
        "unlevel_percent": np.nan,
        "intersect_lon": np.nan,
        "intersect_lat": np.nan
    })

    # Criar lista única de nós
    nodes = sorted(set(df["origin"].tolist() + df["destination"].tolist()))
    
    # Inicializar a matriz de adjacência
    adj_matrix = {}

    # Preencher a matriz
    for _, row in df.iterrows():
        origin = row["origin"]
        destination = row["destination"]
        distance = row["distance_meters"]
        duration = row["duration_minutes"]
        unlevel = row["unlevel_percent"]
        lon = row["intersect_lon"]
        lat = row["intersect_lat"]

        edge_data = {
            'distance_meters': distance,
            'duration_minutes': duration,
            'unlevel_percent': unlevel,
            'intersect_lon': lon,
            'intersect_lat': lat
        }

        if origin not in adj_matrix:
            adj_matrix[origin] = {}

        adj_matrix[origin][destination] = edge_data

        # Assumindo grafo não-direcionado
        if destination not in adj_matrix:
            adj_matrix[destination] = {}

        adj_matrix[destination][origin] = edge_data

    return adj_matrix, nodes