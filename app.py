import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Custom colors
default_target_color = "#808080"  # Default grey color for source nodes without a specified color
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

# App title
st.title("Interactive Sankey Diagram with Formatting Settings")

# Instructions
st.write("Modify the Sankey diagram settings in the table below. Add units for flows in the main data table.")

# Default settings for Sankey formatting
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
        ",",  # Decimal separator
        ".",  # Thousands separator
        18,   # Font size
        1100, # Figure width
        800,  # Figure height
        500,  # Pad
        0.4,  # Transparency
        "Calibri",  # Font family
    ],
}

# Create or edit the settings table
settings_table = st.data_editor(
    pd.DataFrame(default_settings),
    use_container_width=True,
    num_rows="dynamic",
    key="settings_table"
)

# Default data for the Sankey table
default_data = {
    "Source": ["A", "B", "A", "C", "D", "E", "F", "G"],
    "Target": ["B", "C", "D", "E", "F", "G", "H", "A"],
    "Value": [10, 15, 20, 25, 30, 35, 40, 45],
    "Unit": ["m3/y"] * 8,  # Default unit
    "Target Node Color": [
        "Teal",        # Custom Teal
        "Lime",        # Custom Lime
        "Orange",      # Custom Orange
        "Lilac",       # Custom Lilac
        "Lime",        # Custom Lime
        "Teal",        # Custom Teal
        "Lilac",       # Custom Lilac
        "",            # Missing color, should default to grey
    ],
    "Link Color": [
        "Teal_Transparent",  # Custom Transparent Teal
        "Lime_Transparent",  # Custom Transparent Lime
        "Orange_Transparent", # Custom Transparent Orange
        "Lilac_Transparent",  # Custom Transparent Lilac
        "Lime_Transparent",  # Custom Transparent Lime
        "Teal_Transparent",  # Custom Transparent Teal
        "Lilac_Transparent",  # Custom Transparent Lilac
        "",                  # Missing color, should default to grey
    ],
}

# Create or edit the main data table
data = st.data_editor(
    pd.DataFrame(default_data),
    use_container_width=True,
    num_rows="dynamic",
    key="data_table"
)

# Ensure valid settings
if not settings_table.empty:
    settings = settings_table.set_index("Setting")["Value"]

# Apply formatting settings
figure_width = int(settings["figure_width"])
figure_height = int(settings["figure_height"])
font_size = int(settings["font_size"])
pad = int(settings["pad"])
font_family = settings["font_family"]
transparency = float(settings["transparency"])
decimal_separator = settings["decimal_separator"]
thousands_separator = settings["thousands_separator"]

# Replace missing colors with default grey
data["Target Node Color"] = data["Target Node Color"].replace("", default_target_color)
data["Link Color"] = data["Link Color"].replace("", default_target_color)

# Ensure data is valid
if not data.empty:
    # Extract columns for Sankey inputs
    sources = data["Source"].astype(str).tolist()
    targets = data["Target"].astype(str).tolist()
    values = data["Value"].astype(float).tolist()
    units = data["Unit"].astype(str).tolist()
    target_colors = data["Target Node Color"].apply(
        lambda x: custom_colors.get(x, x)  # Use custom color or the given value
    ).tolist()
    link_colors = data["Link Color"].apply(
        lambda x: custom_colors.get(x, x)  # Use custom color or the given value
    ).tolist()

    # Combine unique labels
    all_labels = list(set(sources + targets))
    node_indices = {label: index for index, label in enumerate(all_labels)}

    # Create a mapping for node colors
    node_color_map = {target: color for target, color in zip(targets, target_colors)}

    # Assign colors to nodes
    node_colors = [
        node_color_map.get(node, default_target_color)  # Default source node color is grey
        for node in all_labels
    ]

    # Format values and units for labels
    formatted_labels = [
        f"{src}: {value:,.2f} {unit}".replace(",", thousands_separator).replace(".", decimal_separator)
        for src, value, unit in zip(sources, values, units)
    ]

    # Generate Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=pad,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color=node_colors,  # Use the computed node colors
        ),
        link=dict(
            source=[node_indices[src] for src in sources],
            target=[node_indices[tgt] for tgt in targets],
            value=values,
            label=formatted_labels,
            color=link_colors,  # Use the custom link colors
        ),
    )])

    # Update layout to set plot and paper background to white
    fig.update_layout(
        plot_bgcolor='white',  # Set the plot area background to white
        paper_bgcolor='white',  # Set the entire figure background to white
        title_text="Sankey Diagram",
        font=dict(family=font_family, size=font_size),
        width=figure_width,
        height=figure_height,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Display the Sankey diagram
    st.plotly_chart(fig)
else:
    st.warning("Please enter valid data to generate the Sankey diagram.")
