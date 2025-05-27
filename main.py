import osmnx as ox
import matplotlib.pyplot as plt

# ✅ Custom imports
from utils.graph_loader import load_graph
from utils.map_generator import create_folium_map
from algorithms.bfs import bfs_path
from algorithms.dfs import dfs_path
from algorithms.dijkstra import dijkstra_path
from algorithms.bellman_ford import bellman_ford_path

# ⛳ GPS coordinates for India Gate and Red Fort
source_coords = (28.6129, 77.2295)  # India Gate
target_coords = (28.5245, 77.1855)  # Red Fort

# ✅ Step 1: Load OSM graph around center point (India Gate area)
center_point = (28.6300, 77.2350)  # Central point between both
distance = 15000  # Radius (in meters)

G = load_graph(center_point=center_point, distance=distance)

# ✅ Step 2: Convert coordinates to nearest graph nodes
print("\n📍 Finding nearest nodes to given coordinates...")
source = ox.nearest_nodes(G, source_coords[1], source_coords[0])
target = ox.nearest_nodes(G, target_coords[1], target_coords[0])
print(f"✅ Source node: {source}, Target node: {target}")

# ✅ Step 3: Run algorithms
print("\n🔁 Running algorithms...\n")

paths = {
    "Dijkstra": dijkstra_path(G, source, target),
    "Bellman-Ford": bellman_ford_path(G, source, target),
    "BFS": bfs_path(G, source, target),
    "DFS": dfs_path(G, source, target)
}

# ✅ Step 4: Print results
print("📊 Results:\n")
for algo, path in paths.items():
    if path:
        total_length = sum(ox.utils_graph.get_route_edge_attributes(G, path, 'length'))
        print(f"✅ {algo}: {round(total_length / 1000, 2)} km | Nodes: {len(path)}")
    else:
        print(f"❌ {algo}: Path not found.")

# ✅ Step 5: Plot the Dijkstra path (best one for real road)
if paths["Dijkstra"]:
    print("\n🗺️  Plotting route using Dijkstra...")
    ox.plot_graph_route(G, paths["Dijkstra"], route_linewidth=4, node_size=0, bgcolor='k')
else:
    print("\n⚠️  Dijkstra path unavailable to plot.")