import streamlit as st
import pandas as pd

from weather import (
    get_current_weather,
    get_forecast
)

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Weather Dashboard",
    layout="wide"
)

st.title("🌤️ Weather Dashboard")

# -------------------------
# City Input
# -------------------------

city = st.text_input(
    "Enter City",
    value="Hyderabad"
)

# -------------------------
# Weather Button
# -------------------------

if st.button("Get Weather"):

    current = get_current_weather(city)
    forecast = get_forecast(city)

    # Error handling

    if current.get("cod") != 200:
        st.error(
            f"Unable to fetch weather data for '{city}'"
        )
        st.write(current)
        st.stop()

    # -------------------------
    # Current Weather
    # -------------------------

    st.subheader("Current Weather")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{current['main']['temp']} °C"
    )

    col2.metric(
        "Feels Like",
        f"{current['main']['feels_like']} °C"
    )

    col3.metric(
        "Humidity",
        f"{current['main']['humidity']} %"
    )

    col4.metric(
        "Wind Speed",
        f"{current['wind']['speed']} m/s"
    )

    st.write(
        f"**Condition:** {current['weather'][0]['description'].title()}"
    )

    st.divider()

    # -------------------------
    # Forecast
    # -------------------------

    st.subheader("5-Day Forecast")

    forecast_rows = []

    for item in forecast["list"]:

        forecast_rows.append({
            "Time": item["dt_txt"],
            "Temperature": item["main"]["temp"]
        })

    df = pd.DataFrame(forecast_rows)

    st.line_chart(
        df.set_index("Time")
    )

    st.divider()

    # -------------------------
    # Forecast Table
    # -------------------------

    st.subheader("Forecast Data")

    st.dataframe(
        df,
        use_container_width=True
    )