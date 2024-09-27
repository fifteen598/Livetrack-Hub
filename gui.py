# https://tkdocs.com/tutorial/onepage.html
from tkinter import *
from tkinter import ttk
import importlib
import Coordinates as c
import livetrack

def create_gui():
    root = Tk()
    root.title("LiveTrack Hub")

    root.geometry("400x300")
    root.config(bg="#353537")

    title_label = ttk.Label(root, text="LiveTrack Hub", font=("Impact", 30), foreground="#f2f2f2", background="#353537")
    title_label.pack(pady=10)

    status = StringVar()
    status_label = Label(root, textvariable = status, font=("Georgia", 18, "bold"), fg="#f2f2f2", bg="#6bd432")
    status_label.pack(pady=20)

    def update_status():
        importlib.reload(c)
        home_coordinates = c.home
        campus_coordinates = c.campus
        my_coordinates = c.me

        if livetrack.geofence(campus_coordinates, my_coordinates):
            status.set("Home")
            status_label.config(bg="#6bd432")
        else:
            status.set("Away")
            status_label.config(bg="#d4173f")

        root.after(5000, update_status) # Recursive loop that re-calls update_status every 5 seconds

    update_status()
    root.mainloop()

if __name__ == "__main__":
    create_gui()

                         
