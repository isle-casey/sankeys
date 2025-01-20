import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# Function to generate random color
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Custom colors
custom_colors = {
    "Teal_Transparent": "rgba(0, 150, 150, 0.6)",
    "Lime_Transparent": "rgba(190, 200, 0, 0.6)",
    "Orange_Transparent": "rgba(240, 150, 0, 0.6)",
    "Lilac_Transparent": "rgba(90, 80, 150, 0.6)",
}

# App title
st.title("Interactive Sankey Diagram Creator with Random Default Colors")

# Instructions
st.write("Enter your source, target, value, and target node color data below to generate a Sankey diagram.")

# Default data for the table
default_data = {
    "Source": ["A", "B", "A", "C", "D", "E", "F", "G"],
    "Target": ["B", "C", "D", "E", "F", "G", "H", "A"],
    "Value": [10, 15, 20, 25, 30, 35, 40, 45],
    "Target Node Color": [
        random_color() for _ in range(8)  # Assign random colors
    ],
    "Link Color": [
        random_color() for _ in range(8)  # Assign random colors
    ],
}

# Create or edit a table
data = st.data_editor(
    pd.DataFrame(default_data),
    use_container_width=True,
    num_rows="dynamic"  # Allows adding new rows
)

# Automatically assign random colors to new rows
if len(data) > len(default_data["Source"]):  # If rows have been added
    for i in range(len(default_data["Source"]), len(data)):
        data.at[i, "Target Node Color"] = random_color()
        data.at[i, "Link Color"] = random_color()

# Ensure data is valid
if not data.empty:
    # Extract columns for Sankey inputs
    sources = data["Source"].astype(str).tolist()
    targets = data["Target"].astype(str).tolist()
    values = data["Value"].astype(int).tolist()
    target_colors = data["Target Node Color"].astype(str).tolist()
    link_colors = data["Link Color"].astype(str).tolist()

    # Combine unique labels
    all_labels = list(set(sources + targets))
    node_indices = {label: index for index, label in enumerate(all_labels)}

    # Create a mapping for node colors
    node_color_map = {target: color for target, color in zip(targets, target_colors)}

    # Assign colors to nodes
    node_colors = [
        node_color_map.get(node, random_color())  # Assign random color if missing
        for node in all_labels
    ]

    # Generate Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color=node_colors,  # Use the computed node colors
        ),
        link=dict(
            source=[node_indices[src] for src in sources],
            target=[node_indices[tgt] for tgt in targets],
            value=values,
            color=link_colors,  # Use the custom link colors
        ),
    )])

    # Update layout to set plot and paper background to white
    fig.update_layout(
        plot_bgcolor='white',  # Set the plot area background to white
        paper_bgcolor='white',  # Set the entire figure background to white
        title_text="Sankey Diagram",
        font=dict(family="Calibri", size=14),
        width=800,
        height=600,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Display the Sankey diagram
    st.plotly_chart(fig)
else:
    st.warning("Please enter valid data to generate the Sankey diagram.")
