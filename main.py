import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.write("# EA FC 25 Players Stats")

df = pd.read_csv("data/all_players.csv")

data = df.copy()

nations = st.sidebar.multiselect(
    "Select Nation",
    np.sort(data["Nation"].unique().tolist())
)
if nations:
    data = data[data["Nation"].isin(nations)]

positions = st.sidebar.multiselect(
    'Select Position',
    np.sort(data["Position"].unique().tolist()),
)
if positions:
    data = data[data["Position"].isin(positions)]

teams = st.sidebar.multiselect(
    'Select Team',
    np.sort(data["Team"].unique().tolist()),
)
if teams:
    data = data[data["Team"].isin(teams)]

overall = st.sidebar.slider(
    'Select OVR',
    min_value=data["OVR"].min(), max_value=data["OVR"].max(), value=(data["OVR"].min(), data["OVR"].max())
)
if overall[0] >= overall[1]:
    st.error("Минимальное значение не должно превшать максимальное значение")
else:
    data = data[(data["OVR"] >= overall[0]) & (data["OVR"] <= overall[1])]

ages = st.sidebar.slider(
    'Select Age',
    min_value=data["Age"].min(), max_value=data["Age"].max(), value=(data["Age"].min(), data["Age"].max())
)
if ages[0] >= ages[1]:
    st.error("Минимальное значение не должно превшать максимальное значение")
else:
    data = data[(data["Age"] >= ages[0]) & (data["Age"] <= ages[1])]

data["Height"] = data["Height"].apply(lambda x: int(x.split("cm")[0]))
heights = st.sidebar.slider(
    'Select Height',
    min_value=data["Height"].min(), max_value=data["Height"].max(), value=(data["Height"].min(), data["Height"].max())
)
if heights[0] >= heights[1]:
    st.error("Минимальное значение не должно превшать максимальное значение")
else:
    data = data[(data["Height"] >= heights[0]) & (data["Height"] <= heights[1])]

data["Weight"] = data["Weight"].apply(lambda x: int(x.split("kg")[0]))
data["Weight"] = data["Weight"].astype(np.float64)
weights = st.sidebar.slider(
    'Select Weight',
    min_value=data["Weight"].min(), max_value=data["Weight"].max(), value=(data["Weight"].min(), data["Weight"].max())
)
if weights[0] >= weights[1]:
    st.error("Минимальное значение не должно превшать максимальное значение")
else:
    data = data[(data["Weight"] >= weights[0]) & (data["Weight"] <= weights[1])]

st.altair_chart(alt.Chart(
    data[["OVR"]]).mark_bar().encode(
    x=alt.X("OVR", bin=True),
    y='count()'),
    use_container_width=True
)

st.dataframe(data[[
    "Name",
    "Position",
    "OVR",
    "PAC",
    "SHO",
    "PAS",
    "DRI",
    "DEF",
    "PHY"
]].reset_index(drop=True))

st.altair_chart(alt.Chart(
    data[["Position", "OVR"]]).mark_boxplot().encode(
    x='Position:N',
    y='OVR:Q',
    color='Position:N'),
    use_container_width=True
)
