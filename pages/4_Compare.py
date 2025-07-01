import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Graph Matrix/List Dashboard", layout="centered")

# ---------------------------
# 📌 Custom CSS for light pink sidebar only
# ---------------------------
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #ffe6f0;
    }
    [data-testid="stSidebar"] * {
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚖️ Adjacency Matrix vs List — Dashboard")

# -------------------------------
# Sidebar Menu
# -------------------------------
st.sidebar.header("📂 Menu")

menu_option = st.sidebar.selectbox(
    "Select Mode",
    ["Generate Graph", "Upload CSV"]
)

algo = st.sidebar.selectbox(
    "Algorithm",
    ["BFS", "DFS"]
)

# -------------------------------
# BFS/DFS Functions
# -------------------------------
def bfs_matrix(matrix, start):
    visited = [False] * len(matrix)
    queue = [start]
    visited[start] = True
    while queue:
        node = queue.pop(0)
        for i, connected in enumerate(matrix[node]):
            if connected and not visited[i]:
                queue.append(i)
                visited[i] = True

def dfs_matrix(matrix, node, visited):
    visited[node] = True
    for i, connected in enumerate(matrix[node]):
        if connected and not visited[i]:
            dfs_matrix(matrix, i, visited)

def bfs_list(adj_list, start):
    visited = {node: False for node in adj_list}
    queue = [start]
    visited[start] = True
    while queue:
        node = queue.pop(0)
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True

def dfs_list(adj_list, node, visited):
    visited[node] = True
    for neighbor in adj_list[node]:
        if not visited[neighbor]:
            dfs_list(adj_list, neighbor, visited)

# -------------------------------
# Upload Mode
# -------------------------------
if menu_option == "Upload CSV":
    st.subheader("📥 Upload Adjacency Matrix CSV")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file, header=None)
        adj_matrix = df.to_numpy()
        st.write("✅ Uploaded Matrix:")
        st.dataframe(df)

        # Convert to list
        adj_list = {}
        for i in range(len(adj_matrix)):
            adj_list[i] = []
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] != 0:
                    adj_list[i].append(j)

        st.write("✅ Converted Adjacency List:")
        st.write(adj_list)

        t0 = time.time()
        if algo == "BFS":
            bfs_matrix(adj_matrix, 0)
        else:
            visited = [False] * len(adj_matrix)
            dfs_matrix(adj_matrix, 0, visited)
        t1 = time.time()

        t2 = time.time()
        if algo == "BFS":
            bfs_list(adj_list, 0)
        else:
            visited = {node: False for node in adj_list}
            dfs_list(adj_list, 0, visited)
        t3 = time.time()

        matrix_time = t1 - t0
        list_time = t3 - t2

        st.info(f"Matrix {algo} Time: {matrix_time:.6f}s")
        st.info(f"List {algo} Time: {list_time:.6f}s")

        fig, ax = plt.subplots()
        ax.bar(["Matrix", "List"], [matrix_time, list_time], color=['#1f77b4', '#2ca02c'])
        ax.set_ylabel("Time (s)")
        ax.set_title(f"{algo} — Matrix vs List")
        st.pyplot(fig)

        # PDF Export with Chart
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            fig.savefig(tmp_img.name)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"{algo} Comparison Report", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Matrix Time: {matrix_time:.6f}s", ln=True)
            pdf.cell(200, 10, txt=f"List Time: {list_time:.6f}s", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Comparison Chart:", ln=True)
            pdf.image(tmp_img.name, x=10, y=60, w=180)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdf.output(tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button("⬇️ Download PDF Report", f, file_name="matrix_list_comparison.pdf", mime="application/pdf")

# -------------------------------
# Generate Mode
# -------------------------------
elif menu_option == "Generate Graph":
    st.subheader("🧩 Generate Random Graph")

    graph_type = st.radio("Graph Type", ["Sparse", "Dense"])
    num_nodes = st.slider("Number of Nodes", 5, 200, 20)

    if st.button("Generate"):
        p = 0.1 if graph_type == "Sparse" else 0.7
        G = nx.erdos_renyi_graph(num_nodes, p)

        st.success(f"Generated {graph_type} graph with {G.number_of_edges()} edges.")

        adj_matrix = nx.adjacency_matrix(G).todense()
        adj_list = nx.to_dict_of_lists(G)

        st.write("📋 Adjacency Matrix:")
        st.dataframe(adj_matrix)

        st.write("📋 Adjacency List:")
        st.write(adj_list)

        t0 = time.time()
        if algo == "BFS":
            bfs_matrix(adj_matrix, 0)
        else:
            visited = [False] * len(adj_matrix)
            dfs_matrix(adj_matrix, 0, visited)
        t1 = time.time()

        t2 = time.time()
        if algo == "BFS":
            bfs_list(adj_list, 0)
        else:
            visited = {node: False for node in adj_list}
            dfs_list(adj_list, 0, visited)
        t3 = time.time()

        matrix_time = t1 - t0
        list_time = t3 - t2

        st.info(f"Matrix {algo} Time: {matrix_time:.6f}s")
        st.info(f"List {algo} Time: {list_time:.6f}s")

        fig, ax = plt.subplots()
        ax.bar(["Matrix", "List"], [matrix_time, list_time], color=['#1f77b4', '#2ca02c'])
        ax.set_ylabel("Time (s)")
        ax.set_title(f"{algo} — Matrix vs List")
        st.pyplot(fig)

        # PDF Export with Chart
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            fig.savefig(tmp_img.name)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"{algo} Comparison Report", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Matrix Time: {matrix_time:.6f}s", ln=True)
            pdf.cell(200, 10, txt=f"List Time: {list_time:.6f}s", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Comparison Chart:", ln=True)
            pdf.image(tmp_img.name, x=10, y=60, w=180)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdf.output(tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button("⬇️ Download PDF Report", f, file_name="matrix_list_comparison.pdf", mime="application/pdf")
