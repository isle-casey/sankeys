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

    # Update layout to set plot background to white
    fig.update_layout(
        plot_bgcolor='white',  # Set the plot background to white
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
