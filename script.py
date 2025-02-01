import streamlit as st
import numpy as np
import pandas as pd


st.title('Eces App')
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [45.5019, -73.5674],
    columns=['lat', 'lon'])

st.map(map_data,size=20,color="#0044ff")



dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)


