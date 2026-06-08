import streamlit as st
import pandas as pd
from datetime import datetime, timezone



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

    timezone_offset = current["timezone"]

    sunrise_time = datetime.fromtimestamp(
        current["sys"]["sunrise"] + timezone_offset,
        tz=timezone.utc
    )

    sunset_time = datetime.fromtimestamp(
        current["sys"]["sunset"] + timezone_offset,
        tz=timezone.utc
    )

    # -------------------------
    # Error Handling
    # -------------------------

    if current is None:
        st.error("Unable to fetch weather data.")
        st.stop()

    if current.get("cod") != 200:
        st.error(
            f"Unable to fetch weather data for '{city}'"
        )
        st.json(current)
        st.stop()

    # -------------------------
    # Current Weather
    # -------------------------

    st.subheader("Current Weather")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

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
    col5.metric(
    "Sunrise",
    sunrise_time.strftime("%H:%M")
    )

    col6.metric(
        "Sunset",
        sunset_time.strftime("%H:%M")
    )

    st.write(
        f"**Condition:** {current['weather'][0]['description'].title()}"
    )

    st.divider()

    # -------------------------
    # Forecast
    # -------------------------

    if forecast and "list" in forecast:

        forecast_rows = []

        for item in forecast["list"]:

            forecast_rows.append({
                "Time": item["dt_txt"],
                "Temperature": item["main"]["temp"]
            })

        df = pd.DataFrame(forecast_rows)

        st.subheader("5-Day Forecast")

        st.line_chart(
            df.set_index("Time")
        )

        st.divider()

        st.subheader("Forecast Data")

        st.dataframe(
            df,
            width="stretch"
        )