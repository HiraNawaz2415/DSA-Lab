import streamlit as st
import graphviz
import pandas as pd

st.set_page_config(layout="centered")
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
st.title("🌳 Trees — BST, AVL & Red-Black (Step by Step Visualizer)")

# -----------------------
# DATA STRUCTURES
# -----------------------

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class RBNode:
    def __init__(self, key, color="R"):
        self.key = key
        self.left = None
        self.right = None
        self.color = color

# -----------------------
# BST Insert/Delete
# -----------------------

def insert_bst(root, key):
    if root is None:
        return Node(key)
    elif key < root.key:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root

def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete_bst(root, key):
    if root is None:
        return root
    if key < root.key:
        root.left = delete_bst(root.left, key)
    elif key > root.key:
        root.right = delete_bst(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete_bst(root.right, temp.key)
    return root

# -----------------------
# AVL Insert/Delete
# -----------------------

def get_height(root):
    return 0 if not root else root.height

def get_balance(root):
    return 0 if not root else get_height(root.left) - get_height(root.right)

def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x

def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

def insert_avl(root, key):
    if not root:
        return Node(key)
    elif key < root.key:
        root.left = insert_avl(root.left, key)
    else:
        root.right = insert_avl(root.right, key)

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and key < root.left.key:
        return right_rotate(root)
    if balance < -1 and key > root.right.key:
        return left_rotate(root)
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

def delete_avl(root, key):
    if not root:
        return root
    if key < root.key:
        root.left = delete_avl(root.left, key)
    elif key > root.key:
        root.right = delete_avl(root.right, key)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete_avl(root.right, temp.key)

    if not root:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and get_balance(root.left) >= 0:
        return right_rotate(root)
    if balance > 1 and get_balance(root.left) < 0:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and get_balance(root.right) <= 0:
        return left_rotate(root)
    if balance < -1 and get_balance(root.right) > 0:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

# -----------------------
# RB Insert (Concept only)
# -----------------------

def insert_rb(root, key):
    if not root:
        return RBNode(key)
    elif key < root.key:
        root.left = insert_rb(root.left, key)
    else:
        root.right = insert_rb(root.right, key)
    return root

# -----------------------
# Traversals
# -----------------------

def inorder(root, res):
    if root:
        inorder(root.left, res)
        res.append(root.key)
        inorder(root.right, res)

def preorder(root, res):
    if root:
        res.append(root.key)
        preorder(root.left, res)
        preorder(root.right, res)

def postorder(root, res):
    if root:
        postorder(root.left, res)
        postorder(root.right, res)
        res.append(root.key)

# -----------------------
# Graphviz Drawing
# -----------------------

def draw_bst(node, dot=None):
    if dot is None:
        dot = graphviz.Digraph()
    if node:
        dot.node(str(node.key))
        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            draw_bst(node.left, dot)
        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            draw_bst(node.right, dot)
    return dot

def draw_rb(node, dot=None):
    if dot is None:
        dot = graphviz.Digraph()
    if node:
        dot.node(str(node.key), color="black", style="filled",
                 fillcolor="red" if node.color == "R" else "black",
                 fontcolor="white")
        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            draw_rb(node.left, dot)
        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            draw_rb(node.right, dot)
    return dot

# -----------------------
# UI
# -----------------------

tree_type = st.selectbox("Select Tree", ["BST", "AVL Tree", "Red-Black Tree"])
traversal_type = st.selectbox("Select Traversal", ["Inorder", "Preorder", "Postorder"])

values = st.text_input("Enter keys to insert (comma separated)", "50,30,70,20,40,60,80")
keys = [int(x.strip()) for x in values.split(',') if x.strip().isdigit()]

delete_key = st.text_input("Key to Delete (optional)")

root = None
steps = []  # Store trees at each step

# Insert step by step
for k in keys:
    if tree_type == "BST":
        root = insert_bst(root, k)
    elif tree_type == "AVL Tree":
        root = insert_avl(root, k)
    elif tree_type == "Red-Black Tree":
        root = insert_rb(root, k)
    steps.append(root)  # Save snapshot

# Optional delete step
if delete_key:
    if tree_type == "BST":
        root = delete_bst(root, int(delete_key))
    elif tree_type == "AVL Tree":
        root = delete_avl(root, int(delete_key))
    else:
        st.info("Red-Black Tree deletion not shown here.")
    steps.append(root)  # Final snapshot

st.subheader(f" {tree_type} — Step-by-Step")

for i, snapshot in enumerate(steps):
    dot = draw_bst(snapshot) if tree_type != "Red-Black Tree" else draw_rb(snapshot)
    st.graphviz_chart(dot)
    st.caption(f"Step {i + 1}")

# Traversal
res = []
if traversal_type == "Inorder":
    inorder(root, res)
elif traversal_type == "Preorder":
    preorder(root, res)
elif traversal_type == "Postorder":
    postorder(root, res)

st.write(f"{traversal_type}: ", res)

df = pd.DataFrame({f"{traversal_type}": res})
csv = df.to_csv(index=False).encode()
st.download_button("⬇️ Download Traversal CSV", csv, "tree_traversal.csv", "text/csv")
