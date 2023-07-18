import streamlit as st
import plotly.express as px
import json
from backend import get_data
from datetime import date


# Add page config and titles
st.set_page_config(page_title="Home",
                   page_icon="🗺",
                   layout="centered")

st.title("Pronóstico del Tiempo")

# Add country codes box
with open("countries.json", "r") as file:
    content = file.read()
country_codes = json.loads(content)
country = st.selectbox(
    "Seleccione un país", ([key for key in country_codes.keys()]),
    help="Elija un país")

# Add text input, slider, select box and subheader
place = st.text_input("Lugar: ", help="Ejemplo: Santiago")
days = st.slider("Días pronosticados", min_value=1, max_value=5,
                 help="Seleccione el número de días para el pronóstico")
option = st.selectbox(
    "Seleccione el formato del pronóstico", ("Temperatura", "Cielos"))
st.subheader(f"{option} para los próximos {days} días en {place} {country}")

if place:
    try:
        # Get filtered data
        filtered_data = get_data(country=country, place=place, forecast=days)

        if option == "Temperatura":
            temperatures = [temp.get("main").get("temp")
                            for temp in filtered_data]
            dates = [date.get("dt_txt") for date in filtered_data]

            # Create Temperature plot
            figure = px.line(x=dates, y=temperatures, labels={
                "x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Cielos":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            dates = [date.get("dt_txt") for date in filtered_data]
            sky_conditions = [sky.get("weather")[0].get("main")
                              for sky in filtered_data]

            # Create Skys plots
            image_paths = [images.get(sky) for sky in sky_conditions]

            # Code for the image labels (must be improve)
            img_label = [date(day=int(dates[i][8:10]),
                              month=int(dates[i][5:7]),
                              year=int(dates[i][0:4])).
                         strftime(f'%a, %b %d {dates[i][11:-3]}')
                         for i in range(days*8)]

            st.image(image_paths, width=100, caption=img_label)
    except TypeError:
        st.error(
            "You entered a place that does not exist, please try again!!", icon="🚨")
