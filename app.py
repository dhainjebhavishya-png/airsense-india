import streamlit as st
from data import get_data
from config import CITIES, DEFAULT_CITY
import plotly.graph_objects as go

from data import get_long_data
from features import add_features
from model import train_all, forecast, latest_row
from insights import categorize, ADVICE, ADVICE_GROUPS

st.set_page_config(page_title="AirSense India", layout="wide")

city = st.sidebar.selectbox("City", list(CITIES), index=list(CITIES).index(DEFAULT_CITY))
LAT, LON = CITIES[city]


@st.cache_resource(ttl=3600)
def get_models(lat, lon):
    df = get_long_data(lat, lon)
    data = add_features(df)
    # return the models AND the highest PM2.5 seen in training
    return train_all(data), float(data["pm2_5"].max())


st.title(f"AirSense India: {city}")

with st.spinner("Training the forecast model, this takes 30-60 seconds..."):
    models, train_max = get_models(LAT, LON)

latest, source = latest_row(LAT, LON)
now = latest.index[0]
fc = forecast(models, latest, now)
hist_df, _ = get_data(LAT, LON)
hist = hist_df["pm2_5"][hist_df.index <= now].iloc[-48:]

pm_now = float(latest["pm2_5"].iloc[0])
name, color = categorize(pm_now)

col1, col2 = st.columns(2)
col1.metric("PM2.5 now", f"{pm_now:.0f} µg/m³")
col2.metric("Category", name)

fig = go.Figure()
fig.add_trace(go.Scatter(x=hist.index, y=hist.values, mode="lines", name="Last 48 hours", line=dict(color="#7fd1ff")))
fc_sure = fc.iloc[:12]       # first 12 hours
fc_late = fc.iloc[11:]       # from hour 12 onward (overlaps one point so the line stays connected)

fig.add_trace(go.Scatter(
    x=fc_sure.index, y=fc_sure["pm2_5"],
    mode="lines",
    name="Forecast", line=dict(color="#ff9900")
))
fig.add_trace(go.Scatter(
    x=fc_late.index, y=fc_late["pm2_5"],
    mode="lines",
    name="Low confidence (beyond 12h)",
    line=dict(color="#ff9900", dash="dash")
))
fig.update_layout(title="PM2.5 forecast for the next 24 hours", yaxis_title="µg/m³")
st.plotly_chart(fig, width="stretch")

# ---- Health advice (based on the current category) ----
st.subheader(f"Health advice: air is {name} right now")
advice_cols = st.columns(len(ADVICE_GROUPS))
for col, group, text in zip(advice_cols, ADVICE_GROUPS, ADVICE[name]):
    col.markdown(
        f"""
        <div style="border-left:6px solid {color}; background:rgba(128,128,128,0.12);
                    padding:12px 14px; border-radius:8px; min-height:150px;">
            <b>{group}</b><br><br>
            <span style="font-size:0.95rem;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(f"Data: {source} | as of {now}")
st.caption("Forecasts beyond 12 hours are less reliable. Our backtest showed no improvement over a simple baseline after that.")

# Out-of-range warning: the model underestimates values above its training range
peak = max(pm_now, float(fc["pm2_5"].max()))
if peak > train_max:
    st.warning(f"PM2.5 ({peak:.0f} µg/m³) is above the highest value the model saw in training ({train_max:.0f} µg/m³). The forecast may be underestimated.")