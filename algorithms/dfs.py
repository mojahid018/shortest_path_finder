def dfs_path(G, start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        (vertex, path) = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)

        if vertex == goal:
            return path

        for neighbor in G.neighbors(vertex):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return None  # If no path found