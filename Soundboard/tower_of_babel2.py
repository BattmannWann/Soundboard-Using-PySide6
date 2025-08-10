#Imports -------------------------------------------------------------

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QPixmap, QIntValidator
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
    QStackedLayout
    
)

from PySide6.QtGui import QFontDatabase

from superqt import QDoubleRangeSlider

import sys, os, json, threading, random
import sounddevice as sd
import soundfile as sf
import shutil
import numpy as np
from mutagen import File as MutagenFile
import getpass
import traceback
import time

#--------------------------------------------------------------------


class MultiDevicePlayer:
    
    def __init__(self):
        self.stop_event = threading.Event()
        self.threads = []


    def play_sound(self, path, devices, volume=1.0):
        
        """
        Play the given sound file on the input and output device simultaneously 
        """
        
        try:
            data, samplerate = sf.read(path, dtype='float32')
            
        except Exception as e:
            
            QMessageBox.warning(self, "Error", f"Failed to read audio file, see: {e}")
            return

        if data.ndim == 1:
            data = np.expand_dims(data, axis=1)

        data = np.clip(data * volume, -1.0, 1.0)
        self.stop_event.clear()

        self.threads = []
        
        for device in devices:
            
            t = threading.Thread(target=self._play_on_device,
                                 args=(data.copy(), samplerate, device))
            t.start()
            self.threads.append(t)


    def _play_on_device(self, data, samplerate, device):
        
        try:
            
            device_info = sd.query_devices(device, 'output')
            max_channels = device_info['max_output_channels']

            data = self._match_channels(data, max_channels)

            with sd.OutputStream(device=device,
                                 samplerate=samplerate,
                                 channels=data.shape[1],
                                 dtype='float32') as stream:

                
                blocksize = 1024
                idx = 0
                
                while idx < len(data):
                    
                    if self.stop_event.is_set():
                        break
                    
                    chunk = data[idx:idx+blocksize]
                    stream.write(chunk)
                    idx += blocksize

        except Exception as e:
            QMessageBox.warning(self, "Error", f"There was an error playing sound on device {device}, see: {e}")


    def _match_channels(self, data, max_channels):
        
        """
        Downmix or upmix audio to match the device's max channels.
        """
        
        num_channels = data.shape[1]

        if num_channels == max_channels:
            return data
        
        elif max_channels == 1:
            return data.mean(axis=1, keepdims=True) 
        
        elif max_channels == 2:
            
            mono = data.mean(axis=1)
            return np.stack((mono, mono), axis=1)  
        
        else:
            
            if num_channels > max_channels:
                return data[:, :max_channels]
            
            else:
                
                pad_width = max_channels - num_channels
                return np.hstack((data, np.zeros((len(data), pad_width), dtype=data.dtype)))


    def stop(self):
    
        """
        Signal all threads to stop playback.
        """
        
        self.stop_event.set()
        
        for t in self.threads:
            t.join()
            

