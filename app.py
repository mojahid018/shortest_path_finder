import streamlit as st
import osmnx as ox
import folium
import pandas as pd
import time
from algorithms.dijkstra import dijkstra_path
from algorithms.bfs import bfs_path
from algorithms.dfs import dfs_path
from algorithms.bellman_ford import bellman_ford_path

# Page config
st.set_page_config(
    page_title="Shortest Path Finder",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Calculate path length using new method
def calculate_path_length(G, path):
    if not path:
        return 0
    try:
        route_gdf = ox.utils_graph.route_to_gdf(G, path)
        return route_gdf['length'].sum()
    except Exception as e:
        st.warning(f"Warning in length calculation: {e}")
        return 0

# Show map function
def show_map(m):
    """Display the folium map in Streamlit"""
    map_path = "temp_map.html"
    m.save(map_path)
    with open(map_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=500)

# Load Graph (with caching)
@st.cache_data
def load_city_graph():
    try:
        center = (28.6300, 77.2350)  # Delhi center
        G = ox.graph_from_point(center, dist=15000, network_type='drive')
        return G, "Graph loaded successfully! ✅"
    except Exception as e:
        return None, f"Error loading graph: {str(e)} ❌"

# Run algorithm with timing
def run_algorithm(algo_func, G, source, target):
    start_time = time.time()
    path = algo_func(G, source, target)
    end_time = time.time()
    return path, round((end_time - start_time) * 1000, 2)  # time in milliseconds

# Title
st.title("🗺️ Shortest Path Finder")
st.write("Find and compare shortest paths between Delhi landmarks using different algorithms!")

# Load graph
G, load_message = load_city_graph()

if G is None:
    st.error(load_message)
    st.stop()
else:
    st.success(load_message)

# Predefined locations in Delhi
locations = {
    "India Gate": (28.6129, 77.2295),
    "Red Fort": (28.6562, 77.2410),
    "Connaught Place": (28.6315, 77.2167),
    "AIIMS": (28.5672, 77.2100),
    "Raj Ghat": (28.6400, 77.2500),
    "Jama Masjid": (28.6507, 77.2334),
    "Lotus Temple": (28.5535, 77.2588),
    "Qutub Minar": (28.5245, 77.1855)
}

# Location selection
col1, col2 = st.columns(2)
with col1:
    source_label = st.selectbox("📍 Start Location", list(locations.keys()))
with col2:
    target_label = st.selectbox("🎯 End Location", list(locations.keys()), index=1)

# Get nodes
source = ox.nearest_nodes(G, locations[source_label][1], locations[source_label][0])
target = ox.nearest_nodes(G, locations[target_label][1], locations[target_label][0])

# Algorithm selection
algorithms = {
    "Dijkstra": dijkstra_path,
    "Bellman-Ford": bellman_ford_path,
    "BFS": bfs_path,
    "DFS": dfs_path
}

method = st.radio("🔍 Select Algorithm", list(algorithms.keys()))
compare_all = st.checkbox("Compare all algorithms")

if st.button("🚀 Find Path"):
    if source_label == target_label:
        st.error("⚠️ Please select different start and end locations!")
    else:
        with st.spinner("🔍 Finding routes..."):
            if compare_all:
                # Run all algorithms
                results = []
                for algo_name, algo_func in algorithms.items():
                    path, execution_time = run_algorithm(algo_func, G, source, target)
                    if path:
                        length = calculate_path_length(G, path)
                        results.append({
                            'Algorithm': algo_name,
                            'Distance (km)': round(length/1000, 2),
                            'Nodes': len(path),
                            'Time (ms)': execution_time,
                            'Path': path
                        })
                
                # Display comparison table
                if results:
                    st.write("### 📊 Algorithm Comparison")
                    df_results = pd.DataFrame(results).set_index('Algorithm')
                    st.dataframe(df_results.drop('Path', axis=1))
                    
                    # Use Dijkstra's path for visualization
                    best_path = next(r['Path'] for r in results if r['Algorithm'] == 'Dijkstra')
                else:
                    st.error("❌ No paths found!")
                    st.stop()
                
            else:
                # Run single algorithm
                path, execution_time = run_algorithm(algorithms[method], G, source, target)
                if path:
                    length = calculate_path_length(G, path)
                    km = round(length/1000, 2)
                    
                    st.success(f"✅ Path found using {method}!")
                    st.info(f"""
                    📏 Distance: {km} km
                    🔢 Nodes: {len(path)}
                    ⚡ Time: {execution_time} ms
                    """)
                    best_path = path
                else:
                    st.error("❌ No path found!")
                    st.stop()

            # Create map
            route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in best_path]
            m = folium.Map(location=route_coords[0], zoom_start=13)
            
            # Add route line
            folium.PolyLine(
                route_coords,
                weight=5,
                color='blue',
                opacity=0.8
            ).add_to(m)
            
            # Add markers
            folium.Marker(
                route_coords[0],
                popup=source_label,
                icon=folium.Icon(color='green')
            ).add_to(m)
            
            folium.Marker(
                route_coords[-1],
                popup=target_label,
                icon=folium.Icon(color='red')
            ).add_to(m)
            
            # Show map
            show_map(m)

            # Download buttons
            if st.button("📥 Download Route Data"):
                df = pd.DataFrame({
                    'Latitude': [coord[0] for coord in route_coords],
                    'Longitude': [coord[1] for coord in route_coords]
                })
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False),
                    file_name=f"route_{method}.csv",
                    mime="text/csv"
                )

# Information section
st.markdown("---")
st.markdown("""
    ### 📝 About the Algorithms:
    - **Dijkstra**: Best for weighted graphs, finds shortest path considering road lengths
    - **Bellman-Ford**: Can handle negative weights (rare in roads)
    - **BFS**: Finds shortest path in terms of number of roads
    - **DFS**: Finds any path (not necessarily shortest)
""")

# Algorithm complexities
st.markdown("""
    ### ⚙️ Time Complexities:
    - Dijkstra: O((V + E) log V)
    - Bellman-Ford: O(V × E)
    - BFS: O(V + E)
    - DFS: O(V + E)
    
    Where V = number of vertices (nodes), E = number of edges (roads)
""")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for DAA Project")