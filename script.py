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

event = st.pydeck_chart(chart, on_select="rerun")
if event.selection and 'objects' in event.selection and "district-names" in event.selection['objects']:
    # Access the first object in the 'district-names' list
    selected_object = event.selection['objects']["district-names"][0]

    # Extract district data
    district = selected_object["district"]
    lat = selected_object["lat"]
    lon = selected_object["lon"]
    size = selected_object["size"]

    # Display the details
    st.write(f"**District:** {district}")
    st.write(f"**Latitude:** {lat}")
    st.write(f"**Longitude:** {lon}")
    st.write(f"**Size:** {size}")
else:
    st.write("### No district selected yet. Please click on a district to see details.")

