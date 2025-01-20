import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Custom colors
custom_colors = {
    "Lime": "#BEC800",
    "Teal": "#009696",
    "Orange": "#F09600",
    "Lilac": "#5A5096",
    "Teal_Transparent": "rgba(0, 150, 150, 0.6)",
    "Lime_Transparent": "rgba(190, 200, 0, 0.6)",
    "Orange_Transparent": "rgba(240, 150, 0, 0.6)",
    "Lilac_Transparent": "rgba(90, 80, 150, 0.6)",
}

# Default data for the Sankey table
default_data = {
    "Source": ["A", "B", "A", "C", "D", "E", "F", "G"],
    "Target": ["B", "C", "D", "E", "F", "G", "H", "A"],
    "Value": [10, 15, 20, 25, 30, 35, 40, 45],
    "Unit": ["m3/y"] * 8,  # Default units for values
    "Target Node Color": [
        "Teal", "Lime", "Orange", "Lilac", "Lime", "Teal", "Lilac", "Orange"
    ],
    "Link Color": [
        "Teal_Transparent", "Lime_Transparent", "Orange_Transparent",
        "Lilac_Transparent", "Lime_Transparent", "Teal_Transparent",
        "Lilac_Transparent", "Orange_Transparent"
    ],
}

# Default settings for formatting table
default_settings = {
    "Setting": [
        "decimal_separator",
        "thousands_separator",
        "font_size",
        "figure_width",
        "figure_height",
        "pad",
        "transparency",
        "font_family",
    ],
    "Value": [
        ",", ".", "18", "1100", "800", "500", "0.4", "Calibri"
    ],
}

# App title
st.title("Interactive Sankey Diagram Creator with Aggregated Node Totals")

# Instructions
st.write("Edit the tables below to customize the Sankey diagram and its formatting.")

# Create or edit the Sankey data table
data = st.data_editor(
    pd.DataFrame(default_data),
    use_container_width=True,
    num_rows="dynamic",
    key="sankey_table"
)

# Create or edit the formatting settings table
settings_table = st.data_editor(
    pd.DataFrame(default_settings),
    use_container_width=True,
    num_rows="dynamic",
    disabled=False,
    key="settings_table"
)

# Ensure both tables are valid
if not data.empty and not settings_table.empty:
    # Extract Sankey table columns
    sources = data["Source"].astype(str).tolist()
    targets = data["Target"].astype(str).tolist()
    values = data["Value"].astype(int).tolist()
    units = data["Unit"].astype(str).tolist()
    target_colors = data["Target Node Color"].astype(str).tolist()
    link_colors = [custom_colors[color] for color in data["Link Color"].astype(str).tolist()]

    # Extract settings
    settings = settings_table.set_index("Setting")["Value"]

    # Convert numerical settings to appropriate data types
    figure_width = int(settings["figure_width"])
    figure_height = int(settings["figure_height"])
    font_size = int(settings["font_size"])
    pad = int(settings["pad"])
    transparency = float(settings["transparency"])
    decimal_separator = settings["decimal_separator"]
    thousands_separator = settings["thousands_separator"]
    font_family = settings["font_family"]

    # Format values using the specified separators
    def format_value(value):
        formatted = f"{value:,.0f}".replace(",", "TEMP").replace(".", decimal_separator).replace("TEMP", thousands_separator)
        return formatted

    # Combine unique labels and create a mapping for indices
    all_labels = list(set(sources + targets))
    node_indices = {label: index for index, label in enumerate(all_labels)}

    # Aggregate total values for each source and target node
    source_totals = {}
    target_totals = {}

    for source, value in zip(sources, values):
        source_totals[source] = source_totals.get(source, 0) + value

    for target, value in zip(targets, values):
        target_totals[target] = target_totals.get(target, 0) + value

    # Create a mapping for target node colors
    node_color_map = {target: custom_colors.get(color, "gray") for target, color in zip(targets, target_colors)}

    # Assign colors to nodes
    node_colors = [
        node_color_map.get(node, "gray")  # Default source node color is gray
        for node in all_labels
    ]

    # Generate Sankey labels with totals for source and target nodes
    sankey_labels = []
    for label in all_labels:
        if label in source_totals and label in target_totals:  # Node with both outgoing and incoming flows
            if source_totals[label] == target_totals[label]:  # If "in" and "out" are equal, show only one
                sankey_labels.append(
                    f"{label}<br>{format_value(source_totals[label])} {units[0]}"
                )
            else:
                sankey_labels.append(
                    f"{label}<br>Out: {format_value(source_totals[label])} {units[0]}<br>In: {format_value(target_totals[label])} {units[0]}"
                )
        elif label in source_totals:  # Source node with outgoing flow total
            sankey_labels.append(
                f"{label}<br>{format_value(source_totals[label])} {units[0]}"
            )
        elif label in target_totals:  # Target node with incoming flow total
            sankey_labels.append(
                f"{label}<br>{format_value(target_totals[label])} {units[0]}"
            )
        else:  # Standalone node
            sankey_labels.append(label)

    # Generate the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=pad,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=sankey_labels,
            color=node_colors,  # Use the computed node colors
            font=dict(size=font_size, color="black", family=font_family, weight="bold"),  # Make the font bold
        ),
        link=dict(
            source=[node_indices[src] for src in sources],
            target=[node_indices[tgt] for tgt in targets],
            value=values,
            color=link_colors,  # Use the custom link colors
        ),
    )])

    # Set the default template to "plotly_white"
    fig.update_layout(
        template="plotly_white",  # Apply the plotly_white template
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_text="Sankey Diagram",
        font=dict(family=font_family, size=font_size, color="black"),  # Set font for title and labels
        width=figure_width,
        height=figure_height,
        margin=dict(l=50, r=50, t=100, b=50),
        xaxis=dict(showgrid=False, zeroline=False),  # Hide grid lines on x-axis
        yaxis=dict(showgrid=False, zeroline=False),  # Hide grid lines on y-axis
    )

    # Display the Sankey diagram
    st.plotly_chart(fig)
else:
    st.warning("Please fill out both tables to generate the Sankey diagram.")
