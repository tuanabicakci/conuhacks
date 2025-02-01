import pydeck
import streamlit as st
import pandas as pd
import numpy as np

# map_data = pd.read_csv("montreal-districts.csv")
# st.map(map_data)

district_data = pd.read_csv(
    "montreal-districts.csv",
    header=0,
    names=["district", "lat", "lon"],
)
district_data["size"] = 100

point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=district_data,
    id="district-names",
    get_position=["lon", "lat"],
    get_color="[255, 75, 75]",
    pickable=True,
    auto_highlight=True,
    get_radius="size",

)

view_state = pydeck.ViewState(
    latitude=45.5019, longitude=-73.5674, controller=True, zoom=10.5, pitch=30
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{district}, {lat}, {lon}"},
    map_style="mapbox://styles/mapbox/streets-v12",
)

event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

event.selection

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
        <b>Liveability Index (%)</b><br>
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
        <div class="legend-item">
            <div class="color-circle" style="border: 1px solid black; background: transparent;"></div> No data
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
