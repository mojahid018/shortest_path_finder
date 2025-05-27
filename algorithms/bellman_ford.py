import networkx as nx

def bellman_ford_path(G, source, target):
    try:
        path = nx.bellman_ford_path(G, source, target, weight='length')
        return path
    except nx.NetworkXNoPath:
        return None
    except nx.NetworkXUnbounded:
        print("Negative weight cycle detected!")
        return None