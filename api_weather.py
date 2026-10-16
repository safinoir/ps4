"""Look up current weather and print a short summary using Weatherstack."""

import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


ACCESS_KEY = "661f33f7494a68fd32bfa82c98b961dc"

UNIT_OPTIONS = {
    "metric": ("m", "C", "km/h"),
    "imperial": ("f", "F", "mph"),
    "scientific": ("s", "K", "km/h"),
}


def get_weather(city, units, access_key):
    """Request current conditions for the chosen city."""
    params = urlencode({
        "access_key": access_key,
        "query": city,
        "units": UNIT_OPTIONS[units][0],
    })
    url = f"http://api.weatherstack.com/current?{params}"

    try:
        with urlopen(url, timeout=15) as response:
            data = json.load(response)
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise ValueError("Could not get weather data. Check your connection and try again.") from error

    if not isinstance(data, dict):
        raise ValueError("Weatherstack returned an unexpected response.")
    if "error" in data:
        raise ValueError(data["error"].get("info", "Weatherstack rejected the request."))
    if not isinstance(data.get("current"), dict) or not isinstance(data.get("location"), dict):
        raise ValueError("Weatherstack returned an incomplete report.")
    return data


def weather_note(description, uv_index):
    """Turn the conditions and UV index into a brief note."""
    condition = description.lower()
    if any(word in condition for word in ("thunder", "lightning")):
        note = "Thunderstorms reported. Check local weather alerts."
    elif any(word in condition for word in ("snow", "sleet", "blizzard")):
        note = "Snow or ice reported. Dress warmly and watch for slippery surfaces."
    elif any(word in condition for word in ("rain", "drizzle")):
        note = "You may want to bring an umbrella."
    elif any(word in condition for word in ("fog", "mist", "haze", "smoke")):
        note = "Visibility may be reduced. Take care when traveling."
    else:
        note = "Check conditions again before heading out."

    if uv_index >= 6:
        note += " UV is high, so use sun protection."
    return note


def print_report(data, units):
    current = data["current"]
    location = data["location"]
    _, temp_unit, wind_unit = UNIT_OPTIONS[units]
    description = (current.get("weather_descriptions") or ["Unavailable"])[0]
    uv_index = current.get("uv_index")

    print(f"\nWeather in {location.get('name', '?')}, {location.get('country', '?')}")
    print(f"Local time: {location.get('localtime', 'Unavailable')}")
    print(f"Conditions: {description}")
    print(f"Temperature: {current.get('temperature', '?')} {temp_unit}")
    print(f"Feels like: {current.get('feelslike', '?')} {temp_unit}")
    print(f"Humidity: {current.get('humidity', '?')}%")
    print(f"Wind: {current.get('wind_speed', '?')} {wind_unit}")
    print(f"UV index: {uv_index if uv_index is not None else 'Unavailable'}")

    # Interpret selected fields instead of printing the raw API response.
    print(f"\nNote: {weather_note(description, uv_index or 0)}")


def main():
    print("Current weather lookup")
    try:
        city = input("City or place: ").strip()
        while not city:
            city = input("Please enter a city or place: ").strip()

        units = input("Units (metric/imperial/scientific) [metric]: ").strip().lower() or "metric"
        while units not in UNIT_OPTIONS:
            units = input("Enter metric, imperial, or scientific: ").strip().lower()

        data = get_weather(city, units, ACCESS_KEY)
        print_report(data, units)
    except ValueError as error:
        print(f"Error: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nWeather lookup cancelled.")


if __name__ == "__main__":
    main()
