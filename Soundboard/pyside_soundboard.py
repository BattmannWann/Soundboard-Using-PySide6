from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QCheckBox, QSlider, QGridLayout
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
import sys, os, json, threading, random
import pygame
import sounddevice as sd
import soundfile as sf

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "volume": 100,
    "dark_mode": False,
    "multi_play": True,
    "sounds": [],
    "theme": "light",
    "keybinds": {}
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
MICROPHONE = 6
HEADSET = 5

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


class SoundboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tower of Babel 2")
        self.setMinimumSize(800, 600)

        self.sounds_path = "sounds"
        self.icons_path = "/media/images/"
        self.sound_buttons = {}

        self.layout = QVBoxLayout(self)
        self.top_bar = QHBoxLayout()
        self.grid = QGridLayout()

        self.setup_controls()
        self.layout.addLayout(self.top_bar)
        self.layout.addLayout(self.grid)
        self.load_sounds()

        self.apply_theme()

    def setup_controls(self):
        dark_btn = QPushButton("Toggle Dark Mode")
        dark_btn.clicked.connect(self.toggle_dark_mode)
        self.top_bar.addWidget(dark_btn)

        rand_btn = QPushButton("Random Sound")
        rand_btn.clicked.connect(self.play_random_sound)
        self.top_bar.addWidget(rand_btn)

        stop_btn = QPushButton("Stop All Sounds")
        stop_btn.clicked.connect(self.stop_sounds)
        self.top_bar.addWidget(stop_btn)

        self.multi_play_check = QCheckBox("Multi-play")
        self.multi_play_check.setChecked(settings["multi_play"])
        self.multi_play_check.stateChanged.connect(self.toggle_multi)
        self.top_bar.addWidget(self.multi_play_check)

        vol_label = QLabel("Volume")
        self.top_bar.addWidget(vol_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(settings["volume"])
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.top_bar.addWidget(self.volume_slider)

    def load_sounds(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        if not os.path.exists(self.sounds_path):
            os.makedirs(self.sounds_path)

        files = [f for f in os.listdir(self.sounds_path) if f.endswith(('.wav', '.mp3'))]

        for idx, file in enumerate(files):
            
            name = os.path.splitext(file)[0]
            path = os.path.join(self.sounds_path, file)

            icon_path = os.path.join(self.icons_path, name + ".png")
            btn = QPushButton(name)
            
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                
            btn.clicked.connect(lambda _, p=path: play_sound(p))

            row, col = divmod(idx, 4)
            self.grid.addWidget(btn, row, col)
            self.sound_buttons[name] = path

    def toggle_dark_mode(self):
        settings["dark_mode"] = not settings["dark_mode"]
        save_settings()
        self.apply_theme()

    def apply_theme(self):
        if settings["dark_mode"]:
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
        else:
            self.setStyleSheet("")

    def play_random_sound(self):
        if self.sound_buttons:
            play_sound(random.choice(list(self.sound_buttons.values())))

    def stop_sounds(self):
        pygame.mixer.stop()
        sd.stop()

    def set_volume(self, value):
        settings["volume"] = value
        save_settings()

    def toggle_multi(self, state):
        settings["multi_play"] = bool(state)
        save_settings()
        
    #def set_icon(self, icon_path, button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SoundboardApp()
    window.show()
    sys.exit(app.exec())
