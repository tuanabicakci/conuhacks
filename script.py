import pydeck
import streamlit as st
import pandas as pd

st.markdown(
    """
    If you are a **student** or **immigrant** who just arrived in Montreal and don't know in which neighbourhood to rent, we got the perfect index for you!  
    You can **filter your options** and choose the criteria that matter most to you, including:
    - 🛡️ **Safety**
    - 💼 **Economic Opportunity**
    - 🤝 **Social Inclusion**
    - 🚆 **Transportation**
    - 🏘️ **Housing & Infrastructure**
    - 📚 **Education & Recreation**

    Use the filters above the map to explore and find your ideal neighbourhood!
    """
)

district_data = pd.read_csv("montreal-districts-with-filters.csv")

# Ensure numeric columns are properly parsed
district_data["lat"] = pd.to_numeric(district_data["lat"], errors="coerce")
district_data["lon"] = pd.to_numeric(district_data["lon"], errors="coerce")
district_data["total-score"] = pd.to_numeric(district_data["total-score"], errors="coerce")

filters = st.multiselect(
    "Select filters",
    options=["🛡 Safety", "💼 Economic Opportunity", "🤝 Social Inclusion", "🚆 Transportation", "🏘 Housing & Infrastructure", "📚 Education & Recreation"],
    default=["🛡 Safety", "💼 Economic Opportunity", "🤝 Social Inclusion", "🚆 Transportation", "🏘 Housing & Infrastructure", "📚 Education & Recreation"],
)

district_data["total-score"] = district_data[filters].sum(axis=1)

district_data["size"] = district_data["total-score"] * 5

def get_color(score):
    if score >= 80:
        return [8, 48, 107]  # Dark Blue (80+)
    elif score >= 60:
        return [33, 113, 181]  # Blue (60-80)
    elif score >= 40:
        return [107, 174, 214]  # Light Blue (40-60)
    elif score >= 20:
        return [189, 215, 231]  # Pale Blue (20-40)
    else:
        return [247, 251, 255]  # White (0-20)

district_data["color"] = district_data["total-score"].apply(get_color)

point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=district_data,
    get_position=["lon", "lat"],
    get_color="color",
    get_radius="size",
    id="district-layer",
    pickable=True,
    auto_highlight=True,
)

view_state = pydeck.ViewState(
    latitude=45.5019, longitude=-73.5674, zoom=10.5, pitch=30
)

chart = pydeck.Deck(
    layers=[point_layer],
    initial_view_state=view_state,
    tooltip={"html": "<b>District:</b> {district}<br><b>Score:</b> {total-score}"},
    map_style="mapbox://styles/mapbox/streets-v12",
)

st.pydeck_chart(chart)

sorted_data = district_data.sort_values(by="total-score", ascending=False, ignore_index=True, axis=0)
sorted_data.index = sorted_data.index + 1
# Convert the DataFrame to an HTML table
html_table = sorted_data[["district", "total-score"]].to_html(
    index=True,
    classes="styled-table",
)

# Custom CSS styling for the table
st.markdown(
    """
    <style>
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 16px;
        text-align: left;

    }
    .styled-table th, .styled-table td {
        padding: 12px;
        border: 1px solid #ddd;

    }
    .styled-table th {
        background-color: #9cdbfb;
        text-align: left;
        color: white;
    }
    .styled-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .styled-table tr:hover {
        background-color: #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the styled table
st.markdown(html_table, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .legend {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: white;
        padding: 10px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
        font-size: 12px;
        z-index: 1000;
        border-radius: 8px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }
    .color-circle {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        margin-right: 8px;
    }
    </style>
    <div class="legend">
        <b>Livability Index (%)</b><br>
        <div class="legend-item">
            <div class="color-circle" style="background: #08306b; width: 30px; height: 30px;"></div> (80+)
        </div>
        <div class="legend-item">
            <div class="color-circle" style="background: #2171b5; width: 25px; height: 25px;"></div> (60-80)
        </div>
        <div class="legend-item">
            <div class="color-circle" style="background: #6baed6; width: 20px; height: 20px;"></div> (40-60)
        </div>
        <div class="legend-item">
            <div class="color-circle" style="background: #bdd7e7; width: 15px; height: 15px;"></div> (20-40)
        </div>
        <div class="legend-item">
            <div class="color-circle" style="background: #f7fbff; width: 10px; height: 10px;"></div> (0-20)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
