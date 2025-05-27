import networkx as nx

def bfs_path(G, source, target):
    try:
        path = nx.shortest_path(G, source, target)
        return path
    except nx.NetworkXNoPath:
        return None