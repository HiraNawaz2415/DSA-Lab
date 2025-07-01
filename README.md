# DSA-Lab

Welcome to your **multi-page interactive DSA Visualizer**, built with **Streamlit** — covering **Sorting Algorithms**, **Trees (BST, AVL, Red-Black)**, **Graphs (BFS, DFS, Matrix/List)**, and more.

Use this app to **generate**, **visualize**, **compare**, and **export** results for key Data Structures and Algorithms.  
Everything runs locally — no special server setup needed!

---

## Features

**Multi-page Streamlit App**  
- 📊 **Sorting Algorithms** — Bubble, Insertion, Merge, Quick, Heap, Counting, Radix
- 🌳 **Trees** — BST, AVL Tree, Red-Black Tree (concept)
- 🔗 **Graphs** — Adjacency Matrix/List, BFS & DFS comparison

**Visualizations**
- Step-by-step sorting bar charts
- Graphs drawn using `networkx` and `matplotlib`
- Trees drawn as simple graphs (no external Graphviz binary needed)

 **Exports**
- Download results as **CSV**
- Download results and diagrams as **PDF**

**No External Dependencies**
- Uses only Python packages (`streamlit`, `networkx`, `matplotlib`, `pandas`, `fpdf`)

---

## 🗂️ Repo Structure

```plaintext
📂 your-repo-name/
 ├── pages/
 │   ├── 1_Sorting.py      # Sorting Algorithms Visualizer
 │   ├── 2_Trees.py        # Tree Visualizer (BST, AVL, RB)
 │   ├── 3_Graphs.py       # Graph Algorithms (Matrix/List, BFS/DFS)
 ├── requirements.txt      # Python dependencies
 ├── README.md             # You are here!
 ├── docs/                 # Screenshots or docs (optional)
 ├── .streamlit/
 │   └── config.toml       # (Optional) Streamlit configs

