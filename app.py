import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# App title
st.title("Interactive Sankey Diagram Creator with White Plot Background")

# Instructions
st.write("Enter your source, target, value, and color data below to generate a Sankey diagram.")

# Default data for the table with more examples
default_data = {
    "Source": ["A", "B", "A", "C", "D", "E", "F", "G"],
    "Target": ["B", "C", "D", "E", "F", "G", "H", "A"],
    "Value": [10, 15, 20, 25, 30, 35, 40, 45],
    "Node Color": [
        "rgb(0, 150, 150)",  # Teal
        "rgb(190, 200, 0)",  # Olive
        "rgb(240, 150, 0)",  # Orange
        "rgb(90, 80, 150)",  # Purple
        "rgb(200, 200, 0)",  # Yellow
        "rgb(50, 150, 200)",  # Light Blue
        "rgb(100, 100, 255)",  # Blue
        "rgb(180, 100, 150)"   # Pink
    ],
    "Link Color": [
        "rgba(0, 150, 150, 0.6)",  # Teal link
        "rgba(190, 200, 0, 0.6)",  # Olive link
        "rgba(240, 150, 0, 0.6)",  # Orange link
        "rgba(90, 80, 150, 0.6)",  # Purple link
        "rgba(200, 200, 0, 0.6)",  # Yellow link
        "rgba(50, 150, 200, 0.6)",  # Light Blue link
        "rgba(100, 100, 255, 0.6)",  # Blue link
        "rgba(180, 100, 150, 0.6)"   # Pink link
    ],
}

# Create or edit a table
data = st.data_editor(
    pd.DataFrame(default_data),
    use_container_width=True,
    num_rows="dynamic"  # Allows adding new rows
)

# Ensure data is valid
if not data.empty:
    # Extract columns for Sankey inputs
    sources = data["Source"].astype(str).tolist()
    targets = data["Target"].astype(str).tolist()
    values = data["Value"].astype(int).tolist()
    node_colors = data["Node Color"].astype(str).tolist()
    link_colors = data["Link Color"].astype(str).tolist()

    # Combine unique labels
    all_labels = list(set(sources + targets))
    node_indices = {label: index for index, label in enumerate(all_labels)}

    # Generate Sankey diagram
    fig = go.Fig
