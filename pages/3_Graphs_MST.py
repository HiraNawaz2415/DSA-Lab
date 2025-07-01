import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
# ---------------------------
# 📌 Custom CSS for light pink sidebar only
# ---------------------------
st.markdown("""
    <style>
    /* Sidebar background light pink */
    [data-testid="stSidebar"] {
        background-color: #ffe6f0;
    }

    /* Optional: Make sidebar text darker for readability */
    [data-testid="stSidebar"] * {
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)
st.title("🌐  Graph Lab")

# ------------------------------------------
# Graph Type & Weighted toggle
# ------------------------------------------
colA, colB = st.columns(2)
with colA:
    directed = st.radio("Graph Type:", ["Undirected", "Directed"], horizontal=True)
with colB:
    weighted = st.radio("Edge Type:", ["Weighted", "Unweighted"], horizontal=True)

if directed == "Undirected":
    G = nx.Graph()
else:
    G = nx.DiGraph()

# ------------------------------------------
# Add Edges
# ------------------------------------------
st.subheader("➕ Add Edges")
st.write(f"**Format:** If **Weighted**, use `Node1,Node2,Weight` | If **Unweighted**, use `Node1,Node2`")

example = "A,B,4\nA,C,2\nB,C,1\nB,D,5\nC,D,8" if weighted == "Weighted" else "A,B\nA,C\nB,C\nB,D\nC,D"
edges_input = st.text_area("Edges input:", example)

edges = edges_input.strip().split("\n")
for e in edges:
    parts = e.split(",")
    if weighted == "Weighted":
        if len(parts) >= 3:
            u, v, w = parts[0].strip(), parts[1].strip(), float(parts[2].strip())
            G.add_edge(u, v, weight=w)
    else:
        if len(parts) >= 2:
            u, v = parts[0].strip(), parts[1].strip()
            G.add_edge(u, v, weight=1)

st.write(f"**Nodes:** {list(G.nodes())}")
st.write(f"**Edges:** {list(G.edges(data=True))}")

# ------------------------------------------
# Initial Visual
# ------------------------------------------
st.subheader("🖼️ Initial Graph Visual")

pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
st.pyplot(fig)

# ------------------------------------------
# Representations
# ------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.checkbox(" Show Adjacency Matrix"):
        adj_matrix = nx.adjacency_matrix(G).todense()
        df_matrix = pd.DataFrame(adj_matrix, index=G.nodes(), columns=G.nodes())
        st.write(df_matrix)
        csv_matrix = df_matrix.to_csv(index=True).encode()
        st.download_button(
            "⬇️ Download Adjacency Matrix CSV",
            csv_matrix,
            "adjacency_matrix.csv",
            "text/csv"
        )

with col2:
    if st.checkbox(" Show Adjacency List"):
        adj_list = {n: list(G.adj[n]) for n in G.nodes()}
        df_list = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in adj_list.items()]))
        st.write(df_list)
        csv_list = df_list.to_csv(index=False).encode()
        st.download_button(
            "⬇️ Download Adjacency List CSV",
            csv_list,
            "adjacency_list.csv",
            "text/csv"
        )

# ------------------------------------------
# Traversals
# ------------------------------------------
st.subheader("🚶 Traversals")
start_node = st.text_input("Start Node for Traversal", value="A")

traversal_col1, traversal_col2 = st.columns(2)

# BFS
with traversal_col1:
    if st.button("Run BFS"):
        if start_node not in G:
            st.error("Start node not in graph!")
        else:
            visited = []
            queue = [start_node]
            steps = []

            while queue:
                v = queue.pop(0)
                if v not in visited:
                    visited.append(v)
                    queue.extend(set(G[v]) - set(visited))
                    steps.append(visited.copy())

            st.write("**BFS Steps:**")
            for i, step in enumerate(steps):
                st.write(f"Step {i+1}: {step}")

            st.subheader("BFS Traversal Visualization")
            for i, step in enumerate(steps):
                fig, ax = plt.subplots(figsize=(8, 6))
                node_colors = ["lightgreen" if node in step else "skyblue" for node in G.nodes()]
                nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, ax=ax)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
                st.pyplot(fig)
                st.caption(f"Step {i+1}: Visited {step}")

            st.info("**Time Complexity:** O(V + E)")

            df_bfs = pd.DataFrame({"Step": [i+1 for i in range(len(steps))], "Visited": steps})
            csv_bfs = df_bfs.to_csv(index=False).encode()
            st.download_button(
                "⬇️ Download BFS Steps CSV",
                csv_bfs,
                "bfs_steps.csv",
                "text/csv"
            )

# DFS
with traversal_col2:
    if st.button("Run DFS"):
        if start_node not in G:
            st.error("Start node not in graph!")
        else:
            visited = []
            stack = [start_node]
            steps = []

            while stack:
                v = stack.pop()
                if v not in visited:
                    visited.append(v)
                    stack.extend(reversed(list(set(G[v]) - set(visited))))
                    steps.append(visited.copy())

            st.write("**DFS Steps:**")
            for i, step in enumerate(steps):
                st.write(f"Step {i+1}: {step}")

            st.subheader("DFS Traversal Visualization")
            for i, step in enumerate(steps):
                fig, ax = plt.subplots(figsize=(8, 6))
                node_colors = ["orange" if node in step else "skyblue" for node in G.nodes()]
                nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, ax=ax)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
                st.pyplot(fig)
                st.caption(f"Step {i+1}: Visited {step}")

            st.info("**Time Complexity:** O(V + E)")

            df_dfs = pd.DataFrame({"Step": [i+1 for i in range(len(steps))], "Visited": steps})
            csv_dfs = df_dfs.to_csv(index=False).encode()
            st.download_button(
                "⬇️ Download DFS Steps CSV",
                csv_dfs,
                "dfs_steps.csv",
                "text/csv"
            )

# ------------------------------------------
# Dijkstra
# ------------------------------------------
st.subheader("Dijkstra's Shortest Path")
source_node = st.text_input("Source Node for Dijkstra", value="A")

if st.button("Run Dijkstra"):
    if source_node not in G:
        st.error("Source node not in graph!")
    else:
        has_negative = any(data['weight'] < 0 for _, _, data in G.edges(data=True))
        if has_negative:
            st.warning("⚠️ WARNING: Dijkstra's algorithm cannot handle negative weights!")

        try:
            lengths = nx.single_source_dijkstra_path_length(G, source_node)
            st.write("**Shortest distances from source:**")
            st.write(lengths)
            st.info("**Time Complexity:** O(E + V log V)")

            df_dijkstra = pd.DataFrame(lengths.items(), columns=["Node", "Distance"])
            csv_dijkstra = df_dijkstra.to_csv(index=False).encode()
            st.download_button(
                "⬇️ Download Dijkstra Distances CSV",
                csv_dijkstra,
                "dijkstra_distances.csv",
                "text/csv"
            )

            paths = nx.single_source_dijkstra_path(G, source_node)
            tree_edges = []
            for target in paths:
                path = paths[target]
                if len(path) > 1:
                    tree_edges.extend([(path[i], path[i+1]) for i in range(len(path)-1)])

            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5, ax=ax)
            st.pyplot(fig)
            st.caption("Red edges show shortest-path tree from source node.")

        except Exception as e:
            st.error(f"Error: {e}")

# ------------------------------------------
# Bellman-Ford
# ------------------------------------------
st.subheader("Bellman-Ford — Detect Negative Cycle")
source_bf = st.text_input("Source Node for Bellman-Ford", value="A")

if st.button("Run Bellman-Ford"):
    if source_bf not in G:
        st.error("Source node not in graph!")
    else:
        try:
            if not isinstance(G, nx.DiGraph):
                H = nx.DiGraph()
                H.add_weighted_edges_from([(u, v, d['weight']) for u, v, d in G.edges(data=True)])
            else:
                H = G

            lengths, paths = nx.single_source_bellman_ford(H, source_bf, weight='weight')

            st.success("No Negative Weight Cycle Detected!")
            st.write("**Shortest distances from source:**")
            st.write(lengths)

            df_bf = pd.DataFrame(lengths.items(), columns=["Node", "Distance"])
            csv_bf = df_bf.to_csv(index=False).encode()
            st.download_button(
                "⬇️ Download Bellman-Ford Distances CSV",
                csv_bf,
                "bellman_ford_distances.csv",
                "text/csv"
            )

            tree_edges = []
            for target in paths:
                path = paths[target]
                if len(path) > 1:
                    tree_edges.extend([(path[i], path[i+1]) for i in range(len(path)-1)])

            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5, ax=ax)
            st.pyplot(fig)
            st.caption("Red edges show Bellman-Ford shortest-path tree.")
            st.info("**Time Complexity:** O(V × E)")

        except nx.NetworkXUnbounded:
            st.error("Negative Weight Cycle Detected! Shortest paths do not exist.")

# ------------------------------------------
# MST
# ------------------------------------------
if directed == "Undirected":
    st.subheader("🌳 Minimum Spanning Tree (MST)")
    mst_method = st.radio("Select MST Algorithm", ["Prim's", "Kruskal's"], horizontal=True)

    mst = None
    if st.button("Run MST"):
        if mst_method == "Prim's":
            mst = nx.minimum_spanning_tree(G, algorithm="prim")
            st.success("Prim's MST computed.")
            st.info("**Time Complexity (Prim’s):** O(E log V)")
        elif mst_method == "Kruskal's":
            mst = nx.minimum_spanning_tree(G, algorithm="kruskal")
            st.success("Kruskal's MST computed.")
            st.info("**Time Complexity (Kruskal’s):** O(E log E)")

        if mst:
            mst_edges = list(mst.edges(data=True))
            st.write(mst_edges)

            df_mst = pd.DataFrame(
                [(u, v, d['weight']) for u, v, d in mst_edges],
                columns=["Node1", "Node2", "Weight"]
            )
            csv_mst = df_mst.to_csv(index=False).encode()
            st.download_button(
                "⬇️ Download MST Edges CSV",
                csv_mst,
                "mst_edges.csv",
                "text/csv"
            )

            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=mst.edges(), edge_color='red', width=2.5, ax=ax)
            st.pyplot(fig)
