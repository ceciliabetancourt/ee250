import requests
import json
import vm_sub

# weatherAPI key
WEATHER_API_KEY = 'b7332961c3ec4349a4644114252309'

def get_weather(city):
    # (1) build the API request URL using the base API endpoint, the API key, and the city 
    # chosen with the potentiometer
    API_BASE_URL = 'https://api.weatherapi.com/v1/current.json'
    request_url = f"{API_BASE_URL}?key={WEATHER_API_KEY}&q={city}"

    # (2) make the HTTP request to fetch weather data using the 'requests' library
    response = requests.get(request_url)
    json_weather_data = response.json()

    # (3) handle HTTP status codes
    if response.status_code == 200: # request was successful
        # figure out what values we need specifically
        # current temperature (F)
        current_temp = json_weather_data['current']['temp_c']
        # "feels like" temperature
        feel_temp = json_weather_data['current']['feelslike_c']
        # weather condition (e.g., sunny, cloudy, rainy)
        weather_cond = json_weather_data['current']['condition']['text']
        # humidity percentage
        humidity = json_weather_data['current']['humidity']
        # wind speed and direction
        wind_speed = json_weather_data['current']['wind_kph']
        direction = json_weather_data['current']['wind_dir']
        # atmospheric pressure (mb)
        pressure = json_weather_data['current']['pressure_mb']
        # UV Index value
        uv = json_weather_data['current']['uv']
        # cloud cover percentage
        cloud = json_weather_data['current']['cloud']
        # visibility (miles)
        visibility = json_weather_data['current']['vis_miles']  
    else:
        # request was not successful
        print(f"Error: {response.status_code}. Something went wrong.")

if __name__ == '__main__':
    # call the 'get_weather' function with the city name published in the broker
    get_weather(vm_sub.latest_city)
    pass
