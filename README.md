# Google Flights Scraper

A Python script that automates the process of searching and scraping flight information from Google Flights for a given pair of cities.

## Usage

```python
from google_flights_scraper import get_flight_data

city_from = "New York"
city_to = "London"
flights_df = get_flight_data(city_from, city_to)
print(flights_df)
```

## Expected Results

The script returns a pandas DataFrame containing the following information for various flight combinations:

- Origin and destination cities
- Best departure and return dates
- Outbound flight details (airline, departure time, arrival time, duration, stops, luggage allowance)
- Return flight details (airline, departure time, arrival time, duration, stops, luggage allowance)
- Total price

## Disclaimer

This script relies on specific HTML elements and their attributes on the Google Flights website. Due to potential changes in the website's structure or differences in rendering across various environments, the script may not work consistently on all systems or may require periodic updates to maintain functionality.

## Note

Web scraping may be subject to legal and ethical considerations. Always ensure compliance with the website's terms of service.