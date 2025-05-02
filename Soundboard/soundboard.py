import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import pygame
import threading
import os
import json
import random
from PIL import Image, ImageTk
import sounddevice as sd
import soundfile as sf


# Load settings
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "volume": 100,
    "dark_mode": False,
    "multi_play": True,
    "sounds": [],
    "theme": "light"
}

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = DEFAULT_SETTINGS.copy()


def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


pygame.mixer.init()
print(pygame.mixer.get_init())  # should now say (22050, -16, 2)


# Load & Play Audio
# Assuming the virtual audio cable is device 3, replace with your virtual device index
MICROPHONE = 6 #32
HEADSET = 5 #33

# def play_sound(path):
#     def _play():
#         try:
#             # Load the sound file using soundfile for compatibility with sounddevice
#             data, samplerate = sf.read(path)

#             # Use sounddevice to play the sound through the virtual audio cable
#             sd.play(data, samplerate=samplerate, device=MICROPHONE)
#             #sd.play(data, samplerate=samplerate, device=HEADSET)
#             sd.wait()  # Wait for the sound to finish playing

#         except Exception as e:
#             print(f"Error playing sound: {e}")

#     if not settings["multi_play"]:
#         pygame.mixer.stop()

#     threading.Thread(target=_play).start()

def play_sound(path):
    def _play(device):
        try:
            data, samplerate = sf.read(path)
            sd.play(data, samplerate=samplerate, device=device)
            sd.wait()
        except Exception as e:
            print(f"Error playing sound on device {device}: {e}")

    if not settings["multi_play"]:
        pygame.mixer.stop()
        sd.stop()

    threading.Thread(target=_play, args=(MICROPHONE,)).start()
    threading.Thread(target=_play, args=(HEADSET,)).start()



# Main App
class SoundboardApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Soundboard")
        self.geometry("700x500")
        self.configure(bg="white")

        self.sounds_path = "sounds"
        self.icons_path = "icons"
        self.sound_buttons = {}

        self.create_ui()
        self.bind("<Key>", self.keybind_handler)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

        self.apply_theme()

    def create_ui(self):
        top = ttk.Frame(self)
        top.pack(pady=10)

        ttk.Button(top, text="Toggle Dark Mode", command=self.toggle_dark_mode).pack(side="left", padx=5)
        ttk.Button(top, text="Random Sound", command=self.play_random_sound).pack(side="left", padx=5)
        ttk.Button(top, text="Stop All Sounds", command=self.stop_sounds).pack(side="left", padx=5)

        ttk.Checkbutton(top, text="Multi-play", variable=tk.BooleanVar(value=settings["multi_play"]),
                        command=self.toggle_multi).pack(side="left", padx=5)

        ttk.Label(top, text="Volume").pack(side="left", padx=5)
        self.volume = ttk.Scale(top, from_=0, to=100, orient='horizontal', command=self.set_volume)
        self.volume.set(settings["volume"])
        self.volume.pack(side="left")

        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.load_sounds()

    def load_sounds(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if not os.path.exists(self.sounds_path):
            os.makedirs(self.sounds_path)

        files = [f for f in os.listdir(self.sounds_path) if f.endswith(('.wav', '.mp3'))]

        for idx, file in enumerate(files):
            name = os.path.splitext(file)[0]
            path = os.path.join(self.sounds_path, file)

            icon_path = os.path.join(self.icons_path, name + ".png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path).resize((32, 32))
                photo = ImageTk.PhotoImage(img)
                btn = ttk.Button(self.frame, image=photo, text=name, compound="left",
                                command=lambda p=path: self.animate_button(p))
                btn.image = photo
            else:
                btn = ttk.Button(self.frame, text=name, command=lambda p=path: self.animate_button(p))

            btn.grid(row=idx // 4, column=idx % 4, padx=10, pady=10, ipadx=10, ipady=10)
            self.sound_buttons[name] = path


    def animate_button(self, path):
        name = os.path.splitext(os.path.basename(path))[0]  # Extract the filename without extension
        print(f"Looking for button with text: {name}")
        
        # Find the button using the text (which should be the name without the extension)
        btn = next((b for b in self.frame.winfo_children() if b.cget('text') == name), None)
        
        if btn:
            original = btn.cget('style')
            btn.config(style="Pressed.TButton")
            self.after(100, lambda: btn.config(style=original))  # Reset the style after 100ms
            play_sound(path)
        else:
            print(f"Button not found for {name}")




    def set_volume(self, val):
        settings["volume"] = int(float(val))
        save_settings()

    def toggle_multi(self):
        settings["multi_play"] = not settings["multi_play"]
        save_settings()

    def toggle_dark_mode(self):
        settings["dark_mode"] = not settings["dark_mode"]
        save_settings()
        self.apply_theme()

    def apply_theme(self):
        style = ttk.Style(self)
        if settings["dark_mode"]:
            self.configure(bg="#2e2e2e")
            style.configure('TButton', background="#444", foreground="white")
            style.configure('Pressed.TButton', background="#666")
        else:
            self.configure(bg="white")
            style.configure('TButton', background="#ddd", foreground="black")
            style.configure('Pressed.TButton', background="#aaa")

    def play_random_sound(self):
        if self.sound_buttons:
            play_sound(random.choice(list(self.sound_buttons.values())))

    def keybind_handler(self, event):
        key = event.char
        if key in settings["keybinds"]:
            play_sound(settings["keybinds"][key])

    def on_drop(self, event):
        files = self.tk.splitlist(event.data)
        for f in files:
            name = os.path.basename(f)
            dest = os.path.join(self.sounds_path, name)
            if not os.path.exists(dest):
                os.rename(f, dest)
        self.load_sounds()
        
    def stop_sounds(self):
        pygame.mixer.stop()  # Stops pygame sounds
        sd.stop()            # Stops sounddevice playback



if __name__ == "__main__":
    app = SoundboardApp()
    app.mainloop()
