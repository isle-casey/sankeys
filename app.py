import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Use the port from the environment or default to 8501
#port = int(os.getenv('PORT', 8501))

# App title
st.title("Interactive Sankey Diagram Creator")

# Instructions
st.write("Enter your source, target, and value data below to generate a Sankey diagram.")

# Default data for the table
default_data = {
    "Source": ["A", "B", "A"],
    "Target": ["B", "C", "D"],
    "Value": [10, 5, 15],
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

    # Combine unique labels
    all_labels = list(set(sources + targets))

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
        ),
        link=dict(
            source=[all_labels.index(src) for src in sources],
            target=[all_labels.index(tgt) for tgt in targets],
            value=values,
        ),
    )])

    # Display the Sankey diagram
    st.plotly_chart(fig)
else:
    st.warning("Please enter valid data to generate the Sankey diagram.")
