# https://tkdocs.com/tutorial/onepage.html
# https://github.com/ParthJadhav/Tkinter-Designer 1106 x 132

from tkinter import *
from tkinter import ttk
import importlib
import Coordinates as c
import livetrack
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from tkinter.font import Font
from tkintermapview import TkinterMapView

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / 'assets' / 'frame0'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class LiveTrackHub:
    def __init__(self):
        self.window = Tk()
        self.window.title("LiveTrack Hub")
        self.setup_window()
        self.setup_canvas()
        self.setup_images()
        self.setup_clock()
        self.setup_status_box()
        self.setup_buttons()
        self.window.resizable(False, False)
        self.update_status() 
        self.map_widget = TkinterMapView(self.window, width=307, height=346, corner_radius=20)
        self.map_widget.place(x=1106, y=132)  # Adjust x and y to place the map widget at the desired location
        self.map_widget.set_position(c.me[0], c.me[1])
        self.map_widget.set_marker(c.me[0], c.me[1], text="My Location")
        self.map_widget.set_position(c.home[0], c.home[1])
        self.map_widget.set_marker(c.home[0], c.home[1], text="Home")
        self.window.mainloop()  


    def setup_window(self):
        self.window.geometry("1440x900")
        self.window.configure(bg="#000000")
        self.window.title("LiveTrack Hub")

    def setup_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#000000",
            height=900,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

    def reposition(self):
        self.map_widget.set_position(c.me[0], c.me[1])
        self.map_widget.set_marker(c.me[0], c.me[1], text="My Location")
        

    def setup_images(self):
        self.images = {
            "image_1": PhotoImage(file=relative_to_assets("image_1.png")),
            "image_2": PhotoImage(file=relative_to_assets("image_2.png")),
            "image_3": PhotoImage(file=relative_to_assets("image_3.png")),
            "image_4": PhotoImage(file=relative_to_assets("image_4.png")),
            "image_5": PhotoImage(file=relative_to_assets("image_5.png")),
            "image_6": PhotoImage(file=relative_to_assets("image_6.png")),
            "image_7": PhotoImage(file=relative_to_assets("image_7.png")),
            "image_8": PhotoImage(file=relative_to_assets("image_8.png")),
            "image_9": PhotoImage(file=relative_to_assets("image_9.png")),
        }

        self.canvas.create_image(720.0, 450.0, image=self.images["image_1"])
        self.canvas.create_image(1260.0, 689.0, image=self.images["image_2"])
        self.canvas.create_rectangle(1124.0, 565.0, 1394.0, 567.0000269030434, fill="#282C38", outline="")
        self.canvas.create_image(1260.0, 305.0, image=self.images["image_3"])
        self.canvas.create_image(690.0, 412.0, image=self.images["image_4"])
        self.canvas.create_image(856.9999964593795, 64.99999716930341, image=self.images["image_5"])
        self.canvas.create_rectangle(467.0, 53.0, 469.0000008742278, 77.0, fill="#282C38", outline="")
        self.canvas.create_rectangle(1166.0, 53.0, 1168.0000008742277, 77.0, fill="#282C38", outline="")
        self.canvas.create_rectangle(1274.0, 53.0, 1276.000000874228, 77.0, fill="#282C38", outline="")
        self.canvas.create_image(391.0, 66.0, image=self.images["image_6"])
        self.canvas.create_image(150.0, 63.0, image=self.images["image_7"])
        self.canvas.create_image(150.0, 488.0, image=self.images["image_8"])
        self.canvas.create_image(150.0, 832.0, image=self.images["image_9"])
        self.canvas.create_rectangle(24.0, 99.0, 275.0, 101.00002596456417, fill="#282C38", outline="")

    def setup_buttons(self):
        self.buttons = [
            {"image": "button_1.png", "hover": "button_hover_1.png", "x": 26.0, "y": 720.0, "command": lambda: print("button_1 clicked")},
            {"image": "button_2.png", "hover": "button_hover_2.png", "x": 26.0, "y": 664.0, "command": lambda: print("button_2 clicked")},
            {"image": "button_3.png", "hover": "button_hover_3.png", "x": 26.0, "y": 346.0, "command": lambda: print("button_3 clicked")},
            {"image": "button_4.png", "hover": "button_hover_4.png", "x": 26.0, "y": 290.0, "command": lambda: print("button_4 clicked")},
            {"image": "button_5.png", "hover": "button_hover_5.png", "x": 26.0, "y": 234.0, "command": lambda: print("button_5 clicked")},
            {"image": "button_6.png", "hover": "button_hover_6.png", "x": 26.0, "y": 178.0, "command": lambda: print("button_6 clicked")},
            {"image": "button_7.png", "hover": "button_hover_7.png", "x": 26.0, "y": 122.0, "command": self.reposition},
        ]

        for button in self.buttons:
            self.create_button(button)

        self.canvas.create_text(36.0, 637.0, anchor="nw", text="ACCOUNT", fill="#3C4254", font=("Poppins Medium", 14 * -1))

    def create_button(self, button_info):
        button_image = PhotoImage(file=relative_to_assets(button_info["image"]))
        button_hover_image = PhotoImage(file=relative_to_assets(button_info["hover"]))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=button_info["command"],
            relief="flat"
        )
        button.image = button_image  # Keep a reference to avoid garbage collection
        button.hover_image = button_hover_image  # Keep a reference to avoid garbage collection
        button.place(x=button_info["x"], y=button_info["y"], width=249.0, height=44.0)
        button.bind('<Enter>', lambda e, b=button: b.config(image=b.hover_image))
        button.bind('<Leave>', lambda e, b=button: b.config(image=b.image))


    def setup_status_box(self):
        self.status_var = StringVar()
        self.status_label = Label(
            self.window,
            textvariable=self.status_var,
            bg="#282C38",
            fg="#FFFFFF",
            font=("Poppins", 14))
        self.status_label.place(x=608, y=381, width=166, height=62)


    def update_status(self):
        """Update the status dynamically."""
        importlib.reload(c)  # Reload coordinates module to get updated data

        home_coords = c.home
        campus_coordinates = c.campus
        my_coordinates = c.me

        if livetrack.geofence(campus_coordinates, my_coordinates):
            self.status_var.set("is Home")
            self.status_label.config(bg="#246CF9")
        else:
            self.status_var.set("is Away")
            self.status_label.config(bg="#FA2256")

        self.window.after(5000, self.update_status)
    
    def setup_clock(self):
        self.clock_label = Label(
            font=("Poppins", 14),
            bg="#1D1F25",
            fg="#FFFFFF")
        self.clock_label.place(x=1180, y=50)

        self.date_label = Label(
            font=("Poppins", 14),
            bg="#1D1F25",
            fg="#FFFFFF")
        self.date_label.place(x=1280, y=50)
        self.update_clock()
    
    def update_clock(self):
        import time
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%a, %b %d")
        self.clock_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.window.after(10000, self.update_clock)


if __name__ == "__main__":
    LiveTrackHub()