import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except Exception:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_current_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()


def get_forecast(city):

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()