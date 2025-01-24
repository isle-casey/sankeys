import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# Set the page layout to wide
st.set_page_config(layout="wide")

# Custom colors
custom_colors = {
    "Lime": "#BEC800",
    "Teal": "#009696",
    "Orange": "#F09600",
    "Lilac": "#5A5096",
    "Teal_Transparent": "rgba(0, 150, 150, 0.3)",
    "Lime_Transparent": "rgba(190, 200, 0, 0.3)",
    "Orange_Transparent": "rgba(240, 150, 0, 0.3)",
    "Lilac_Transparent": "rgba(90, 80, 150, 0.3)",
}

# Default data for the Sankey table
default_data = {
    "Source": ["A", "B", "A", "C", "D", "E", "F", "G"],
    "Target": ["B", "C", "D", "E", "F", "G", "H", "A"],
    "Value": [10, 15, 20, 25, 30, 35, 40, 45],
    "Percentage": [10] * 8,
    "Unit": ["m3/y"] * 8,
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

# Replace empty or "none" values in "Unit" column with "m3/y"
data["Unit"] = data["Unit"].apply(lambda x: "m3/y" if pd.isna(x) or str(x).strip().lower() == "none" else x)

# Replace empty or "none" values in "Target Node Color" column with "Teal"
data["Target Node Color"] = data["Target Node Color"].apply(lambda x: "Teal" if pd.isna(x) or str(x).strip().lower() == "none" else x)

# Replace empty or "none" values in "Link Color" column with "Teal_Transparent"
data["Link Color"] = data["Link Color"].apply(lambda x: "Teal_Transparent" if pd.isna(x) or str(x).strip().lower() == "none" else x)

# Create or edit the formatting settings table
settings_table = st.data_editor(
    pd.DataFrame(default_settings),
    use_container_width=False,
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
    percentages = data["Percentage"].astype(int).tolist()
    units = data["Unit"].astype(str).tolist()
    target_colors = data["Target Node Color"].astype(str).tolist()

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

    # Dynamically adjust link transparency
    link_colors = [
        custom_colors[color].replace("0.3", f"{transparency}")  # Replace the hardcoded transparency
        if "rgba" in custom_colors[color]
        else custom_colors[color]  # Keep solid colors unchanged
        for color in data["Link Color"].astype(str).tolist()
    ]

    # Combine unique labels and create a mapping for indices
    all_labels = list(set(sources + targets))
    node_indices = {label: index for index, label in enumerate(all_labels)}

    # Aggregate total values and percentages for each source and target node
    source_totals = {}
    source_percentages = {}
    target_totals = {}
    target_percentages = {}

    for source, value, percentage in zip(sources, values, percentages):
        source_totals[source] = source_totals.get(source, 0) + value
        source_percentages[source] = source_percentages.get(source, 0) + percentage

    for target, value, percentage in zip(targets, values, percentages):
        target_totals[target] = target_totals.get(target, 0) + value
        target_percentages[target] = target_percentages.get(target, 0) + percentage

    # Create a mapping for target node colors
    node_color_map = {target: custom_colors.get(color, "gray") for target, color in zip(targets, target_colors)}

    # Assign colors to nodes
    node_colors = [
        node_color_map.get(node, "gray")  # Default source node color is gray
        for node in all_labels
    ]

    # Generate Sankey labels with totals, percentages, and units
    sankey_labels = []
    for label in all_labels:
        outgoing_percentage = source_percentages.get(label, 0)
        incoming_percentage = target_percentages.get(label, 0)

        # Select the larger of incoming or outgoing percentage
        max_percentage = max(outgoing_percentage, incoming_percentage)

        if label in source_totals and label in target_totals:  # Node with both outgoing and incoming flows
            sankey_labels.append(
                f"<b>{label}</b><br>{format_value(source_totals[label])} {units[0]}<br>{max_percentage}%"
            )
        elif label in source_totals:  # Source node with outgoing flow total
            sankey_labels.append(
                f"<b>{label}</b><br>{format_value(source_totals[label])} {units[0]}<br>{outgoing_percentage}%"
            )
        elif label in target_totals:  # Target node with incoming flow total
            sankey_labels.append(
                f"<b>{label}</b><br>{format_value(target_totals[label])} {units[0]}<br>{incoming_percentage}%"
            )
        else:  # Standalone node
            sankey_labels.append(f"<b>{label}</b>")

    # Generate the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=pad,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=sankey_labels,
            color=node_colors,  # Use the computed node colors
        ),
        link=dict(
            source=[node_indices[src] for src in sources],
            target=[node_indices[tgt] for tgt in targets],
            value=values,
            color=link_colors,  # Use the dynamically computed link colors
        ),
    )])

    # Set the default template to "plotly_white"
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_text="Sankey Diagram",
        font=dict(family=font_family, size=font_size, color="black"),
        width=figure_width,
        height=figure_height,
        margin=dict(l=50, r=50, t=100, b=50),
    )

    # Display the Sankey diagram
    st.plotly_chart(fig)

    # Download functionality
    with io.BytesIO() as buffer:
        fig.write_image(buffer, format="svg")
        st.download_button(
            label="Download Sankey Diagram as SVG",
            data=buffer,
            file_name="sankey_diagram.svg",
            mime="image/svg+xml",
        )
else:
    st.warning("Please fill out both tables to
