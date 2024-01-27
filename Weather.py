import json
import tkinter as tk
import ttkbootstrap
from PIL import Image, ImageTk
import requests
from tkinter import messagebox
import io

# Function to get weather info
def get_weather(city):
    API_Key = '806f63a96ddb29c571d221d4d33222ad'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Key}'
    res = requests.get(url)
    if res.status_code == 404:
        messagebox.showerror("Error", "City not Found!")
        return None

    try:
        weather = res.json()
        icon_id = weather['weather'][0]["icon"]
        temp = weather['main']['temp'] - 273.15
        description = weather['weather'][0]['description']
        city = weather['name'].capitalize()  # Capitalize city name
        country = weather['sys']['country'].capitalize()  # Capitalize country name
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        return (icon_url, temp, description, city, country)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather information: {e}")
        return None

# Search function
def search(event=None):
    city = city_entry.get()
    result = get_weather(city)
    if result is not None:
        icon_url, temperature, description, city, country = result
        Location_label.configure(text=f"{city} , {country}")
        response = requests.get(icon_url)
        image = Image.open(io.BytesIO(response.content))
        icon = ImageTk.PhotoImage(image)
        icon_label.configure(image=icon)
        icon_label.image = icon
        tempo_label.configure(text=f"Temperature: {temperature:.2f}°C")
        desc_label.configure(text=f"Description: {description.capitalize()}")  # Capitalize description

# Create the window
win = ttkbootstrap.Window(themename="darkly")
win.title("Weather App")
win.geometry("400x400")

# Entry
city_entry = ttkbootstrap.Entry(win, font=("Helvetica", 18), justify="center")  # Centered text
city_entry.pack(pady=12)
city_entry.bind("<Return>", search)  # Bind the <Return> key to the search function

# Search button widget
search_button = ttkbootstrap.Button(win, text="Search!", command=search, bootstyle="darkly")
search_button.pack(pady=10)

# Label widget to show City
Location_label = tk.Label(win , font=('Helvetica' , 25))
Location_label.pack(pady=10)

# Label for weather Icon
icon_label = tk.Label(win)
icon_label.pack()

# Label to show the temperature
tempo_label = tk.Label(win, font=("Helvetica" , 20))
tempo_label.pack()

# Widget for description
desc_label = tk.Label(win ,font=("Helvetica" , 20))
desc_label.pack()

win.mainloop()
