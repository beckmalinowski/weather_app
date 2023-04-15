import customtkinter as ctk
import requests, bs4
from PIL import Image
import shutil
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
    

    def get_image(self):
        html_image = self._soup.find("img", class_ = "pull-left")

        image_source = html_image.attrs["src"]
        full_image_url = f"https://forecast.weather.gov/{image_source}"

        image_root = requests.get(full_image_url, stream = True)

        if image_root.status_code == 200:
           with open("assets/current_image.jpg", "wb") as f: 
              image_root.raw.decode_content = True
              shutil.copyfileobj(image_root.raw, f)


class App(ctk.CTk):
    """customtkinter app"""
    def __init__(self, weather: Weather):
        # window setup
        super().__init__()
        self.title("Weather App")
        self.geometry("400x250")
        self.minsize(400, 250)
        self.maxsize(400, 250)
        # self.iconbitmap("") TODO ico

        # TODO set appearance based on time of day

        self._data = weather
        self._data.get_image()
        weather_image = ctk.CTkImage(
                Image.open("assets/current_image.jpg"),
                size = (100, 100)
        )
        
        # layout config
        title_frame = ctk.CTkFrame(
                self,
                width = 400,
                height = 30,
                fg_color = ("#87CEEB", "#0c1445")
        )

        content_frame = ctk.CTkFrame(
                self,
                width = 400,
                height = 220,
                fg_color = ("#808080", "#5A5A5A")
        )

        # other widget config
        self._Label(
                title_frame,
                "Lawrence, KS"
        ).place(relx = 0.5, rely = 0.5, anchor = "center")

        ctk.CTkLabel(
                content_frame,
                text = "",
                image = weather_image
        ).pack()
        
        # pack
        title_frame.pack(expand = True, fill = "both")
        content_frame.pack(expand = True, fill = "both")

        # run
        self.mainloop()


    class _Label(ctk.CTkLabel):
            def __init__(self, parent, text):
                super().__init__(
                        parent,
                        text = text,
                        font = ("Calibri", 24),
                        text_color = ("black", "white"),
                )
