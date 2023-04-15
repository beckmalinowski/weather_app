import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests, bs4
import datetime
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
    

    def get_condition(self):
        html_condition = self._soup.select(".myforecast-current")
        return html_condition[0].get_text()
    

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
        self.geometry("400x250")
        self.minsize(400, 250)
        self.maxsize(400, 250)
        # self.iconbitmap("") TODO

        self._data = weather
        
        # will pull the current image associated with the weather conditions
        # into the assets folder.
        self._data.get_image()
        weather_photo = ImageTk.PhotoImage(
                Image.open("assets/current_image.jpg")
        )

        # TODO set appearance based on time of day

        
        # frame config
        header = ttk.Frame(self, width = 400, height = 30)
        image_frame = ttk.Frame(self, width = 100, height = 190)
        content_frame = ttk.Frame(self, width = 300, height = 190)
        footer = ttk.Frame(self, width = 400, height = 30)


        # header widgets
        ttk.Label(
                header,
                text = "Lawrence, KS",
                font = ("", H1)
        ).place(anchor = "center", relx = 0.5, rely = 0.5)

        header.pack(expand = True, fill = "both")
        

        # weather_photo
        ttk.Label(
                image_frame,
                image = weather_photo,
                text = ""
        ).pack(side = "left", expand = True, fill = "x")
        image_frame.pack(side = "left")


        # content_frame widgets
        # weather description
        ttk.Label(
                self,
                text = self._data.get_condition(),
                font = ("", H4)
        ).pack()

        # fahrenheit temperature
        ttk.Label(
                self,
                text = self._data.get_temperature_f()
        ).pack()

        content_frame.pack(expand = True, fill = "both")


        # footer widgets

        
        footer.pack(expand = True, fill = "both")

        # run
        self.mainloop()
