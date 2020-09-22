import streamlit as st
import pandas as pd
import numpy as np
import folium as fo
from streamlit_folium import folium_static
import geopandas as gp
import altair as alt
import pydeck as pdk
import datetime

st.title("ST WORK")
st.markdown("""
Mr.WITSANU KHAKHRUANGRUAN 6030822121
""")

"""
## [See source code](https://github.com/WITSANUKHA/streamlit-work/blob/master/stwork.py)
"""

day = st.slider("Select Day",1,5,step = 1)
if day == 1:
        url = ("https://github.com/WITSANUKHA/streamlit-work/blob/master/20190101.csv")
elif day == 2:
        url = ("https://github.com/WITSANUKHA/streamlit-work/blob/master/20190102.csv")
elif day == 3:
        url = ("https://github.com/WITSANUKHA/streamlit-work/blob/master/20190103.csv")
elif day == 4:
        url = ("https://github.com/WITSANUKHA/streamlit-work/blob/master/20190104.csv")
else:
        url = ("https://github.com/WITSANUKHA/streamlit-work/blob/master/20190105.csv")

time_start = "timestart"

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[time_start] = pd.to_datetime(data[time_start])
    return data
data = load_data(100000)

time = st.slider("Select time",0,23)
data = data[data[time_start].dt.hour == hour]

data = data.drop(data.columns[0], axis=1)
for i in range(5):
    data = data.drop(data.columns[6], axis=1)

st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 3) % 24))
midpoint = (np.average(data["latstartl"]), np.average(data["lonstartl"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lonstartl", "latstartl"],
            radius=150,
            elevation_scale=5,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 3) % 24))
filtered = data[
    (data[time_start].dt.hour >= hour) & (data[time_start].dt.hour < (hour + 3))
]
hist = np.histogram(filtered[time_start].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)

if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 3) % 24))
    st.write(data)
