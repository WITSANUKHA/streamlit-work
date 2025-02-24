import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gp
import datetime
import altair as alt
import pydeck as pdk

st.title('STREAMLIT-WORK')
'''
## [Developed from](https://github.com/streamlit/demo-uber-nyc-pickups)
'''

st.markdown('''
Mr.WITSANU KHAKHRUANGRUAN 6030822121
''')
'''
## [See my source code](https://github.com/WITSANUKHA/streamlit-work/blob/master/stwork.py)
'''

start = "timestart"
stop = "timestop"
day = st.slider("Select Day", 1, 5)
if day == 1:
        url = ("https://raw.githubusercontent.com/WITSANUKHA/streamlit-work/master/20190101.csv")
elif day == 2:
        url = ("https://raw.githubusercontent.com/WITSANUKHA/streamlit-work/master/20190102.csv")
        '''
        ## DATA DAY 2 Error
        '''
elif day == 3:
        url = ("https://raw.githubusercontent.com/WITSANUKHA/streamlit-work/master/20190103.csv")
elif day == 4:
        url = ("https://raw.githubusercontent.com/WITSANUKHA/streamlit-work/master/20190104.csv")
else:
        url= ("https://raw.githubusercontent.com/WITSANUKHA/streamlit-work/master/20190105.csv")

def load_data(nrows):
    data = pd.read_csv(url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[start] = pd.to_datetime(data[start])
    return data

data = load_data(100000)

hour = st.slider("Select Hour", 0, 23)

data = data[data[start].dt.hour == hour]
data = data.drop(data.columns[0], axis=1)
for i in range(5):
    data = data.drop(data.columns[6], axis=1)

st.subheader("START Data between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data["latstartl"]), np.average(data["lonstartl"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
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

st.subheader("By minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[start].dt.hour >= hour) & (data[start].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[start].dt.minute, bins=60, range=(0, 60))[0]
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
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
