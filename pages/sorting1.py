import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fpdf import FPDF
import tempfile

# ---------------------------
# Page config & custom CSS
# ---------------------------
st.set_page_config(page_title="Sorting Visualizer", layout="centered")

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

# ---------------------------
# Title
# ---------------------------
st.title("Sorting Algorithms - Visualizer, CSV and PDF Export")

# ---------------------------
# Sorting Algorithm Functions
# ---------------------------
def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr.copy())
    return arr, steps

def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            steps.append(arr.copy())
        arr[j + 1] = key
        steps.append(arr.copy())
    return arr, steps

def merge_sort(arr):
    steps = []
    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:m+1]
        R = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            steps.append(arr.copy())
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            steps.append(arr.copy())
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            steps.append(arr.copy())
    def mergeSort(arr, l, r):
        if l < r:
            m = (l + r) // 2
            mergeSort(arr, l, m)
            mergeSort(arr, m + 1, r)
            merge(arr, l, m, r)
    mergeSort(arr, 0, len(arr) - 1)
    return arr, steps

def quick_sort(arr):
    steps = []
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr.copy())
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr.copy())
        return i + 1
    def quickSort(low, high):
        if low < high:
            pi = partition(low, high)
            quickSort(low, pi - 1)
            quickSort(pi + 1, high)
    quickSort(0, len(arr) - 1)
    return arr, steps

def heapify(arr, n, i, steps):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        steps.append(arr.copy())
        heapify(arr, n, largest, steps)

def heap_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        steps.append(arr.copy())
        heapify(arr, i, 0, steps)
    return arr, steps

def counting_sort(arr):
    steps = []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    i = 0
    for num, c in enumerate(count):
        for _ in range(c):
            arr[i] = num
            i += 1
            steps.append(arr.copy())
    return arr, steps

def radix_sort(arr):
    steps = []
    def counting_sort_exp(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in arr:
            index = i // exp
            count[index % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1
        for i in range(len(arr)):
            arr[i] = output[i]
            steps.append(arr.copy())
    max1 = max(arr)
    exp = 1
    while max1 // exp > 0:
        counting_sort_exp(arr, exp)
        exp *= 10
    return arr, steps

# ---------------------------
# PDF Export Utility
# ---------------------------
def generate_pdf(algo_name, result, steps):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"{algo_name} - Sorting Report", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Final Sorted Array:", ln=True)
    pdf.multi_cell(0, 10, f"{result}")

    pdf.cell(0, 10, "Sorting Steps:", ln=True)
    for idx, step in enumerate(steps, 1):
        pdf.multi_cell(0, 10, f"Step {idx}: {step}")

    return pdf.output(dest="S").encode("latin1")

# ---------------------------
# UI & Controls
# ---------------------------
algo = st.selectbox("Choose Algorithm", [
    "Bubble Sort", "Insertion Sort", "Merge Sort",
    "Quick Sort", "Heap Sort", "Counting Sort", "Radix Sort"
])

size = st.slider("Default Input Size (used if no custom array)", 5, 50, 10)
user_input = st.text_input("Enter your array (comma-separated):", "")

if user_input.strip():
    try:
        arr = [int(x.strip()) for x in user_input.split(",")]
        st.success(f"Using custom array: {arr}")
    except:
        st.error("Invalid input! Please enter integers separated by commas.")
        arr = random.sample(range(1, 100), size)
else:
    arr = random.sample(range(1, 100), size)
    st.info(f"Using random array: {arr}")

if st.button("Run Sort"):
    start = time.time()
    arr_copy = arr.copy()
    if algo == "Bubble Sort":
        result, steps = bubble_sort(arr_copy)
    elif algo == "Insertion Sort":
        result, steps = insertion_sort(arr_copy)
    elif algo == "Merge Sort":
        result, steps = merge_sort(arr_copy)
    elif algo == "Quick Sort":
        result, steps = quick_sort(arr_copy)
    elif algo == "Heap Sort":
        result, steps = heap_sort(arr_copy)
    elif algo == "Counting Sort":
        result, steps = counting_sort(arr_copy)
    elif algo == "Radix Sort":
        result, steps = radix_sort(arr_copy)
    end = time.time()

    st.success(f"Sorted: {result}")
    st.info(f"Time Taken: {end - start:.6f} seconds")

    st.subheader("Step-by-Step Visualization")
    for i, step in enumerate(steps):
        fig, ax = plt.subplots()
        ax.bar(range(len(step)), step, color='skyblue')
        ax.set_title(f"{algo} - Step {i + 1}")
        st.pyplot(fig)

    st.subheader("Download Results")
    df_result = pd.DataFrame({"Sorted Array": result})
    csv_result = df_result.to_csv(index=False).encode()
    file_name = f"{algo.replace(' ', '_').lower()}_result.csv"
    st.download_button(
        label="Download CSV",
        data=csv_result,
        file_name=file_name,
        mime="text/csv"
    )

    pdf_file = generate_pdf(algo, result, steps)
    pdf_name = f"{algo.replace(' ', '_').lower()}_result.pdf"
    st.download_button(
        label="Download PDF",
        data=pdf_file,
        file_name=pdf_name,
        mime="application/pdf"
    )

    st.subheader("Complexity Comparison")
    sizes = list(range(5, 100, 5))
    times = []
    for s in sizes:
        a = random.sample(range(1, 1000), s)
        t0 = time.time()
        if algo == "Bubble Sort":
            bubble_sort(a)
        elif algo == "Insertion Sort":
            insertion_sort(a)
        elif algo == "Merge Sort":
            merge_sort(a)
        elif algo == "Quick Sort":
            quick_sort(a)
        elif algo == "Heap Sort":
            heap_sort(a)
        elif algo == "Counting Sort":
            counting_sort(a)
        elif algo == "Radix Sort":
            radix_sort(a)
        t1 = time.time()
        times.append(t1 - t0)

    fig, ax = plt.subplots()
    ax.plot(sizes, times, label="Experimental Time", marker='o')
    if algo in ["Bubble Sort", "Insertion Sort"]:
        theory = [s ** 2 for s in sizes]
    elif algo in ["Merge Sort", "Quick Sort", "Heap Sort"]:
        theory = [s * np.log2(s) for s in sizes]
    elif algo in ["Counting Sort", "Radix Sort"]:
        theory = [s for s in sizes]
    else:
        theory = times
    theory_scaled = [t / max(theory) * max(times) for t in theory]
    ax.plot(sizes, theory_scaled, label="Theoretical Trend", linestyle='--')
    ax.set_xlabel("Input Size")
    ax.set_ylabel("Time (s)")
    ax.set_title(f"{algo}: Theoretical vs Experimental")
    ax.legend()
    st.pyplot(fig)
