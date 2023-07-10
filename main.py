import streamlit as st
import plotly.express as px
import json
from backend import get_data


# Add page config and titles
st.set_page_config(page_title="Home",
                   page_icon="🗺",
                   layout="centered")

st.title("Weather Forecast for the Next Days")

# Add country codes box
with open("countries.json", "r") as file:
    content = file.read()
country_codes = json.loads(content)
country = st.selectbox(
    "Select country", ([key for key in country_codes.keys()]))

# Add text input, slider, select box and subheader
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place} {country}")


if place:
    # Get filtered data
    filtered_data = get_data(country=country, place=place, forecast=days)

    if option == "Temperature":
        temperatures = [temp.get("main").get("temp")
                        for temp in filtered_data]
        dates = [date.get("dt_txt") for date in filtered_data]

        # Create Temperature plot
        figure = px.line(x=dates, y=temperatures, labels={
            "x": "Date", "y": "Temperature (C)"})
        st.plotly_chart(figure)

    if option == "Sky":
        images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                  "Rain": "images/rain.png", "Snow": "images/snow.png"}
        sky_conditions = [sky.get("weather")[0].get("main")
                          for sky in filtered_data]

        # Create Skys plots
        image_paths = [images.get(sky) for sky in sky_conditions]
        st.image(image_paths, width=100)
