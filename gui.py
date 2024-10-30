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
import live_flask
import threading
import requests  # Added for making HTTP requests to toggle sharing

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / 'assets' / 'frame0_b'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class LiveTrackHub:
    def __init__(self):
        self.window = Tk()
        self.window.title("LiveTrack Hub")
        # Added to track sharing state locally
        self.is_sharing = True  # Default to True when app starts
        self.setup_window() #
        self.setup_canvas() #
        self.setup_images()
        self.setup_clock()
        self.setup_status_box()
        self.setup_buttons()
        self.window.resizable(False, False)
        self.update_status() 
        self.setup_map()  # Separated map setup for better organization
        self.map_widget = TkinterMapView(self.window, width=307, height=346, corner_radius=20)
        self.map_widget.place(x=1106, y=132)  # Adjust x and y to place the map widget at the desired location
        self.map_widget.set_position(live_flask.fetch_coordinates('Adrien')[0], live_flask.fetch_coordinates('Adrien')[1])
        self.map_widget.set_marker(live_flask.fetch_coordinates('Adrien')[0], live_flask.fetch_coordinates('Adrien')[1], text="My Location")
        self.window.mainloop()

    # New method to separate map setup logic
    def setup_map(self):
        self.map_widget = TkinterMapView(self.window, width=307, height=346, corner_radius=20)
        self.map_widget.place(x=1106, y=132)
        self.update_map_position()

    # New method to handle map position updates
    def update_map_position(self):
        coordinates = live_flask.fetch_coordinates('Adrien')
        if coordinates:  # Only update if we have valid coordinates
            self.map_widget.set_position(coordinates[0], coordinates[1])
            self.map_widget.set_marker(coordinates[0], coordinates[1], text="My Location")

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
        coordinates = live_flask.fetch_coordinates('Adrien')
        if coordinates:  # Only update if we have valid coordinates
            self.map_widget.set_position(coordinates[0], coordinates[1])
            self.map_widget.set_marker(coordinates[0], coordinates[1], text="My Location")
        

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
            # New images for sharing toggle button
            "sharing_on": PhotoImage(file=relative_to_assets("sharing_on.png")),
            "sharing_off": PhotoImage(file=relative_to_assets("sharing_off.png")),
            "sharing_on_hover": PhotoImage(file=relative_to_assets("sharing_on_hover.png")),
            "sharing_off_hover": PhotoImage(file=relative_to_assets("sharing_off_hover.png"))
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

    # New method to handle location sharing toggle
    def toggle_sharing(self):
        """Toggle location sharing and update UI accordingly"""
        response = requests.post(f'http://localhost:5000/toggle_sharing/Adrien')
        if response.status_code == 200:
            self.is_sharing = response.json()['sharing']
            # Update sharing button image
            self.sharing_button.config(
                image=self.images["sharing_on"] if self.is_sharing else self.images["sharing_off"]
            )
            # Update status immediately
            if not self.is_sharing:
                self.status_var.set("Sharing Off")
                self.status_label.config(bg="#808080")
            else:
                self.update_status()  # Refresh status if sharing is turned back on

    def setup_buttons(self):
        self.buttons = [
            {"image": "button_1.png", "hover": "button_hover_1.png", "x": 26.0, "y": 720.0, "command": lambda: print("button_1 clicked")},
            {"image": "button_2.png", "hover": "button_hover_2.png", "x": 26.0, "y": 664.0, "command": lambda: print("button_2 clicked")},
            {"image": "button_3.png", "hover": "button_hover_3.png", "x": 26.0, "y": 346.0, "command": lambda: print("button_3 clicked")},
            {"image": "button_4.png", "hover": "button_hover_4.png", "x": 26.0, "y": 290.0, "command": lambda: print("button_4 clicked")},
            {"image": "button_5.png", "hover": "button_hover_5.png", "x": 26.0, "y": 234.0, "command": lambda: print("button_5 clicked")},
            {"image": "button_6.png", "hover": "button_hover_6.png", "x": 26.0, "y": 178.0, "command": lambda: print("button_6 clicked")},
            {"image": "button_7.png", "hover": "button_hover_7.png", "x": 26.0, "y": 122.0, "command": self.reposition},
            # Add sharing toggle button to the regular button list
            {"image": "sharing_on.png", "hover": "sharing_on_hover.png", "x": 26.0, "y": 776.0, "command": self.toggle_sharing}
        ]

        for button in self.buttons:
            self.create_button(button)

        # Create sharing toggle button separately
        self.sharing_button = Button(
            image=self.images["sharing_on"],
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_sharing,
            relief="flat"
        )
        self.sharing_button.place(x=26.0, y=776.0, width=249.0, height=44.0)
        
        # Add hover effects for sharing button
        self.sharing_button.bind('<Enter>', self.on_sharing_hover)
        self.sharing_button.bind('<Leave>', self.on_sharing_leave)

        self.canvas.create_text(36.0, 637.0, anchor="nw", text="ACCOUNT", fill="#3C4254", font=("Poppins Medium", 14 * -1))

     # New methods for sharing button hover effects
    def on_sharing_hover(self, event):
        """Handle hover effect for sharing button"""
        self.sharing_button.config(
            image=self.images["sharing_on_hover"] if self.is_sharing 
            else self.images["sharing_off_hover"]
        )

    def on_sharing_leave(self, event):
        """Handle hover leave effect for sharing button"""
        self.sharing_button.config(
            image=self.images["sharing_on"] if self.is_sharing 
            else self.images["sharing_off"]
        )

    # Modified update_status to handle sharing state
    def update_status(self):
        """Update the status dynamically."""
        try:
            coordinates = live_flask.fetch_coordinates('Adrien')
            
            if coordinates is None:  # Sharing is disabled or error fetching coordinates
                self.status_var.set("Sharing Off")
                self.status_label.config(bg="#808080")
            else:
                campus_coordinates = c.campus_coordinates
                if livetrack.geofence(campus_coordinates, coordinates):
                    self.status_var.set("is Home")
                    self.status_label.config(bg="#246CF9")
                else:
                    self.status_var.set("is Away")
                    self.status_label.config(bg="#FA2256")
                
                # Update map if sharing is enabled
                self.update_map_position()
                
        except Exception as e:
            print(f"Error updating status: {e}")
            
        self.window.after(5000, self.update_status)
        
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

        campus_coordinates = c.campus_coordinates
        my_coordinates = live_flask.fetch_coordinates('Adrien')

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

def run_flask():
    live_flask.app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    gui_thread = threading.Thread(target=LiveTrackHub())

