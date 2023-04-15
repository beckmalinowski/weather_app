import requests, bs4
from app import App


def main():
    weather = requests.get("https://forecast.weather.gov/MapClick.php?lat=38.973070000000064&lon=-95.23617999999999#.ZDq_6OzMIQ8")
    weather.raise_for_status()

    # soup = bs4.BeautifulSoup(weather.text, "html.parser")
    # html_temperature = soup.select(".myforecast-current-lrg")
    # temperature = html_temperature[0].get_text()

    

    # App(weather)

if __name__ == "__main__":
    main()
