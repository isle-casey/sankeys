import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# App title
st.title("Interactive Sankey Diagram Creator with Colors")

# Instructions
st.write("Enter your source, target, value, and optional color data below to generate a Sankey diagram.")

# Default data for the table
default_data = {
    "Source": ["A", "B", "A"],
    "Target": ["B", "C", "D"],
    "Value": [10, 5, 15],
    "Node Color": ["rgb(0, 150, 150)", "rgb(190, 200, 0)", "rgb(240, 150, 0)"],  # Node colors
    "Link Color": ["rgba(0, 150, 150, 0.6)", "rgba(190, 200, 0, 0.6)", "rgba(240, 150, 0, 0.6)"],  # Link colors
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
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color=[node_colors[all_labels.index(node)] if node in sources else "gray" for node in all_labels],
        ),
        link=dict(
            source=[node_indices[src] for src in sources],
            target=[node_indices[tgt] for tgt in targets],
            value=values,
            color=link_colors,  # Use the custom link colors
        ),
    )])

    # Display the Sankey diagram
    st.plotly_chart(fig)
else:
    st.warning("Please enter valid data to generate the Sankey diagram.")
