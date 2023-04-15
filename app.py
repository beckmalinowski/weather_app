from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests, bs4
from datetime import datetime
import shutil


H1 = 30
H2 = 26
H3 = 20
H4 = 18
H5 = 13
H6 = 10


class Weather:
    """manages weather data for App instance."""
    def __init__(self, browser: requests.models.Response):
        self._soup = bs4.BeautifulSoup(browser.text, "html.parser")
       

    def get_temperature_f(self):
        html_temperature = self._soup.select(".myforecast-current-lrg")
        return html_temperature[0].get_text()



    def get_temperature_c(self):
        html_temperature = self._soup.select(".myforecast-current-sm")
        return html_temperature[0].get_text()
    

    def get_condition(self):
        html_condition = self._soup.select(".myforecast-current")
        return html_condition[0].get_text()
    

    def get_humidity(self):
        html_humidity = self._soup.find_all("td")
        return html_humidity[1].get_text()


    def get_windspeed(self):
        html_humidity = self._soup.find_all("td")
        return html_humidity[3].get_text()


    def get_dewpoint(self):
        html_humidity = self._soup.find_all("td")
        return html_humidity[7].get_text()


    def get_wind_chill(self):
        html_humidity = self._soup.find_all("td")
        return html_humidity[11].get_text()


    def get_image(self):
        html_image = self._soup.find("img", class_ = "pull-left")
        image_source = html_image.attrs["src"]
        full_image_url = f"https://forecast.weather.gov/{image_source}"
        image_root = requests.get(full_image_url, stream = True)

        if image_root.status_code == 200:
           with open("assets/current_image.jpg", "wb") as f: 
              image_root.raw.decode_content = True
              shutil.copyfileobj(image_root.raw, f)


class App(ttk.Window):
    """tkinter app"""
    def __init__(self, weather: Weather):
        # window setup
        super().__init__(themename = "vapor")
        self.title("Weather App")
        self.geometry("500x250")
        self.minsize(500, 250)
        self.maxsize(500, 250)
        # self.iconbitmap("") TODO

        current_time = datetime.now().strftime("%H:%M:%S")
        self._data = weather
        
        # will pull the current image associated with the weather conditions
        # into the assets folder.
        self._data.get_image()
        weather_photo = ImageTk.PhotoImage(
                Image.open("assets/current_image.jpg")
        )

        # TODO set appearance based on time of day
        
        # frame config
        header = ttk.Frame(self, width = 500, height = 30)

        content_frame = ttk.Frame(self, width = 500, height = 190)
        content_frame.columnconfigure((0, 1, 2), weight = 1, uniform = 'a')
        content_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1, uniform = 'a')

        footer = ttk.Frame(self, width = 500, height = 30)


        # header widgets
        location = ttk.Label(header, text = "Lawrence, KS", font = ("", H1))
        location.place(anchor = "center", relx = 0.5, rely = 0.5)
        
        self.time_text = ttk.Label(header, text = current_time, font = ("", H3))

        header.pack(expand = True, fill = "both")
        

        # weather_photo
        ttk.Label(
                content_frame,
                image = weather_photo,
                text = ""
        ).grid(row = 0, column = 0, rowspan = 7, sticky = "nws")


        # content_frame widgets
        # weather description
        weather_condition = ttk.Label(content_frame, text = self._data.get_condition(), font = ("", H4))
        weather_condition.grid(row = 1, column = 1, columnspan = 3, sticky = "nws", padx = 2)

        # fahrenheit temperature
        fahrenheit = ttk.Label(content_frame, text = self._data.get_temperature_f(), font = ("", H2))
        fahrenheit.grid(row = 2, column = 1, sticky = "nws", padx = 2)

        # celsius temperature
        fahrenheit = ttk.Label(content_frame, text = f"({self._data.get_temperature_c()})", font = ("", H3))
        fahrenheit.grid(row = 3, column = 1, sticky = "nws", padx = 2)


        humidity = ttk.Label(content_frame, text = f"Humidity: {self._data.get_humidity()}", font = ("", H6))
        humidity.grid(row = 2, column = 2, sticky = "es")

        wind_speed = ttk.Label(content_frame, text = f"Wind Speed: {self._data.get_windspeed()}", font = ("", H6))
        wind_speed.grid(row = 3, column = 2, sticky = "es")

        dewpoint = ttk.Label(content_frame, text = f"Dewpoint: {self._data.get_dewpoint()}", font = ("", H6))
        dewpoint.grid(row = 4, column = 2, sticky = "es")

        wind_chill = ttk.Label(content_frame, text = f"Wind Chill: {self._data.get_wind_chill()}", font = ("", H6))
        wind_chill.grid(row = 5, column = 2, sticky = "es")


        
        self.time_text.pack(side = "right")
        content_frame.pack(expand = True, fill = "both")

        footer.pack(expand = True, fill = "both")

        # run
        self.update_time()
        self.mainloop()
    

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")

        #Use the config method of message to update the text
        self.time_text.config(text = current_time)
        self.after(1000, self.update_time)
