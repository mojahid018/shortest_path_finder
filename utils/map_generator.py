import folium
import osmnx as ox

def create_folium_map(G, path, filename='route_map.html'):
    # Get coordinates of nodes in path
    route_nodes = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]

    # Center point
    center_coords = route_nodes[len(route_nodes)//2]

    # Folium map object
    m = folium.Map(location=center_coords, zoom_start=14)

    # Draw the path
    folium.PolyLine(route_nodes, color="blue", weight=5, opacity=0.8).add_to(m)

    # Add start & end markers
    folium.Marker(route_nodes[0], tooltip='Start', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(route_nodes[-1], tooltip='End', icon=folium.Icon(color='red')).add_to(m)

    # Save map
    m.save(filename)
    print(f"✅ Route map saved to '{filename}'")