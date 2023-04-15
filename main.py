import requests, bs4
from app import Weather
from app import App


def main():
    root = requests.get("https://forecast.weather.gov/MapClick.php?lat=38.973070000000064&lon=-95.23617999999999#.ZDq_6OzMIQ8")
    root.raise_for_status()
    weather_data = Weather(root)
    App(weather_data)


if __name__ == "__main__":
    main()
