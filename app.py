import tkinter as tk
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
        header = ttk.Frame(self, width = 400, height = 30)

        content_frame = ttk.Frame(self, width = 400, height = 190)
        content_frame.columnconfigure(0, weight = 1, uniform = 'a') # index, weight
        content_frame.columnconfigure(1, weight = 2, uniform = 'a') # index, weight
        content_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1, uniform = 'a')

        footer = ttk.Frame(self, width = 400, height = 30)


        # header widgets
        ttk.Label(
                header,
                text = "Lawrence, KS",
                font = ("", H1)
        ).place(anchor = "center", relx = 0.5, rely = 0.5)
        
        self.time_text = ttk.Label(
                header,
                text = current_time,
                font = ("", H3)
        )

        header.pack(expand = True, fill = "both")
        

        # weather_photo
        ttk.Label(
                content_frame,
                image = weather_photo,
                text = ""
        ).grid(row = 0, column = 0, rowspan = 7, sticky = "nws")


        # content_frame widgets
        # weather description
        ttk.Label(
                content_frame,
                text = self._data.get_condition(),
                font = ("", H4)
        ).grid(row = 1, column = 1, columnspan = 3, sticky = "nws", padx = 2)

        # fahrenheit temperature
        ttk.Label(
                content_frame,
                text = self._data.get_temperature_f(),
                font = ("", H2)
        ).grid(row = 2, column = 1, sticky = "nws", padx = 2)

        self.time_text.pack(side = "right")
        content_frame.pack(expand = True, fill = "both")


        # footer widgets

        
        footer.pack(expand = True, fill = "both")

        # run
        self.update_time()
        self.mainloop()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")

        #Use the config method of message to update the text
        self.time_text.config(text = current_time)
        self.after(1000, self.update_time)
