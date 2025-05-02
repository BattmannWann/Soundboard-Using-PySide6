#Imports -------------------------------------------------------------

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QScrollArea, 
    QSlider,
    QLineEdit,
    QFrame, 
    
)

import sys, os, json, threading, random
import pygame
import sounddevice as sd
import soundfile as sf
import shutil
import numpy as np
from mutagen import File as MutagenFile

#--------------------------------------------------------------------


class Settings(QWidget):
    
    def __init__(self, main_app):
        
        super().__init__()
        self.main_app = main_app
        self.main_app.hide()
        
        self.setWindowTitle("Settings")
        self.resize(QSize(400, 200))
        self.setMaximumSize(400, 200)
        
        layout = QVBoxLayout(self)
        self.grid = QGridLayout()
        
        layout.addLayout(self.grid)
        
        devices = [device["name"] for device in sd.query_devices()]
        
        input_audio_label = QLabel("Default Input Device (Headphones): ")
        output_audio_label = QLabel("Default Output Device (Microphone): ")
        
        self.input_audio_option = QComboBox()
        self.input_audio_option.addItems(devices)
        self.input_audio_option.setCurrentIndex(main_app.settings["default_input_info"]["index"])
        
        self.output_audio_option = QComboBox()
        self.output_audio_option.addItems(devices)
        self.output_audio_option.currentIndexChanged.connect(self.index_changed)
        self.output_audio_option.setCurrentIndex(main_app.settings["default_output_info"]["index"])
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        save_button.setFixedSize(60,20)
        
        default_volume_label = QLabel("Default Volume Setting: ")
        default_volume = QLineEdit()
        default_volume.setMaxLength(10)
        default_volume.setPlaceholderText("Enter the volume here, E.g. 100")
        default_volume.setValidator(QIntValidator(1, 100, self))
        
        self.grid.addWidget(input_audio_label, 0, 0)
        self.grid.addWidget(self.input_audio_option, 0, 1)
        self.grid.addWidget(output_audio_label, 1, 0)
        self.grid.addWidget(self.output_audio_option, 1, 1)
        self.grid.addWidget(default_volume_label, 2, 0)
        self.grid.addWidget(default_volume, 2, 1)
        
        layout.addWidget(save_button, Qt.AlignmentFlag.AlignCenter)
        
    def index_changed(self, index):
        print(index)
        
    def text_changed(self, text):
        print(text)
        
        
    def save(self):
        self.main_app.settings["default_output"] = self.output_audio_option.currentIndex()
        self.main_app.settings["default_input"] = self.input_audio_option.currentIndex()
        
        self.main_app.save_settings()
        
    def closeEvent(self, event):
        self.main_app.show()
        return super().closeEvent(event)
        
        
