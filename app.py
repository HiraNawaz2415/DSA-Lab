import streamlit as st

st.set_page_config(page_title="DAA Lab", layout="centered")

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

# ---------------------------
# Main Content
# ---------------------------
st.title("📚 Design and Analysis of Algorithms Lab")

st.write("""
Welcome to your interactive DAA Lab built with **Streamlit**!  
Use the sidebar to explore:
- 📊 **Sorting Algorithms**
- 🌳 **Trees** (BST, AVL, Red-Black)
- 🔗 **Graphs & Minimum Spanning Trees**
- ⚖️ **Complexity & Representation Comparisons**

Each module lets you **upload**, **run**, **visualize**, **analyze**, and **download** results.
""")
