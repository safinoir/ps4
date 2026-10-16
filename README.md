# BSC4452 Computational Rools for Research in Biology

Problem Set 4

This is a group assignment with 2-4 people per group.

For each group member, find a data source with an API--here is the Public API page I linked to in class, there are other lists, I am sure. Each group member can pick their own API and there is no need that it be Biology related, though should be appropriate. Each group member should pick a different API.

For each API, write a script (or Jupyter Notebook) to retrieve information using that API and select part of that to save/print/graph/display in a useful/interesting manner. Again the information retrieved is up to you, though you must do more than print the entire returned value.

So, one API per group member, use Python to interact with the API, do something with the returned data beyond just printing the whole raw return.

Submit as a link to a public github repository. We will try doing peer review for this assignment. I hope in addition to reviewing each other's code you will see more examples of working APIs and what can be done using them.

## Weatherstack Field Note

The script fetches current conditions from Weatherstack and turns selected fields into a compact field note with visual meters and a condition-based takeaway.

1. Create a Weatherstack account and get an access key.
2. Set the key in your shell as `WEATHERSTACK_ACCESS_KEY`.
3. Run `python api_script.py "Tokyo"`.

Use `--units imperial` for Fahrenheit and miles, or `--units scientific` for Kelvin. Metric units are the default. The API key is read from the environment and should not be committed to the repository.