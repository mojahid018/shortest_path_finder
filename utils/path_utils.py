import osmnx as ox

def calculate_path_length(G, path):
    """
    Calculate the total length of a path using the new route_to_gdf method
    """
    if not path:
        return 0
    try:
        # Convert route to GeoDataFrame and sum the lengths
        route_gdf = ox.utils_graph.route_to_gdf(G, path)
        return route_gdf['length'].sum()
    except Exception as e:
        print(f"Error calculating path length: {e}")
        return 0