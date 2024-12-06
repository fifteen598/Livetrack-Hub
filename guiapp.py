from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from tkintermapview import TkinterMapView
import time
import live_flask
import threading
import importlib
import Coordinates as c
import livetrack


class Application:
    def __init__(self, root):
        self.root = root
        self.user_names = [] # List of names
        self.status_labels = [] # List of status labels
        self.setup_window()
        self.setup_canvas()
        self.load_images()
        self.create_buttons()
        self.setup_clock()
        self.create_status_labels()
        self.update_user_statuses()
        self.create_labels_with_transparency()
        self.map_widget = TkinterMapView(self.root, width=739, height=619, corner_radius=20)
        self.map_widget.place(x=321, y=152)  # Adjust x and y to place the map widget at the desired location
        self.map_widget.set_position(live_flask.fetch_coordinates('Adrien')[0], live_flask.fetch_coordinates('Adrien')[1])
        self.map_widget.set_marker(live_flask.fetch_coordinates('Adrien')[0], live_flask.fetch_coordinates('Adrien')[1], text="Adrien")

    def setup_window(self):
        self.root.geometry("1440x900")
        self.root.configure(bg="#000000")
        self.root.title("LiveTrack Hub")
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
        }
        for i in range(1, 6):
            self.images[f"isHome_{i}"] = PhotoImage(file=self.relative_to_assets(f"isHome_{i}.png"))
            self.images[f"isAway_{i}"] = PhotoImage(file=self.relative_to_assets(f"isAway_{i}.png"))

        # Creating canvas images
        self.canvas.create_image(720.0, 450.0, image=self.images["background"])
        self.canvas.create_image(690.0, 461.0, image=self.images["body"])
        self.canvas.create_image(857.0, 64.999, image=self.images["dashboard"])
        self.canvas.create_image(1259.0, 503.0, image=self.images["status_panel"])
        self.canvas.create_image(137.0, 450.0, image=self.images["button_panel"])

    def create_status_labels(self):
        y_positions = [283.0, 413.0, 543.0, 673.0, 802.0]  # Y-coordinates for each user
        self.user_statuses = {}  # Store references to each status image

        users = live_flask.fetch_records()

        for i, (user, coords) in enumerate(users.items(), start=1):
            if i > len(y_positions):  # Limit to the number of positions available
                break
            status_image = self.canvas.create_image(1259.0, y_positions[i - 1], image=self.images[f"isAway_{i}"])
            self.user_statuses[user] = status_image

            self.canvas.create_text(
                1164, y_positions[i - 1] - 30,
                text=f"{user}",
                font=("Poppins", 14),
                fill="#FFFFFF",
                tags="f{user}_label"
            )

    def update_user_statuses(self):
        home_coords = (37.71783399900819, -97.29209838253563)
        # Example users and coordinates
        users = live_flask.fetch_records()
        
        y_positions = [283.0, 413.0, 543.0, 673.0, 802.0]
        for i, (user, coords) in enumerate(users.items(), start=1):
            if i>5: 
                break


            # Check if the user is within the geofence
            if livetrack.geofence(coords, home_coords):
                # Update canvas image to "isHome"
                if user in self.user_statuses:
                    self.canvas.itemconfig(self.user_statuses[user], image=self.images[f"isHome_{i}"])
                else:
                    print(f"User '{user}' not found in status labels.")
            else:
                # Update canvas image to "isAway"
                if user in self.user_statuses:
                    self.canvas.itemconfig(self.user_statuses[user], image=self.images[f"isAway_{i}"])
                else:
                    print(f"User '{user}' not found in status labels.")

            if f"{user}_label" not in self.canvas.find_withtag(f"{user}_label"):
                self.canvas.create_text(
                    1164, y_positions[i - 1] - 30,
                    text=user,
                    font=("Poppins", 14),
                    fill="#FFFFFF",
                    tags=f"{user}_label"
                )

        for i in range(len(users) +1, 6):
            self.canvas.delete(self.user_statuses.get(f"user_{i}", None))
            self.canvas.delete(f"user_{i}_label")

        self.root.after(5000, self.update_user_statuses)

    def create_buttons(self):
        # Creating buttons using a helper method
        buttons_config = [
            ("button_1", "button_hover_1", (27.0, 259.0, 218.0, 58.0), "Button 1 clicked"),
            ("button_2", "button_hover_2", (27.0, 367.0, 218.0, 58.0), "Button 2 clicked"),
            ("button_3", "button_hover_3", (27.0, 473.0, 218.0, 58.0), "Button 3 clicked"),
            ("button_4", "button_hover_4", (27.0, 579.0, 218.0, 58.0), "Button 4 clicked"),
            ("button_5", "button_hover_5", (301.0, 811.0, 777.0, 42.0), "Button 5 clicked"),
        ]
        for button_name, hover_name, geometry, command_msg in buttons_config:
            self.create_hover_button(button_name, hover_name, geometry, command_msg)

    def create_hover_button(self, button_name, hover_name, geometry, command_msg):
        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print(command_msg),
            relief="flat"
        )
        button.place(x=geometry[0], y=geometry[1], width=geometry[2], height=geometry[3])

        # Event bindings for hover effects
        button.bind('<Enter>', lambda e: button.config(image=self.images[hover_name]))
        button.bind('<Leave>', lambda e: button.config(image=self.images[button_name]))

    def create_labels_with_transparency(self):
        # Adding text labels using canvas with transparent background
        labels_config = []
        for text, x, y in labels_config:
            self.canvas.create_text(
                x, y, text=text, font=("Poppins", 24), fill="#000000")

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

#def run_flask():
    #live_flask.app.run(host='0.0.0.0', port=5000)

def run_gui():
    window = Tk()
    app = Application(window)
    window.mainloop()

if __name__ == "__main__":
    #flask_thread = threading.Thread(target=run_flask)
    gui_thread = threading.Thread(target=run_gui)
    #flask_thread.start()
    gui_thread.start()
    gui_thread.join()
    #flask_thread.join()
