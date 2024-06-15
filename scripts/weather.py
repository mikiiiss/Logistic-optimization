import requests
import datetime

# Define the OpenWeatherMap API key
api_key = "566d6148fa21834601bedfbc585af65c"

# Define the function to check if it rains on a date in Nigeria
def is_raining(date):
    # Convert the date to a string in the format YYYY-MM-DD
    date_str = date.strftime("%Y-%m-%d")

    # Fetch the weather data for the given date
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Nigeria&dt={date_str}&appid={api_key}")

    # Check if the API response is valid
    if response.status_code == 200:
        # Try to get the weather data from the response
        try:
            weather_data = response.json()
            # Check if it rains on the date
            if "rain" in weather_data.get("weather", [])[0].get("main", ""):
                return 1
            else:
                return 0
        except KeyError:
            # If the API response is not valid, return 0
            return 0
    else:
        # If the API response is not valid, return 0
        return 0