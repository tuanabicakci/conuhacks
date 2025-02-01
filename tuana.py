import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

map_data = pd.read_csv("montreal-districts.csv")
st.map(map_data)

