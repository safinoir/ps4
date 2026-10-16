# BSC4452 Computational Rools for Research in Biology

Problem Set 4

This is a group assignment with 2-4 people per group.

For each group member, find a data source with an API--here is the Public API page I linked to in class, there are other lists, I am sure. Each group member can pick their own API and there is no need that it be Biology related, though should be appropriate. Each group member should pick a different API.

For each API, write a script (or Jupyter Notebook) to retrieve information using that API and select part of that to save/print/graph/display in a useful/interesting manner. Again the information retrieved is up to you, though you must do more than print the entire returned value.

So, one API per group member, use Python to interact with the API, do something with the returned data beyond just printing the whole raw return.

Submit as a link to a public github repository. We will try doing peer review for this assignment. I hope in addition to reviewing each other's code you will see more examples of working APIs and what can be done using them.

## Weatherstack Field Note

The script fetches current conditions from Weatherstack and prints selected fields, including temperature, humidity, wind speed, and UV index. It also interprets the conditions to give a short weather note instead of printing the entire API response.

1. Open `api_script.py` and press Run in your editor, or run `python api_script.py` in a terminal. Use a terminal-based Run option so you can type your answers.
2. Enter a city or place and choose metric, imperial, or scientific units. Press Enter at the units prompt to use metric.

Metric uses Celsius and km/h, imperial uses Fahrenheit and mph, and scientific uses Kelvin and km/h. The Weatherstack API key is set in `ACCESS_KEY` near the top of the script.

Python 3 and an internet connection are required. No extra Python packages are needed.
