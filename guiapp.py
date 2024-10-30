from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from tkintermapview import TkinterMapView
import time
import live_flask
import threading
import importlib
import Coordinates as c
import livetrack
import requests  # Add for sharing toggle HTTP requests


class Application:
    def __init__(self, root):
        self.root = root
        self.is_sharing = True  # Track sharing state
        self.setup_window()
        self.setup_canvas()
        self.load_images()
        self.create_buttons()
        self.setup_clock()
        self.create_labels_with_transparency()
        self.map_widget = TkinterMapView(self.root, width=779, height=659, corner_radius=20)
        self.map_widget.place(x=301, y=132)  # Adjust x and y to place the map widget at the desired location
        self.map_widget.set_position(live_flask.fetch_coordinates('Adrien')[0], live_flask.fetch_coordinates('Adrien')[1])
        self.map_widget.set_marker(live_flask.fetch_coordinates('Adrien')[0], live_flask.fetch_coordinates('Adrien')[1], text="My Location")
         # Set up periodic map updates
        self.root.after(5000, self.update_map_position)

    def setup_window(self):
        self.root.geometry("1440x900")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

    def setup_canvas(self):
        self.canvas = Canvas(
            self.root,
            bg="#000000",
            height=900,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

    def load_images(self):
        self.assets_path = Path(__file__).parent / 'assets' / 'frame0'
        self.images = {
            "background": PhotoImage(file=self.relative_to_assets("background.png")),
            "body": PhotoImage(file=self.relative_to_assets("body.png")),
            "dashboard": PhotoImage(file=self.relative_to_assets("dashboard.png")),
            "status_panel": PhotoImage(file=self.relative_to_assets("status_panel.png")),
            #"logo": PhotoImage(file=self.relative_to_assets("logo.png")),
            "button_panel": PhotoImage(file=self.relative_to_assets("button_panel.png")),
            "button_1": PhotoImage(file=self.relative_to_assets("button_1.png")),
            "button_hover_1": PhotoImage(file=self.relative_to_assets("button_hover_1.png")),
            "button_2": PhotoImage(file=self.relative_to_assets("button_2.png")),
            "button_hover_2": PhotoImage(file=self.relative_to_assets("button_hover_2.png")),
            "button_3": PhotoImage(file=self.relative_to_assets("button_3.png")),
            "button_hover_3": PhotoImage(file=self.relative_to_assets("button_hover_3.png")),
            "button_4": PhotoImage(file=self.relative_to_assets("button_4.png")),
            "button_hover_4": PhotoImage(file=self.relative_to_assets("button_hover_4.png")),
            "button_5": PhotoImage(file=self.relative_to_assets("button_5.png")),
            "button_hover_5": PhotoImage(file=self.relative_to_assets("button_hover_5.png")),
            "isAway_1": PhotoImage(file=self.relative_to_assets("isAway_1.png")),
            "isHome_2": PhotoImage(file=self.relative_to_assets("isHome_2.png")),
            "isHome_3": PhotoImage(file=self.relative_to_assets("isHome_3.png")),
            "isHome_4": PhotoImage(file=self.relative_to_assets("isHome_4.png")),
            "isHome_5": PhotoImage(file=self.relative_to_assets("isHome_5.png")),
            # new sharing toggle button images
            "sharing_on": PhotoImage(file=self.relative_to_assets("sharing_on.png")),
            "sharing_off": PhotoImage(file=self.relative_to_assets("sharing_off.png")),
            "sharing_on_hover": PhotoImage(file=self.relative_to_assets("sharing_on_hover.png")),
            "sharing_off_hover": PhotoImage(file=self.relative_to_assets("sharing_off_hover.png"))

        }
        # Creating canvas images
        self.canvas.create_image(720.0, 450.0, image=self.images["background"])
        self.canvas.create_image(690.0, 461.0, image=self.images["body"])
        self.canvas.create_image(857.0, 64.999, image=self.images["dashboard"])
        self.canvas.create_image(1259.0, 503.0, image=self.images["status_panel"])
        #self.canvas.create_image(137.0, 106.0, image=self.images["logo"])
        self.canvas.create_image(137.0, 450.0, image=self.images["button_panel"])
        self.canvas.create_image(1259.0, 283.0, image=self.images["isAway_1"])
        self.canvas.create_image(1259.0, 413.0, image=self.images["isHome_2"])
        self.canvas.create_image(1259.0, 543.0, image=self.images["isHome_3"])
        self.canvas.create_image(1259.0, 673.0, image=self.images["isHome_4"])
        self.canvas.create_image(1259.0, 802.0, image=self.images["isHome_5"])

    def create_buttons(self):
        # Creating buttons using a helper method
        buttons_config = [
            ("button_1", "button_hover_1", (27.0, 259.0, 218.0, 58.0), "Button 1 clicked"),
            ("button_2", "button_hover_2", (27.0, 367.0, 218.0, 58.0), "Button 2 clicked"),
            ("button_3", "button_hover_3", (27.0, 473.0, 218.0, 58.0), "Button 3 clicked"),
            ("button_4", "button_hover_4", (27.0, 579.0, 218.0, 58.0), "Button 4 clicked"),
            ("button_5", "button_hover_5", (301.0, 811.0, 777.0, 42.0), "Button 5 clicked"),
            # new sharing button
            ("sharing_on", "sharing_on_hover", (27.0, 685.0, 218.0, 58.0), "toggle_sharing")
        ]
        for button_name, hover_name, geometry, command_msg in buttons_config:
            self.create_hover_button(button_name, hover_name, geometry, command_msg)

    def create_hover_button(self, button_name, hover_name, geometry, command_msg):
        command = self.toggle_sharing if command_msg == "toggle_sharing" else lambda: print(command_msg)
        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print(command_msg),
            relief="flat"
        )
        button.place(x=geometry[0], y=geometry[1], width=geometry[2], height=geometry[3])

        # Event bindings for hover effects
        if command_msg == "toggle_sharing":
            button.bind('<Enter>', lambda e: button.config(
                image=self.images["sharing_on_hover" if self.is_sharing else "sharing_off_hover"]))
            button.bind('<Leave>', lambda e: button.config(
                image=self.images["sharing_on" if self.is_sharing else "sharing_off"]))
        else:
            button.bind('<Enter>', lambda e: button.config(image=self.images[hover_name]))
            button.bind('<Leave>', lambda e: button.config(image=self.images[button_name]))

    # new methods
    def toggle_sharing(self):
        """Toggle location sharing"""
        response = requests.post(f'http://localhost:5000/toggle_sharing/Adrien')
        if response.status_code == 200:
            self.is_sharing = response.json()['sharing']
            # Update button image based on state
            button = self.find_button_by_geometry((27.0, 685.0, 218.0, 58.0))
            if button:
                button.config(
                    image=self.images["sharing_on" if self.is_sharing else "sharing_off"]
                )

    def find_button_by_geometry(self, geometry):
        """Helper method to find button by its geometry"""
        for widget in self.root.winfo_children():
            if isinstance(widget, Button):
                if (widget.winfo_x(), widget.winfo_y(), 
                    widget.winfo_width(), widget.winfo_height()) == geometry:
                    return widget
        return None

    def update_map_position(self):
        """Update map marker position"""
        try:
            coordinates = live_flask.fetch_coordinates('Adrien')
            if coordinates:
                self.map_widget.set_position(coordinates[0], coordinates[1])
                self.map_widget.set_marker(coordinates[0], coordinates[1], text="My Location")
        except Exception as e:
            print(f"Error updating map: {e}")
    
    def create_labels_with_transparency(self):
        # Adding text labels using canvas with transparent background
        labels_config = []
        for text, x, y in labels_config:
            self.canvas.create_text(
                x, y, text=text, font=("Poppins", 14), fill="#000000")

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_clock(self):
        self.update_clock()
    
    def update_clock(self):
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%a, %b %d")

        # Clear previous text before updating
        self.canvas.delete("clock_text")
        self.canvas.delete("date_text")

        # Draw the current time and date on the canvas
        self.canvas.create_text(
            1220, 65,
            text=current_time,
            font=("Poppins", 14),
            fill="#FFFFFF",
            tags="clock_text"
        )
        self.canvas.create_text(
            1340, 65,
            text=current_date,
            font=("Poppins", 14),
            fill="#FFFFFF",
            tags="date_text"
        )

        # Schedule next update
        self.root.after(60000, self.update_clock)

def run_flask():
    live_flask.app.run(host='0.0.0.0', port=5000)

def run_gui():
    window = Tk()
    app = Application(window)
    window.mainloop()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    gui_thread = threading.Thread(target=run_gui)
    flask_thread.start()
    gui_thread.start()
    gui_thread.join()
    flask_thread.join()
