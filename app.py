import customtkinter as ctk
import requests, bs4
import datetime


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
    

    def get_current_image(self):
        pass


class App(ctk.CTk):
    """customtkinter app"""
    def __init__(self, weather: Weather):
        # window setup
        super().__init__()
        self.title("Weather App")
        self.geometry("400x250")
        self.minsize(400, 250)
        self.maxsize(400, 250)

        self._data = weather
        
        # widget config
        title_frame = ctk.CTkFrame(
                self,
                width = 400,
                height = 50,
                fg_color = "#87CEEB"
        )

        self._Label(
                title_frame,
                "Lawrence, KS"
        ).pack()

        title_frame.pack(expand = True, fill = "both")

        # run
        self.mainloop()


    class _Label(ctk.CTkLabel):
            def __init__(self, parent, text):
                super().__init__(
                        parent,
                        text = text,
                        font = ("Calibri", 24),
                )
