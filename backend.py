import requests
import os


API_KEY = os.getenv("WEATHER_PASSWORD")

def get_data(country, place, forecast=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place},{country}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    filtered_data = data.get("list")
    filtered_data = filtered_data[:8*forecast]
    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Chanco", country="CL", forecast=1))
