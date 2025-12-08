# note ––> we're using the following API: https://www.weatherapi.com
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
        # latitude
        latitude = json_weather_data['location']['lat']
        # longitude
        longitude = json_weather_data['location']['lon']
    else:
        # request was not successful
        print(f"Error: {response.status_code}. Something went wrong.")

if __name__ == '__main__':
    # call the 'get_weather' function with the city name published in the broker
    get_weather(vm_sub.latest_city)
    pass
