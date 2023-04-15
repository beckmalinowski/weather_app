import customtkinter as ctk
import requests
import bs4


class App(ctk.CTk):
    def __init__(self, weather: requests.models.Response):
        # window setup
        super().__init__()
        self.title("Weather App")
        self.geometry("400x250")
        self.minsize(400, 250)
        self.maxsize(400, 250)
        
        self.weather = weather

        # widget config
        ctk.CTkFrame(
                self,
                width = 400,
                height = 150,
                fg_color = "purple"
        ).pack()


        # run
        self.mainloop()


    def get_weather_data(self):
        pass
