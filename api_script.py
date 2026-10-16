"""Fetch a live Weatherstack report and render a compact weather field note."""

import argparse
import json
import os
import sys
import textwrap
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


ENDPOINT = "http://api.weatherstack.com/current"
UNIT_OPTIONS = {
	"metric": ("m", "C", "km/h", "km", "mb"),
	"imperial": ("f", "F", "mph", "mi", "in"),
	"scientific": ("s", "K", "km/h", "km", "mb"),
}


def get_weather(query, units):
	access_key = os.environ.get("WEATHERSTACK_ACCESS_KEY")
	if not access_key:
		raise ValueError("Set WEATHERSTACK_ACCESS_KEY before running this script.")

	api_units = UNIT_OPTIONS[units][0]
	params = urlencode({"access_key": access_key, "query": query, "units": api_units})
	request_url = f"{ENDPOINT}?{params}"
	try:
		with urlopen(request_url, timeout=15) as response:
			payload = json.loads(response.read().decode("utf-8"))
	except (URLError, TimeoutError, json.JSONDecodeError) as error:
		raise ValueError("Could not retrieve a valid response from Weatherstack.") from error

	if "error" in payload:
		details = payload["error"].get("info", "Weatherstack rejected the request.")
		raise ValueError(details)
	if not isinstance(payload.get("current"), dict) or not isinstance(
		payload.get("location"), dict
	):
		raise ValueError("Weatherstack returned an incomplete weather report.")
	return payload


def meter(value, maximum, width=16):
	filled = round(max(0, min(value / maximum, 1)) * width)
	return "[" + "#" * filled + "." * (width - filled) + "]"


def interpret_weather(description, uv_index):
	condition = description.lower()
	if any(word in condition for word in ("thunder", "lightning")):
		headline, takeaway = "STORM SIGNAL", "Keep an eye on changing conditions."
	elif any(word in condition for word in ("snow", "sleet", "blizzard")):
		headline, takeaway = "WINTER WEATHER", "Warm layers and grippy shoes are a good call."
	elif any(word in condition for word in ("rain", "drizzle")):
		headline, takeaway = "WET-WEATHER MODE", "Bring a shell or umbrella for the trip."
	elif any(word in condition for word in ("fog", "mist", "haze", "smoke")):
		headline, takeaway = "LOW-VISIBILITY ALERT", "Take extra care when traveling."
	elif any(word in condition for word in ("cloud", "overcast")):
		headline, takeaway = "SOFT-LIGHT SKIES", "A comfortable day for being outdoors."
	elif any(word in condition for word in ("sunny", "clear")):
		headline, takeaway = "OPEN-SKY WINDOW", "Good conditions for time outside."
	else:
		headline, takeaway = "LOCAL WEATHER, LIVE", "Check conditions again before a long outing."

	if uv_index >= 8:
		takeaway += " UV is very high; seek shade and protect skin."
	elif uv_index >= 6:
		takeaway += " UV is high; use sun protection."
	elif uv_index >= 3:
		takeaway += " Consider sun protection around midday."
	return headline, takeaway


def render_report(payload, units):
	current = payload["current"]
	location = payload["location"]
	_, temp_unit, speed_unit, distance_unit, pressure_unit = UNIT_OPTIONS[units]
	descriptions = current.get("weather_descriptions") or ["Conditions unavailable"]
	description = descriptions[0]
	uv_index = float(current.get("uv_index") or 0)
	headline, takeaway = interpret_weather(description, uv_index)
	place = ", ".join(
		value for value in (location.get("name"), location.get("country")) if value
	) or "Unknown location"
	local_time = location.get("localtime", "Local time unavailable")
	day_label = "daytime" if current.get("is_day") == "yes" else "nighttime"

	temperature = current.get("temperature", "?")
	feels_like = current.get("feelslike", "?")
	humidity = int(current.get("humidity") or 0)
	wind_speed = float(current.get("wind_speed") or 0)
	wind_direction = current.get("wind_dir", "")
	pressure = current.get("pressure", "?")
	visibility = current.get("visibility", "?")

	lines = [
		"WEATHERSTACK  /  LIVE FIELD NOTE",
		f"{place}  |  {local_time}",
		"",
		headline,
		f"{description}  -  {day_label}",
		f"{temperature} {temp_unit}  |  feels like {feels_like} {temp_unit}",
		"",
		f"Humidity   {meter(humidity, 100)} {humidity}%",
		f"Wind       {meter(wind_speed, 60)} {wind_speed:g} {speed_unit} {wind_direction}".rstrip(),
		f"UV index   {meter(uv_index, 11)} {uv_index:g} / 11",
		f"Pressure   {pressure} {pressure_unit}  |  visibility {visibility} {distance_unit}",
		"",
		"TAKEAWAY",
	]
	lines.extend(textwrap.wrap(takeaway, width=68))
	width = max(len(line) for line in lines)
	border = "+-" + "-" * width + "-+"
	print(border)
	for line in lines:
		print(f"| {line:<{width}} |")
	print(border)


def main(argv=None):
	parser = argparse.ArgumentParser(description="Show a live Weatherstack field note.")
	parser.add_argument("city", help="City or place to look up, for example 'Tokyo'")
	parser.add_argument(
		"--units",
		choices=UNIT_OPTIONS,
		default="metric",
		help="Measurement system (default: metric)",
	)
	args = parser.parse_args(argv)

	try:
		payload = get_weather(args.city, args.units)
		render_report(payload, args.units)
	except ValueError as error:
		print(f"Error: {error}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
