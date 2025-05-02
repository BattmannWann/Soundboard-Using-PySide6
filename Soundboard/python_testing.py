import sounddevice as sd
import os
import subprocess

# List all available devices
#print(sd.query_devices())


# Define the path to the folder containing sound files
# sounds_folder = 'sounds'
# output_folder = "sounds_converted"

# os.makedirs(output_folder, exist_ok=True)

# # Loop through all files in the folder
# for filename in os.listdir(sounds_folder):
#     #file_path = os.path.join(sounds_folder, filename)
#     input_path = os.path.join(sounds_folder, filename)
    
#     # Check if the file is a WAV or MP3 file (you can add more formats if needed)
#     if filename.lower().endswith(('.wav', '.mp3')):
#         output_path = os.path.join(output_folder, f"converted_{filename}")
        
#         # Command to convert to stereo (2 channels)
#         command = [
#             'ffmpeg', '-i', input_path, '-ac', '2', output_path
#         ]
        
#         try:
#             # Run the command
#             subprocess.run(command, check=True)
#             print(f"Successfully converted: {filename}")
#         except subprocess.CalledProcessError:
#             print(f"Error converting: {filename}")


# Get default device indices (output, input)
# default_output, default_input = sd.default.device

# print(f"Default output device index: {default_output}")
# print(f"Default input device index: {default_input}")


# from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QScrollArea
# from PySide6.QtCore import Qt
# import sys

# app = QApplication(sys.argv)

# # Main window
# window = QWidget()
# window.setWindowTitle("Scrollable Grid with Side Scrollbar")
# window.resize(400, 300)

# # Main layout
# layout = QVBoxLayout(window)

# # Scroll area
# scroll_area = QScrollArea()
# scroll_area.setWidgetResizable(True)
# scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # disable horizontal scrolling (optional)
# scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)     # vertical scrollbar when needed

# # Content widget inside scroll area
# content_widget = QWidget()
# grid_layout = QGridLayout(content_widget)

# # Populate the grid with labels
# for row in range(20):  # More rows = scrolling needed
#     for col in range(4):
#         label = QLabel(f"Label {row},{col}")
#         label.setFixedSize(80, 40)  # optional: fix size
#         grid_layout.addWidget(label, row, col)

# scroll_area.setWidget(content_widget)
# layout.addWidget(scroll_area)

# window.show()
# app.exec()


