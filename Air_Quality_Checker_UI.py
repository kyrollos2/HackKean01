import tkinter as tk
from Webscraping import get_aqi

def fetch_air_quality():
    city = city_entry.get()
    state = state_entry.get()
    aqi = get_aqi(city, state)

#check our api connection
 if aqi is not None:
        air_quality_label.config(text=f'The AQI in {city} is {aqi}')
        
# Check if air quality is good or bad
        if aqi < 50:
            new_window = tk.Toplevel(root)
            new_window.title("Air Quality is Good")
            new_window.configure(bg='#4496D2')
            label = tk.Label(new_window, text="The air quality is good!", font=("Arial Bold", 20))
            label.pack(padx=50, pady=50)
        else:
            new_window = tk.Toplevel(root)
            new_window.title("Air Quality is Bad")
            new_window.configure(bg='#F2220F')
            label = tk.Label(new_window, text="The air quality is bad! Make sure to wear a mask or other precaution!", font=("Arial Bold", 20))
            label.pack(padx=50, pady=50)
    else:
        air_quality_label.config(text="No air quality data available or invalid input.")

#Theese are all our data converted to a visual
root = tk.Tk()
root.title("Air Quality Checker")

frame = tk.Frame(root, bg='#D3D3D3')
frame.pack(padx=20, pady=20)

city_label = tk.Label(frame, text="Enter City:")
city_label.grid(row=0, column=0, padx=(0, 10))

city_entry = tk.Entry(frame)
city_entry.grid(row=0, column=1)

state_label = tk.Label(frame, text="Enter State (Two Letters):")
state_label.grid(row=1, column=0, padx=(0, 10), pady=(5, 0))

state_entry = tk.Entry(frame)
state_entry.grid(row=1, column=1, pady=(5, 0))

check_button = tk.Button(frame, text="Check Air Quality", command=fetch_air_quality, bg='#6EA61B')
check_button.grid(row=2, columnspan=2, pady=(10, 0))

air_quality_label = tk.Label(frame, text="")
air_quality_label.grid(row=3, columnspan=2, pady=(15, 0))

root.mainloop()
