import pandas as pd
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import igraph as ig
import leidenalg

# Load facilities dataset
data = pd.read_csv("../dataset/facilities.csv")

coords = data[["lat", "lon"]]

# Build KNN model
knn = NearestNeighbors(n_neighbors=6)
knn.fit(coords)

distances, indices = knn.kneighbors(coords)

# Create graph
G = nx.Graph()

for i in range(len(indices)):
    for j in indices[i]:

        if i != j:
            G.add_edge(i, j)

# Convert NetworkX graph to igraph
g = ig.Graph.TupleList(G.edges(), directed=False)

# Run Leiden clustering
partition = leidenalg.find_partition(
    g,
    leidenalg.ModularityVertexPartition
)

clusters = partition.membership

# Assign cluster ID
data["cluster"] = clusters


# Function to return cluster data
def get_cluster_data():
    return data