class EditFiles(QWidget):
    
    def __init__(self, main_app):
        
        super().__init__()
        
        self.main_app = main_app
        self.main_app.hide()
        self.setWindowTitle("Edit File(s)")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 800)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.layout = QVBoxLayout(self)
        
        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        #self.grid.setContentsMargins(20, 10, 10, 10)
        
        #self.layout.addLayout(self.grid)
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)
        
        self.emoji = QLabel("Emoji")
        self.emoji.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.sound_name = QLabel("Name")
        self.sound_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.duration = QLabel("Duration")
        self.duration.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.options = QLabel("Options")
        self.options.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.underline = QFrame()
        self.underline.setFrameShape(QFrame.HLine)
        self.underline.setFrameShadow(QFrame.Plain)
        self.underline.setStyleSheet("color: gray; background-color: gray;")
        
        self.vertical_separator = QFrame()
        self.vertical_separator.setFrameShape(QFrame.VLine)
        self.vertical_separator.setFrameShadow(QFrame.Sunken)
        self.vertical_separator.setStyleSheet("color: gray;")
        
        
        self.vertical_separator2 = QFrame()
        self.vertical_separator2.setFrameShape(QFrame.VLine)
        self.vertical_separator2.setFrameShadow(QFrame.Sunken)
        self.vertical_separator2.setStyleSheet("color: gray;")
        
        
        font = self.emoji.font()
        font.setPointSize(15)
        
        self.emoji.setFont(font)
        self.sound_name.setFont(font)
        self.duration.setFont(font)
        self.options.setFont(font)
        
        self.grid.addWidget(self.emoji, 0, 0)
        self.grid.addWidget(self.sound_name, 0, 1)
        self.grid.addWidget(self.duration, 0, 2)
        
        self.grid.addWidget(self.options, 0, 4)
        self.grid.addWidget(self.underline, 1, 0, 1, -1)
        self.grid.addWidget(self.vertical_separator, 0, 0, -1, 1, alignment = Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.vertical_separator2, 0, 2, -1, 1, alignment = Qt.AlignmentFlag.AlignRight)

        
        curr_grid = 2
        
        for key, value in self.main_app.sound_buttons.items():
            
            sound_name = QLabel(key)
            sound_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
            emoji = QLabel()
            emoji.setPixmap(QPixmap(f"{self.main_app.icons_path}/angry.png").scaled(40,40))
            emoji.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
            duration = QLabel(f"{value["duration"]}")
            duration.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
            remove_button = QPushButton()
            remove_button.setIcon(QIcon(f"{self.main_app.icons_path}/cross.png"))
            remove_button.setStatusTip("Remove Sound")
            
            edit_name_button = QPushButton()
            edit_name_button.setIcon(QIcon(f"{self.main_app.icons_path}/application-rename.png"))
            edit_name_button.setStatusTip("Rename Sound")
            
            edit_sound_length_button = QPushButton()
            edit_sound_length_button.setIcon(QIcon(f"{self.main_app.icons_path}/radio--pencil"))
            edit_sound_length_button.setStatusTip("Modify Sound Length/Segment")
            
            self.grid.addWidget(emoji, curr_grid, 0)            
            self.grid.addWidget(sound_name, curr_grid, 1)
            self.grid.addWidget(duration, curr_grid, 2)
            self.grid.addWidget(remove_button, curr_grid, 3)
            self.grid.addWidget(edit_name_button, curr_grid, 4)
            self.grid.addWidget(edit_sound_length_button, curr_grid, 5)
            
            curr_grid += 1
            
            
    def closeEvent(self, event):
        self.main_app.show()
        return super().closeEvent(event)
               
                  

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        self.SETTINGS_FILE = "settings.json"
        
        DEFAULT_SETTINGS = {
            "volume": 1.0,
    
        }
        

        if os.path.exists(self.SETTINGS_FILE):
            
            with open(self.SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                
        else:
            
            settings = DEFAULT_SETTINGS.copy()
            default_output, default_input = sd.default.device

            input_device_info = sd.query_devices(default_input)
            output_device_info = sd.query_devices(default_output)

            settings["default_input_info"] = input_device_info
            settings["default_output_info"] = output_device_info
            settings["default_output"] = default_output
            settings["default_input"] = default_input
            

        pygame.mixer.init()
        
        self.icons_path = "media/images"
        self.sounds_path = "sounds"
        self.sound_buttons = {}
        self.settings = settings
        self.save_settings()
        
        self.setWindowTitle("Tower of Babel 2")
        self.setWindowIconText("Soundboard App")
        self.setWindowIcon(QIcon(f"{self.icons_path}/cassette.png"))
        self.setGeometry(100, 100, 800, 500)
        
        self.layout = QVBoxLayout()
        
        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        self.grid.setHorizontalSpacing(50)
        self.grid.setVerticalSpacing(20)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        
        #self.layout.addLayout(self.grid)
        self.load_sounds()
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)
        
        layout_widget = QWidget()
        layout_widget.setLayout(self.layout)
        self.setCentralWidget(layout_widget)
        
        self.setMinimumSize((QSize(1000, 500)))
        
        toolbar = QToolBar("Soundboard Toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)
        
        settings_button = QAction("Settings", self)
        settings_button.triggered.connect(self.settings_config)
        
        toolbar.addAction(settings_button)
        toolbar.addSeparator()
        
        add_files_button = QAction("Add File(s)", self)
        add_files_button.setStatusTip("Add your sound files here")
        add_files_button.triggered.connect(self.add_files)
        
        toolbar.addAction(add_files_button)
        toolbar.addSeparator()
        
        edit_files_button = QAction("Edit File(s)", self)
        edit_files_button.setStatusTip("Edit the sounds")
        edit_files_button.triggered.connect(self.edit_files)
        
        toolbar.addAction(edit_files_button)
        toolbar.addSeparator()
        
        spacer = QWidget()
        spacer.setFixedSize(450, 0)
        toolbar.addWidget(spacer)
        
        volume_label = QLabel("Volume    ")
        toolbar.addWidget(volume_label)
        
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(1, 100)
        volume_slider.setSingleStep(1)
        volume_slider.setValue(self.settings["volume"])
        volume_slider.setFixedWidth(250)
        volume_slider.valueChanged.connect(self.set_volume)
        
        toolbar.addWidget(volume_slider)
        
        
    def set_volume(self, value):
        print("Value: ", value/100)
        self.settings["volume"] = value/100
        self.load_sounds()

    
    def load_sounds(self):
        
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        if not os.path.exists(self.sounds_path):
            os.makedirs(self.sounds_path)

        files = [f for f in os.listdir(self.sounds_path) if f.endswith(('.wav', '.mp3'))]

        for idx, file in enumerate(files):
            
            name = os.path.splitext(file)[0]
            path = os.path.join(self.sounds_path, file)
            
            try:
                audio = MutagenFile(path)
                
                if audio is not None and audio.info is not None:
                    duration = round(audio.info.length, 2)
                
            except Exception as e:
                print(f"Failed to read {file}: {e}")
                duration = None

            icon_path = os.path.join(self.icons_path, name + ".png")
            btn = QPushButton(name[:40])
            
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                
            btn.clicked.connect(lambda _, p=path, v = self.settings["volume"]: self.play_sound(p, v))

            row, col = divmod(idx, 2)
            self.grid.addWidget(btn, row, col)
            self.sound_buttons[name] = {"path": path, "emoji_path": icon_path, "duration": duration}
            
    
        
    def add_files(self):
        
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Sound Files (*.mp3 *.wav)")
        
        if file_paths:
            for path in file_paths:
                
                filename = os.path.basename(path)
                destination = os.path.join(self.sounds_path, filename)
                
                try:
                    shutil.copy(path, destination)
                    
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to copy {filename}:\n{e}")           
        
        self.load_sounds() 
        
        
    def edit_files(self):
        
        self.external_window = EditFiles(self)
        self.external_window.show()
        
        
    def settings_config(self):
        
        self.external_window = Settings(self)
        self.external_window.show()
        
        
    def save_settings(self):
            with open(self.SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
                
                
    def play_sound(self, path, volume_level = 1.0):
        
        print(f"Volume Level is: {volume_level}")
    
        def _play(device):
            
            try:
                data, samplerate = sf.read(path)
                data = np.clip(data * volume_level, -1.0, 1.0)
                
                sd.play(data, samplerate=samplerate, device=device)
                sd.wait()
                
            except Exception as e:
                print(f"Error playing sound on device {device}: {e}\n")

        # if not self.settings["multi_play"]:
        #     pygame.mixer.stop()
        #     sd.stop()

        threading.Thread(target=_play, args=(self.settings["default_input"],)).start()
        threading.Thread(target=_play, args=(self.settings["default_output"],)).start()
        
        
    def closeEvent(self, event):
        pygame.mixer.stop()
        sd.stop()
        return super().closeEvent(event)


        
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec()