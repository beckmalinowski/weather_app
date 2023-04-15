import requests
from app import Weather, App


def main():
    # hardcoded to use the weather for Lawrence, KS. May implement
    # a way to search using selenium later
    root = requests.get("https://forecast.weather.gov/MapClick.php?lat=38.973070000000064&lon=-95.23617999999999#.ZDq_6OzMIQ8")
    root.raise_for_status()
    weather_data = Weather(root)
    App(weather_data)


if __name__ == "__main__":
    main()
