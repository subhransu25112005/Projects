import tkinter as tk
from datetime import datetime, timedelta
from moon_phase import get_moon_phase  # your moon phase function
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import os, random

# ----------------- Fix: Use absolute path for moon_images -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # folder where this script is
MOON_IMAGE_PATH = os.path.join(BASE_DIR, "moon_images")  # points to moon_images/ folder

# ----------------- Get Moon Image -----------------
def get_moon_image(illumination, waxing=True):
    """
    Returns a real moon image based on illumination and waxing/waning.
    """
    if illumination < 1:
        phase_file = "new_moon.png"
    elif illumination < 50:
        phase_file = "waxing_crescent.png" if waxing else "waning_crescent.png"
    elif illumination == 50:
        phase_file = "first_quarter.png" if waxing else "last_quarter.png"
    elif illumination < 99:
        phase_file = "waxing_gibbous.png" if waxing else "waning_gibbous.png"
    else:
        phase_file = "full_moon.png"

    img_path = os.path.join(MOON_IMAGE_PATH, phase_file)
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")

    img = Image.open(img_path).resize((200, 200), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# ----------------- Waxing or Waning -----------------
def waxing_or_waning(date, lat, lon):
    today_phase = get_moon_phase(date, lat, lon)
    tomorrow = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow_phase = get_moon_phase(tomorrow, lat, lon)
    return tomorrow_phase >= today_phase

# ----------------- Show Moon Phase -----------------
def show_phase():
    date = date_entry.get()
    try:
        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        phase = get_moon_phase(date, lat, lon)
        waxing = waxing_or_waning(date, lat, lon)
        moon_img = get_moon_image(phase, waxing)
        moon_canvas.config(image=moon_img)
        moon_canvas.image = moon_img
        phase_label.config(
            text=f"Illumination: {phase:.2f}% ({'Waxing' if waxing else 'Waning'})"
        )
    except Exception as e:
        phase_label.config(text=f"Error: {e}")

# ----------------- Plot 30-Day Phases -----------------
def plot_month():
    try:
        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        phases = []
        dates = []
        base_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
        for i in range(30):
            d = base_date + timedelta(days=i)
            phase = get_moon_phase(d.strftime("%Y-%m-%d"), lat, lon)
            phases.append(phase)
            dates.append(d.strftime("%d-%b"))
        plt.figure(figsize=(10, 4))
        plt.plot(dates, phases, marker='o', color='orange')
        plt.xticks(rotation=45)
        plt.title("Moon Phase Over 30 Days")
        plt.ylabel("Illumination (%)")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        phase_label.config(text=f"Plot Error: {e}")

# ----------------- Twinkling Stars -----------------
def create_stars(num=50):
    stars = []
    for _ in range(num):
        x = random.randint(0, 350)
        y = random.randint(0, 550)
        size = random.randint(1, 2)
        color = random.choice(["white", "lightblue"])
        star = bg_canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
        stars.append(star)
    return stars

def twinkle():
    for star in stars:
        # Randomly change brightness
        color = random.choice(["white", "lightblue", "#a9cfff", "#dbe9ff"])
        bg_canvas.itemconfig(star, fill=color, outline=color)
    root.after(500, twinkle)  # repeat every 0.5 sec

# ----------------- Shooting Stars -----------------
def shooting_star():
    # random start and end positions
    x1 = random.randint(0, 300)
    y1 = random.randint(0, 200)
    x2 = x1 + random.randint(50, 100)
    y2 = y1 + random.randint(20, 50)

    star = bg_canvas.create_line(x1, y1, x1, y1, fill="white", width=2)

    def animate(step=0):
        if step < 15:  # animate 15 frames
            bg_canvas.coords(star, x1, y1, x1 + step*5, y1 + step*2)
            root.after(30, animate, step+1)
        else:
            bg_canvas.delete(star)  # remove after streak ends

    animate()
    root.after(random.randint(5000, 10000), shooting_star)  # another shooting star later

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Moon Phase Visualizer")
root.geometry("350x550")

# Canvas for starry background
bg_canvas = tk.Canvas(root, width=350, height=550, bg="black", highlightthickness=0)
bg_canvas.pack(fill="both", expand=True)

# Create stars
stars = create_stars(60)
twinkle()
shooting_star()  # start shooting stars loop

# Place widgets on top of canvas
date_label = tk.Label(root, text="Date (YYYY-MM-DD):", bg="black", fg="white", font=("Arial", 12))
date_entry = tk.Entry(root, bg="#1f2833", fg="white", insertbackground="white", font=("Arial", 12))
date_entry.insert(0, datetime.utcnow().strftime("%Y-%m-%d"))

lat_label = tk.Label(root, text="Latitude:", bg="black", fg="white", font=("Arial", 12))
lat_entry = tk.Entry(root, bg="#1f2833", fg="white", insertbackground="white", font=("Arial", 12))
lat_entry.insert(0, "20.2961")

lon_label = tk.Label(root, text="Longitude:", bg="black", fg="white", font=("Arial", 12))
lon_entry = tk.Entry(root, bg="#1f2833", fg="white", insertbackground="white", font=("Arial", 12))
lon_entry.insert(0, "85.8245")

show_button = tk.Button(root, text="Show Moon Phase", command=show_phase, bg="#45a29e", fg="white")
plot_button = tk.Button(root, text="Plot Month Phases", command=plot_month, bg="#66fcf1", fg="black")

moon_canvas = tk.Label(root, bg="black")
phase_label = tk.Label(root, text="", bg="black", fg="white", font=("Arial", 12))

# Place widgets (overlay on canvas)
bg_canvas.create_window(175, 30, window=date_label)
bg_canvas.create_window(175, 60, window=date_entry)
bg_canvas.create_window(175, 100, window=lat_label)
bg_canvas.create_window(175, 130, window=lat_entry)
bg_canvas.create_window(175, 170, window=lon_label)
bg_canvas.create_window(175, 200, window=lon_entry)
bg_canvas.create_window(175, 240, window=show_button)
bg_canvas.create_window(175, 280, window=plot_button)
bg_canvas.create_window(175, 360, window=moon_canvas)
bg_canvas.create_window(175, 470, window=phase_label)

root.mainloop()