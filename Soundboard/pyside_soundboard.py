from PySide6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame
)

app = QApplication([])

# Main window
window = QWidget()
layout = QVBoxLayout(window)

# Title
title_label = QLabel("SoundBoard")
title_label.setObjectName("MainTitle")
layout.addWidget(title_label)

# Subtitle
subtitle_label = QLabel("Click the buttons to play sounds")
subtitle_label.setObjectName("MainSubtitle")
layout.addWidget(subtitle_label)

# Soundboard frame
soundboard_frame = QFrame()
soundboard_frame.setObjectName("SoundboardCard")
soundboard_layout = QHBoxLayout(soundboard_frame)

# Sound buttons
for label in ["Drum", "Bell", "Click", "Success"]:
    btn = QPushButton(label)
    btn.setProperty("class", "SoundButton")
    soundboard_layout.addWidget(btn)

layout.addWidget(soundboard_frame)

# Footer
footer = QLabel("Created with PySide6")
footer.setObjectName("Footer")
layout.addWidget(footer)

# Apply stylesheet (after setting all object names / classes)
with open("style_sheet.qss", "r") as f:
    app.setStyleSheet(f.read())

# Show window
window.show()
app.exec()
