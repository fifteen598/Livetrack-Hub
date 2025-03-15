from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Label, Entry, Toplevel
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
        self.setup_window()
        self.setup_canvas()
        self.load_images()
        self.user_manager = UserStatus(canvas=self.canvas, images=self.images, y_positions=[283.0, 413.0, 543.0, 673.0, 802.0])
        self.create_buttons()
        self.setup_clock()
        self.update_user_statuses()
        self.create_labels_with_transparency()
        self.map_widget = TkinterMapView(self.root, width=739, height=619, corner_radius=20)
        self.map_widget.place(x=321, y=152)  # Adjust x and y to place the map widget at the desired location
        self.update_map()
        # self.myx = live_flask.fetch_coordinates('Adrien')[0]
        # self.myy = live_flask.fetch_coordinates('Adrien')[1]
        # self.map_widget.set_position(self.myx, self.myy, 15)
        # self.map_widget.set_marker(self.myx, self.myy, text="Adrien")

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

    def update_user_statuses(self):
        users = live_flask.fetch_records()
        home_coords = (37.71783399900819, -97.29209838253563)
        self.user_manager.create_status_labels(users)
        self.user_manager.update_status_labels(users, home_coords)
        self.root.after(5000, self.update_user_statuses)

    def create_buttons(self):
        # Creating buttons using a helper method
        buttons_config = [
            ("button_1", "button_hover_1", (27.0, 259.0, 218.0, 58.0), "Button 1 clicked"),
            ("button_2", "button_hover_2", (27.0, 367.0, 218.0, 58.0), "Button 2 clicked"),
            ("button_3", "button_hover_3", (27.0, 473.0, 218.0, 58.0), "Button 3 clicked"),
            ("button_4", "button_hover_4", (27.0, 579.0, 218.0, 58.0), "Button 4 clicked"),
            ("button_5", "button_hover_5", (301.0, 811.0, 777.0, 42.0), self.set_geofence)
        ]
        for button_name, hover_name, geometry, command_msg in buttons_config:
            self.create_hover_button(button_name, hover_name, geometry, command_msg)

    def set_geofence(self):
        # Create a popup window
        popup = Toplevel(self.root)
        popup.title("Set Geofence Location")
        popup.geometry("400x200")

        # Add label and entry for address input
        Label(popup, text="Enter Address:").pack(pady=10)
        address_entry = Entry(popup, width=40)
        address_entry.pack(pady=10)

        # Button to fetch and update coordinates
        def submit_address():
            address = address_entry.get()
            coords = livetrack.get_coords(address)
            if coords:
                # Update home_coords and notify the user
                self.user_manager.home_coords = coords
                Label(popup, text=f"Geofence set to: {coords}", fg="green").pack(pady=10)
                self.map_widget.set_position(coords[0], coords[1], 15)
                self.map_widget.set_marker(coords[0], coords[1], text="Home")
            else:
                Label(popup, text="Failed to fetch coordinates.", fg="red").pack(pady=10)

        Button(popup, text="Set Geofence", command=submit_address).pack(pady=10)        

    def create_hover_button(self, button_name, hover_name, geometry, command):
        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: command() if callable(command) else print(command),
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

    def update_map(self):
        users = live_flask.fetch_records()  # Fetch all user records
        home_coords = (37.71783399900819, -97.29209838253563)  # Define home coordinates

        self.map_widget.delete_all_marker()  # Clear existing markers
        for user, coords in users.items():
            self.map_widget.set_marker(coords[0], coords[1], text=user)  # Add a marker for each user
            if user == "Adrien":  # Optionally focus the map on a specific user
                self.map_widget.set_position(coords[0], coords[1], 15)

        self.root.after(5000, self.update_map)

class UserStatus:
    def __init__(self, canvas, images, y_positions):
        self.canvas = canvas
        self.images = images
        self.y_positions = y_positions
        self.user_statuses = {}

    def create_status_labels(self, users):
        self.clear_all_status_labels() # Y-coordinates for each user
        users = live_flask.fetch_records()

        for i, (user, coords) in enumerate(users.items(), start=1):
            if i > len(self.y_positions):  # Limit to the number of positions available
                break
            status_image = self.canvas.create_image(1259.0, self.y_positions[i - 1], image=self.images[f"isAway_{i}"])
            self.user_statuses[user] = status_image

            self.canvas.create_text(
                1175, self.y_positions[i - 1] - 17,
                text=f"{user}",
                font=("Poppins", 14),
                fill="#FFFFFF",
                tags="f{user}_label",
                anchor="w"
            )

    def update_status_labels(self, users, home_coords):
        for i, (user, coords) in enumerate(users.items(), start=1):
            if i > len(self.y_positions):  # Limit to available positions
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

            # Ensure the label for this user exists
            # if f"{user}_label" not in self.canvas.find_withtag(f"{user}_label"):
            #     self.canvas.create_text(
            #         1164, self.y_positions[i - 1] -30,
            #         text=user,
            #         font=("Poppins", 14),
            #         fill="#FFFFFF",
            #         tags=f"{user}_label"
            #     )

        # Remove extra labels and images beyond the current users
        for i in range(len(users) + 1, len(self.y_positions) + 1):
            self.canvas.delete(self.user_statuses.get(f"user_{i}", None))
            self.canvas.delete(f"user_{i}_label")

    def clear_all_status_labels(self):
        for user, status_id in self.user_statuses.items():
            self.canvas.delete(status_id)
            self.canvas.delete(f"{user}_label")
        self.user_statuses.clear()

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