class Settings(QWidget):
    
    def __init__(self, main_app):
        
        super().__init__()
        self.main_app = main_app

        self.main_app.resize(QSize(500, 400))
        
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(f"{self.main_app.icons_path}/cassette.png"))
        
        layout = QVBoxLayout(self)
        self.grid = QGridLayout()
        
        layout.addLayout(self.grid)
        
        devices = [device["name"] for device in sd.query_devices()]
        
        input_audio_label = QLabel("Default Input Device (Headphones): ")
        output_audio_label = QLabel("Default Output Device (Microphone): ")
        
        self.input_audio_option = QComboBox()
        self.input_audio_option.addItems(devices)
        self.input_audio_option.setCurrentIndex(main_app.settings["default_input"])
        
        self.output_audio_option = QComboBox()
        self.output_audio_option.addItems(devices)
        self.output_audio_option.setCurrentIndex(main_app.settings["default_output"])
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        save_button.setFixedSize(60,20)
        
        self.default_volume_label = QLabel("Default Volume Setting: ")
        self.default_volume = QLineEdit()
        self.default_volume.setFixedSize(QSize(400, 20))
        self.default_volume.setPlaceholderText("Enter the volume here, E.g. 100")
        self.default_volume.setValidator(QIntValidator(1, 100, self))
        

        self.username_label = QLabel("Username: ")
        self.username = QLineEdit()
        self.username.setFixedSize(QSize(400, 20))
        self.username.setPlaceholderText(f"{self.main_app.settings["username"]}")
        
        self.grid.addWidget(input_audio_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.input_audio_option, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(output_audio_label, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.output_audio_option, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.default_volume_label, 2, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.default_volume, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.username_label, 3, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.username, 3, 1, Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(save_button, Qt.AlignmentFlag.AlignCenter)

        with open("themes/style_sheet_settings.qss", "r") as f:
            self.setStyleSheet(f.read())
        
        
    def save(self):

        try:

            self.main_app.settings["default_output"] = self.output_audio_option.currentIndex()
            self.main_app.settings["default_input"] = self.input_audio_option.currentIndex()


            if self.default_volume.text().strip() != "":

                self.main_app.settings["volume"] = float(self.default_volume.text())/100
                self.main_app.volume_slider.setValue(self.main_app.settings["volume"]*100)

            if self.username.text().strip() != "":

                self.main_app.settings["username"] = self.username.text()
            
            self.main_app.save_settings()

            QMessageBox.information(self, "Success!", "Your settings have been saved successfully.")
            

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unable to save settings, see: {e}")

        
        
class EditFiles(QWidget):
    
    def __init__(self, main_app):
        
        super().__init__()
        
        self.main_app = main_app
        self.setWindowTitle("Edit File(s)")
        self.setWindowIcon(QIcon(f"{self.main_app.icons_path}/cassette.png"))
        

        self.button_to_options_mapping = {}

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
            
        self.layout = QVBoxLayout(self)
            
        self.content_widget = QWidget()
        self.content_widget.setObjectName("ContentWidget")
        self.grid = QGridLayout(self.content_widget)
        
        self.load_sound_options()

        self.resize(QSize(1400, 1000))

        with open("themes/style_sheet_edit_files.qss", "r") as f:
            self.setStyleSheet(f.read())
    
    
    def load_sound_options(self):

        try:

            if self.grid:

                for i in reversed(range(self.grid.count())):
                    item = self.grid.itemAt(i)
                    widget = item.widget()

                    if widget is not None:
                        widget.setParent(None) 
                        widget.deleteLater()

        except Exception as e:
            
            print(f"Unable to reload: {e}")

            pass


        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)
            
        self.emoji = QLabel("Emoji")
        self.emoji.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.emoticons_list = os.listdir(f"{self.main_app.icons_path}")
            
        self.sound_name = QLabel("Name")
        self.sound_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
        self.duration = QLabel("Duration")
        self.duration.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
        self.options = QLabel("Options")
        self.options.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
        self.underline = self.create_horizontal_separator()
        self.heading_line = self.create_horizontal_separator()
        self.bottom_line = self.create_horizontal_separator()
            
        #These are the vertical lines that span from left to right
        self.vertical_separator = self.create_vertical_separator()
        self.vertical_separator2 = self.create_vertical_separator()
        self.vertical_separator3 = self.create_vertical_separator()
        self.vertical_separator4 = self.create_vertical_separator()
        self.vertical_separator5 = self.create_vertical_separator()
            
            
        font = self.emoji.font()
        font.setPointSize(15)
            
        self.emoji.setFont(font)
        self.sound_name.setFont(font)
        self.duration.setFont(font)
        self.options.setFont(font)

        
        self.grid.addWidget(self.emoji, 1, 0)
        self.grid.addWidget(self.sound_name, 1, 1)
        self.grid.addWidget(self.duration, 1, 2)
        self.grid.addWidget(self.options, 1, 3)

        self.grid.addWidget(self.heading_line, 0, 0, 1, -1)
        self.grid.addWidget(self.underline, 2, 0, 1, -1)

        

        curr_grid = 3
        
        for key, value in self.main_app.sound_buttons.items():
            
            sound_name = QLabel(key)
            sound_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            sound_name.setObjectName("TableContentLabels")
            
            emoji = QLabel()

            if "emoji" in self.main_app.sound_buttons[key].keys(): 
                emoji.setPixmap(QPixmap(f"{value["emoji"]}").scaled(70,70))
            
            edit_emoji_button = QPushButton()
            edit_emoji_button.setIcon(QIcon(f"{self.main_app.icons_path}/Edit_Emoji.png"))
            edit_emoji_button.setStatusTip("Change Emoji/Picture")
            edit_emoji_button.clicked.connect(lambda _, name = sound_name, emoji = emoji: self.change_emoji(name, emoji))
            edit_emoji_button.setFixedSize(40, 30)
            edit_emoji_button.setStyleSheet("margin-left: 10px; padding-right: 10px;")
            
            remove_emoji_button = QPushButton()
            remove_emoji_button.setIcon(QIcon(f"{self.main_app.icons_path}/Remove_Icon.png"))
            remove_emoji_button.setStatusTip("Remove the set icon")
            remove_emoji_button.clicked.connect(lambda _, name = sound_name: self.remove_emoji(name))
            remove_emoji_button.setFixedSize(40, 30)
            
            emoji_widgets_box = QWidget()
            emoji_widgets_layout = QHBoxLayout(emoji_widgets_box)
            
            emoji_widgets_layout.setContentsMargins(0, 0, 0, 0)
            emoji_widgets_layout.setSpacing(10)
            
            emoji_widgets_layout.addWidget(edit_emoji_button)
            emoji_widgets_layout.addWidget(remove_emoji_button)
            emoji_widgets_layout.addWidget(emoji) 
            
            duration = QLabel(f"{value["duration"]}s")
            duration.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            duration.setObjectName("TableContentLabels")
            
            remove_button = QPushButton()
            remove_button.setIcon(QIcon(f"{self.main_app.icons_path}/cross.png"))
            remove_button.setStatusTip("Remove Sound")
            remove_button.clicked.connect(lambda _, name = sound_name: self.delete_sound(name))
            remove_button.setFixedSize(70, 20)
            
            edit_name_button = QPushButton()
            edit_name_button.setIcon(QIcon(f"{self.main_app.icons_path}/application-rename.png"))
            edit_name_button.setStatusTip("Rename Sound")
            edit_name_button.clicked.connect(lambda _, name = sound_name: self.rename_sound(name))
            edit_name_button.setFixedSize(70, 20)
            
            edit_sound_length_button = QPushButton()
            edit_sound_length_button.setIcon(QIcon(f"{self.main_app.icons_path}/radio--pencil"))
            edit_sound_length_button.setStatusTip("Modify Sound Length/Segment")
            edit_sound_length_button.clicked.connect(lambda _, name = sound_name, len =  duration: self.edit_sound_length(name, len))
            edit_sound_length_button.setFixedSize(70, 20)
            edit_sound_length_button.setStyleSheet("margin-right: 5px;")
            
            option_widgets_box = QWidget()
            option_widgets_box_layout = QHBoxLayout(option_widgets_box)
            
            option_widgets_box_layout.setContentsMargins(0, 0, 0, 0)
            option_widgets_box_layout.setSpacing(10)
            
            option_widgets_box_layout.addWidget(remove_button)
            option_widgets_box_layout.addWidget(edit_name_button)
            option_widgets_box_layout.addWidget(edit_sound_length_button)
          
            self.grid.addWidget(emoji_widgets_box, curr_grid, 0)          
            self.grid.addWidget(sound_name, curr_grid, 1)
            self.grid.addWidget(duration, curr_grid, 2)
            self.grid.addWidget(option_widgets_box, curr_grid, 3)

            self.button_to_options_mapping[sound_name] = {"remove": remove_button, 
                                                          "rename": edit_name_button, 
                                                          "modify_length": edit_sound_length_button,
                                                          "pos": curr_grid,
                                                        }

            
            curr_grid += 1

        self.grid.addWidget(self.bottom_line, curr_grid, 0, 1, -1)

        self.grid.addWidget(self.vertical_separator, 0, 0, -1, 1, alignment = Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.vertical_separator2, 0, 2, -1, 1, alignment = Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.vertical_separator3, 0, 0, -1, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.vertical_separator4, 0, 3, -1, 1, alignment = Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.vertical_separator5, 0, 2, -1, 1, alignment = Qt.AlignmentFlag.AlignLeft)

        with open("themes/style_sheet_edit_files.qss", "r") as f:
            self.setStyleSheet(f.read())

    
    def create_vertical_separator(self):
        
        vertical_separator = QFrame()
        vertical_separator.setFrameShape(QFrame.VLine)
        vertical_separator.setFrameShadow(QFrame.Plain)
        vertical_separator.setStyleSheet("color: gray; background-color: gray; padding: 50px")
        vertical_separator.setFixedWidth(4)
        

        return vertical_separator
    
    
    def create_horizontal_separator(self):

        horizontal_separator = QFrame()
        horizontal_separator.setFrameShape(QFrame.HLine)
        horizontal_separator.setFrameShadow(QFrame.Plain)
        horizontal_separator.setStyleSheet("color: gray; background-color: gray; padding-left: 50px;")
        horizontal_separator.setFixedHeight(4)

        return horizontal_separator
    
    
    def change_emoji(self, name, emoji):
        
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select Image for {name.text()}", "", "Image Files (*.png *.jpg *.jpeg)")
        
        if file_path:
                
            try:
                
                emoji.setPixmap(QPixmap(file_path).scaled(40,40))
                self.main_app.sound_buttons[name.text()]["emoji"] = file_path
                self.main_app.button_icons[name.text()] = file_path

                self.main_app.save_icons()
                self.main_app.edit_files()
                    
                    
            except Exception as e:
                error_msg = traceback.format_exc()
                QMessageBox.warning(self, "Error", f"Failed to change icon to {file_path}:\n{e}, \n\n and see: {error_msg}")
                
                
    def remove_emoji(self, name):
        
        if self.main_app.sound_buttons[name.text()]["emoji"] == f"{self.main_app.icons_path}/Icon_Placeholder.png":
            
            QMessageBox.information(self, "No Image Set", f"No image has been set for '{name.text()}'. \n\n The icon cannot be removed.")
            return
        
        warning_msg = QMessageBox.warning(self, "Warning", f"This will remove the icon set for '{name.text()}', are you sure you'd like to continue?", 
                                          QMessageBox.Yes | QMessageBox.Cancel)
        
        try:
        
            if warning_msg == QMessageBox.Yes:
                
                self.main_app.sound_buttons[name.text()]["emoji"] = f"{self.main_app.icons_path}/Icon_Placeholder.png"
                self.main_app.button_icons[name.text()] = f"{self.main_app.icons_path}/Icon_Placeholder.png"
                
                self.main_app.save_icons()
                self.main_app.edit_files()
                
                ok_box = QMessageBox.information(self, "Success!", f"The icon for '{name.text()}' has been removed.")
                
        except Exception as e:
            
            error_msg = traceback.format_exc()
            QMessageBox.warning(self, "ERROR", f"There was a problem removing the icon for '{name.text()}', \n\n see: {e}, \n\n and see: {error_msg}")
        
        
    
    
    def delete_sound(self, name):

        warning_msg = QMessageBox.question(self, "Confirm", f"Are you sure that you want to delete '{name.text()}'?", 
                                           QMessageBox.Cancel | QMessageBox.Yes)
        
        ok_box = QMessageBox(self)
        ok_box.setWindowTitle("Success!")
        ok_box.setText(f"'{name.text()}' has been successfully deleted.")
        ok_box.setStandardButtons(QMessageBox.Ok)
        
        try:

            if warning_msg == QMessageBox.Yes:

                print(f"Removing {self.main_app.sound_buttons[name.text()]["path"]}...")
                os.remove(self.main_app.sound_buttons[name.text()]["path"])
                self.main_app.sound_buttons.pop(name.text())
                self.main_app.button_icons.pop(name.text())

                ok_box.exec()

                self.main_app.edit_files()
                self.main_app.save_icons()
                
        
        except Exception as e:
            
            not_ok_box = QMessageBox(self)
            not_ok_box.setWindowTitle("ERROR")
            not_ok_box.setText(f"There has been an error deleting '{name}', see: {e}")
            not_ok_box.setStandardButtons(QMessageBox.Ok)
            
            not_ok_box.exec()

    
    def rename_sound(self, name):
        
        self.window = QWidget()
        self.window.resize(900,100)
        self.window.setWindowTitle(f"Renaming: '{name.text()}'")
        self.window.setWindowIcon(QIcon(f"{self.main_app.icons_path}/cassette.png"))
        self.window.show()
        
        self.grid = QGridLayout()
        self.window.setLayout(self.grid)
        
        if len(name.text()) > 30:
            self.sound_name_label = QLabel(f"Original Name: '{name.text()[:30]}...' ")
        
        else:
            self.sound_name_label = QLabel(f"Original Name: '{name.text()}' ")
        
        self.rename_box = QLineEdit()
        self.rename_box.setPlaceholderText("Enter new sound name here...")
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(lambda _, original = name: self.save_rename(original))
        self.save_button.setFixedSize(70, 30)
        
        self.grid.addWidget(self.sound_name_label, 0, 0)
        self.grid.addWidget(self.rename_box, 0, 1)
        self.grid.addWidget(self.save_button, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        
        with open("themes/style_sheet_edit_options.qss", "r") as f:
            self.window.setStyleSheet(f.read())
        
        
    def save_rename(self, original):
            
        original_path = f"{self.main_app.sound_buttons[original.text()]["path"]}"
        
        file_type = self.main_app.sound_buttons[original.text()]["file_type"]
        new_path = f"{self.main_app.sounds_path}/{self.rename_box.text()}{file_type}"
        
        try:
            
            if f"{original.text()}{file_type}" in os.listdir(self.main_app.unedited_sounds_path):
                
                os.rename(f"{self.main_app.unedited_sounds_path}/{original.text()}{file_type}", f"{self.main_app.unedited_sounds_path}/{self.rename_box.text()}{file_type}")
                
            if self.rename_box.text().strip() != '':
                    
                os.rename(original_path, new_path)
                self.main_app.sound_buttons[f"{self.rename_box.text()}"] = self.main_app.sound_buttons.pop(f"{original.text()}")

                if original.text() in self.main_app.button_icons.keys():

                    renamed_val = self.main_app.button_icons.pop(original.text())
                    self.main_app.button_icons[self.rename_box.text()] = renamed_val

                    self.main_app.save_icons()
                
                QMessageBox.information(self, "Success!", f"Your sound '{original.text()}'  has been renamed to '{self.rename_box.text()}' ")
                self.window.close()
                    
                self.main_app.edit_files()
                
                
            else:
                QMessageBox.information(self, "Nothing Entered", "Nothing has been entered in the box. If this was a mistake, please try again.")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"We were unable to rename your file, see: {e}")
            
            
    
    def edit_sound_length(self, name, duration):
        
        self.window = QWidget()
        self.window.setFixedSize(QSize(800,110))
        self.window.setWindowIcon(QIcon(f"{self.main_app.icons_path}/cassette.png"))
            
        self.window.setWindowTitle(f"Editing Length of  sound '{name.text()}'")
        self.window.show()
        
        self.grid = QGridLayout()
        self.window.setLayout(self.grid)
        
        self.trimmed_sounds = {}
        self.previewed = False
        
        self.length = float(duration.text()[:len(duration.text())-1])
        self.curr_len_label = QLabel(f"Length of '{name.text()[:25]}': {duration.text()}")
        
        self.length_slider = QDoubleRangeSlider(Qt.Orientation.Horizontal)
        self.length_slider.setFixedSize(200,20)
        self.length_slider.valueChanged.connect(self.length_slider_val_changed)
        
        
        
        if self.length < 1:
            
            error_message = QMessageBox.warning(self, "Sound too short", "Sounds less than 1s are unable to be modified.", buttons = QMessageBox.Ok)
            self.window.close()
            return
            
            
        else:
            
            self.length_slider.setSingleStep(0.1)
            self.len_slider_label = QLabel("1s")
            
            self.length_slider.setRange(1.0, self.length)
            
        
        self.preview_button = QPushButton()
        self.preview_button.clicked.connect(lambda _, name = name.text(), slider = self.length_slider: self.preview_sound(name, slider))
        
        self.preview_button.setIcon(QIcon(f"{self.main_app.icons_path}/Speaker_Icon.svg"))
        self.preview_button.setIconSize(QSize(24, 24))
        self.preview_button.setBaseSize(QSize(15, 10))
        
        self.save_length_button = QPushButton("Save")
        self.save_length_button.clicked.connect(lambda _, name = name.text(): self.save_length(name))
        
        self.revert_sound_button = QPushButton("Revert Sound")
        self.revert_sound_button.clicked.connect(lambda _, name = name.text(): self.revert_sound(name))
        
        self.grid.addWidget(self.preview_button, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.curr_len_label, 0, 0,Qt.AlignmentFlag.AlignHCenter)
        self.grid.addWidget(self.length_slider, 0, 1, Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.len_slider_label, 0, 1, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.save_length_button, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.revert_sound_button, 1, 0, Qt.AlignmentFlag.AlignCenter)
        
        with open("themes/style_sheet_edit_options.qss", "r") as f:
            self.window.setStyleSheet(f.read())
        
        
        
    def length_slider_val_changed(self, value):
        
        print(f"Value is: {value[0]} - {value[1]}")
        self.len_slider_label.setText(f"Between {round(value[0], 2)}s and {round(value[1], 2)}s")

        
    def preview_sound(self, name, slider):
        
        """ 
        Each sound has been stored as a numpy array. This, using this knowledge we can splice the sound array to edit its length as follows:
        
            - Each row in the data array is ONE AUDIO FRAME.
            - The number of frames per second is determined by the SAMPLERATE
            - Thus, to trim our audio, we do 
            
                trimmed_length = samplerate * number_of_seconds
                trimmed_data = data[:trimmed_data]
                
            - So, if we want the first 5 seconds, substitute 'number_of_seconds' with 5. 
            
            - Here, we have a double handled slider, so we can splice using a start and stop value
            
                trimmed_start = samplerate * handle_1
                trimmed_end = samplerate * handle_2
                
                trimmed_sound = data[trimmed_start:trimmed_end]
        """
        
        self.preview_button.setDisabled(True)
        self.length_slider.setDisabled(True)
        
        self.previewed = True
        
        self.trim_sound(name, slider)
            
        self.preview_button.setDisabled(False)
        self.length_slider.setDisabled(False)
        
    
    def trim_sound(self, name, slider):
        
        print(f"This is {name}")
        
        file_path = self.main_app.sound_buttons[name]["path"]
        print(file_path)
        
        device = self.main_app.settings["default_input"]
        data, samplerate = sf.read(file_path)
        
        handle_1 = int(slider.value()[0])
        handle_2 = int(slider.value()[1])
        
        trimmed_start = samplerate * handle_1
        trimmed_end = samplerate * handle_2
        
        if self.previewed == True:
        
            try:
                sd.play(data = data[trimmed_start: trimmed_end], samplerate = samplerate, device = device)
                sd.wait()
                
            except Exception as e:
                print(f"Whoops, something went wrong: {e}")
            
        self.trimmed_sounds[name] = {"trimmed_data": data[trimmed_start:trimmed_end], "samplerate": samplerate}
               
    
    def save_length(self, name):
        
        ok_box = QMessageBox(self)
        ok_box.setWindowTitle("Success!")
        ok_box.setText(f"{name} has been successfully modified.")
        ok_box.setStandardButtons(QMessageBox.Ok)
        
        warning_msg = QMessageBox.question(self, "Confirm", 
        f"This action will modify '{name}'. \n\n You may revert this at any time. Do you wish to proceed? ",
        QMessageBox.Cancel | QMessageBox.Yes)
        
        if self.previewed == False:
            
            self.trim_sound(name, self.length_slider)
            print("Trimmed")
        
        try: 
            if warning_msg == QMessageBox.Yes:
                
                print("Saving modified sound...")
                
                file_type = self.main_app.sound_buttons[name]["file_type"]
                shutil.move(f"{self.main_app.sound_buttons[name]["path"]}", f"{self.main_app.unedited_sounds_path}/")
                
                sf.write(f"{self.main_app.sounds_path}/{name}{file_type}", self.trimmed_sounds[name]["trimmed_data"], self.trimmed_sounds[name]["samplerate"])
                ok_box.exec()
                
                duration = self.main_app.get_duration(f"{self.main_app.sounds_path}/{name}{file_type}", name)
                self.main_app.sound_buttons[name]["duration"] = duration
                
                self.window.close()
                self.main_app.edit_files()
                
                
                
                
        except Exception as e:
            
            not_ok_box = QMessageBox(self)
            not_ok_box.setWindowTitle("Error")
            not_ok_box.setText(f"There has been an error updating '{name}', see: {e}")
            not_ok_box.setStandardButtons(QMessageBox.Ok)
            
            not_ok_box.exec()
            
            self.window.close()
            
            
    def revert_sound(self, name):
        
        warning_msg = QMessageBox.question(self, "Confirm", 
        f"This will revert the sound back to its original form. Are you certain?",
        QMessageBox.Cancel | QMessageBox.Yes)
        
        ok_box = QMessageBox(self)
        ok_box.setWindowTitle("Success!")
        ok_box.setText(f"'{name}' has been successfully reverted back to the original file.")
        ok_box.setStandardButtons(QMessageBox.Ok)
        
        try:
            
            if warning_msg == QMessageBox.Yes:
                
                file_type = self.main_app.sound_buttons[name]["file_type"]
                
                os.remove(f"{self.main_app.sounds_path}/{name}{file_type}")
                shutil.move(f"{self.main_app.unedited_sounds_path}/{name}{file_type}", f"{self.main_app.sounds_path}/")
                
                duration = self.main_app.get_duration(f"{self.main_app.sounds_path}/{name}{file_type}", name)
                self.main_app.sound_buttons[name]["duration"] = duration
                
                self.main_app.edit_files()
                
                ok_box.exec()
                
        except Exception as e:
            
            not_ok_box = QMessageBox(self)
            not_ok_box.setWindowTitle("ERROR")
            not_ok_box.setText(f"There has been an error reverting '{name}', this sound likely hasn't been modified yet.")
            not_ok_box.setStandardButtons(QMessageBox.Ok)
            
            not_ok_box.exec()  

        finally:
            
            self.window.close()
            self.main_app.edit_files()
            
            
               
                  
class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()

        self.active_threads = []
        self.stop_event = threading.Event()
        
        self.SETTINGS_FILE = "settings.json"
        self.BUTTON_ICONS_FILE = "button_images.json"
        
        DEFAULT_SETTINGS = {
            "volume": 1.0,
    
        }

        username = getpass.getuser()

        if os.path.exists(self.SETTINGS_FILE):
            
            with open(self.SETTINGS_FILE, "r") as f:
                settings = json.load(f)

            if "username" not in settings.keys():
                settings["username"] = username

                
        else:
            
            settings = DEFAULT_SETTINGS.copy()
            default_output, default_input = sd.default.device

            input_device_info = sd.query_devices(default_input)
            output_device_info = sd.query_devices(default_output)

            settings["default_input_info"] = input_device_info
            settings["default_output_info"] = output_device_info
            settings["default_output"] = default_output
            settings["default_input"] = default_input
            settings["username"] = username

        if os.path.exists(self.BUTTON_ICONS_FILE):

            with open(self.BUTTON_ICONS_FILE, "r") as f:
                button_icons = json.load(f)

        else:

            button_icons = {}
            
        
        self.icons_path = "media/images"
        self.sounds_path = "sounds"
        self.trimmed_sounds_path = "trimmed_sounds"
        self.unedited_sounds_path = "unedited_sounds"
        
        self.player = MultiDevicePlayer()

        self.sound_buttons = {}
        self.button_icons = button_icons
        self.settings = settings
        self.save_settings()
        
        self.setWindowTitle("Tower of Babel 2")
        self.setWindowIconText("Soundboard App")
        self.setWindowIcon(QIcon(f"{self.icons_path}/cassette.png"))

        self.setGeometry(100, 100, 800, 500)
        self.resize(QSize(1400, 450))
        self.setMaximumSize(QSize(1400, 1000))

        self.build_home_view()
        
        toolbar = QToolBar("Soundboard Toolbar")
        toolbar.setIconSize(QSize(32,32))
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        
        self.addToolBar(toolbar)

        home_button = QAction(QIcon("media/images/Home-icon.png"), "", self)
        home_button.setStatusTip("Home Dashboard")
        home_button.triggered.connect(self.build_home_view)

        toolbar.addAction(home_button)
        toolbar.addSeparator()
        
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

        stop_sounds_button = QAction("Stop Sound(s)", self)
        stop_sounds_button.setStatusTip("Stop playing the current sound(s)")
        stop_sounds_button.triggered.connect(self.player.stop)

        toolbar.addAction(stop_sounds_button)
        toolbar.addSeparator()
        
        spacer = QWidget()
        spacer.setFixedSize(600, 0)
        toolbar.addWidget(spacer)
        
        volume_label = QLabel("Volume    ")
        toolbar.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setProperty("class", "VolumeSlider")
        self.volume_slider.setRange(1, 100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setValue(self.settings["volume"]*100)
        self.volume_slider.setFixedWidth(250)
        self.volume_slider.valueChanged.connect(self.set_volume)
        
        toolbar.addWidget(self.volume_slider)


        with open("themes/style_sheet_main_app.qss", "r") as f:
            self.setStyleSheet(f.read())
        
        
    def set_volume(self, value):
        print("Value: ", value/100)
        self.settings["volume"] = value/100
        self.load_sounds()
        
        
    def get_duration(self, path, file):
        
        try:
                audio = MutagenFile(path)
                
                if audio is not None and audio.info is not None:
                    duration = round(audio.info.length, 2)
                
        except Exception as e:
            print(f"Failed to read {file}: {e}")
            duration = None
            
        return duration

    
    def load_sounds(self):

        if not os.path.exists(self.sounds_path):

            os.makedirs(self.sounds_path)

            no_files_label = QLabel("Looks like we don't have any files yet. Click 'Add File(s)' to add some sounds!")

            font = no_files_label.font()
            font.setPointSize(15)

            no_files_label.setFont(font)
            self.grid.addWidget(no_files_label)
            

            return
        
        if not os.listdir(self.sounds_path):
        
            no_files_label = QLabel("Looks like we don't have any files yet. Click 'Add File(s)' to add some sounds!")

            font = no_files_label.font()
            font.setPointSize(15)

            no_files_label.setFont(font)
            self.grid.addWidget(no_files_label)
            

            return
        
        if not os.path.exists(self.unedited_sounds_path):
            
            os.makedirs(self.unedited_sounds_path)
   

        files = [f for f in os.listdir(self.sounds_path) if f.endswith(('.wav', '.mp3'))]

        for idx, file in enumerate(files):
            
            name = os.path.splitext(file)[0]
            path = os.path.join(self.sounds_path, file)
            
            duration = self.get_duration(path, file)
            
            devices = [self.settings["default_input"], self.settings["default_output"]]

            btn = QPushButton(f" {name[:40]}")
            btn.setProperty("class", "SoundButton")
            btn.setFixedHeight(75)
                
            btn.clicked.connect(lambda _, p=path, v = self.settings["volume"]: self.player.play_sound(path = p, devices = devices, volume = v))

            row, col = divmod(idx, 3)
            self.grid.addWidget(btn, row, col)

            if name not in self.sound_buttons.keys():
                self.sound_buttons[name] = {"path": path, "emoji": f"{self.icons_path}/Icon_Placeholder.png", "duration": duration, "file_type": f".{path.split(".")[-1]}"}

            if name in self.button_icons.keys():
                self.sound_buttons[name]["emoji"] = self.button_icons[name]

            if self.sound_buttons[name]["emoji"] != f"{self.icons_path}/Icon_Placeholder.png":
                btn.setIcon(QIcon(self.sound_buttons[name]["emoji"]))
                btn.setIconSize(QSize(60, 55))



    def build_home_view(self):

        self.resize(QSize(1400, 450))

        self.layout = QVBoxLayout()

        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        self.grid.setHorizontalSpacing(50)
        self.grid.setVerticalSpacing(20)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.welcome_label = QLabel(f"Welcome {self.settings['username']}!")
        welcome_font = self.welcome_label.font()
        welcome_font.setPointSize(30)
        self.welcome_label.setFont(welcome_font)
        self.welcome_label.setObjectName("MainTitle")

        self.layout.addWidget(self.welcome_label)

        self.load_sounds()
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        layout_widget = QWidget()
        layout_widget.setLayout(self.layout)
        self.setCentralWidget(layout_widget)

        with open("themes/style_sheet_main_app.qss", "r") as f:
            self.setStyleSheet(f.read())



        
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

        with open("themes/style_sheet_edit_files.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(EditFiles(self))
        self.resize(QSize(1400, 500))
        
        
    def settings_config(self):
    
        with open("themes/style_sheet_settings.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(Settings(self))
        
        
    def save_settings(self):
            
        try:    
            with open(self.SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4) 

        except Exception as e:
            QMessageBox.warning(self, f"Error", f"Unable to save settings, see: {e}")

    
    def save_icons(self):

        try:
            with open(self.BUTTON_ICONS_FILE, "w") as f:
                json.dump(self.button_icons, f, indent = 4)

        except Exception as e:
            QMessageBox.warning(self, f"Error", f"Unable to save icon path, see: {e}")
        

    def closeEvent(self, event):
        
        self.player.stop()
        return super().closeEvent(event)


        
        
app = QApplication([])
window = MainWindow()

roboto = QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Regular.ttf")
roboto_medium = QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Medium.ttf")
roboto_black = QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Black.ttf")


window.show()
app.exec()