import osmnx as ox

ox.settings.timeout = 180              
ox.settings.use_cache = True           
ox.settings.log_console = True         

def load_graph(center_point=(28.6129, 77.2295), distance=3000):
    """
    Downloads road network from OpenStreetMap data around a central GPS point.

    :param center_point: Tuple of (lat, lon)
    :param distance: Distance in meters to cover around the point
    :return: Graph object (networkx.MultiDiGraph)
    """
    print(f"📍 Downloading map within {distance}m of coordinates: {center_point}")
    G = ox.graph_from_point(center_point, dist=distance, network_type='drive')
    return G

def get_nearest_node(G, address):
    """
    Finds the nearest node in the graph to a given address.

    :param G: Road network graph
    :param address: Address string like "Red Fort, Delhi"
    :return: Nearest graph node ID
    """
    try:
        lat, lon = ox.geocode(address)
        node = ox.nearest_nodes(G, lon, lat)
        print(f"✅ Nearest node to '{address}' found: {node}")
        return node
    except Exception as e:
        print(f"❌ Error finding node for '{address}': {e}")
        return None