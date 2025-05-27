import networkx as nx

def dijkstra_path(G, source, target):
    try:
        path = nx.shortest_path(G, source, target, weight='length')
        return path
    except nx.NetworkXNoPath:
        return None