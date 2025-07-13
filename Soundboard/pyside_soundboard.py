import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStyle
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtCore import QSize, Qt

class ButtonIconDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPushButton Icon Left Align Demo")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        button = QPushButton("Play Sound")
        button.setObjectName("SoundButton")

        # Set an icon directly on the button
        try:
            icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        except AttributeError:
            from PySide6.QtGui import QPixmap, QPainter
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(Qt.blue)
            painter.drawEllipse(0, 0, 32, 32)
            painter.end()
            icon = QIcon(pixmap)

        button.setIcon(icon)
        button.setIconSize(QSize(20, 20))

        layout.addWidget(button)

        # Apply your QSS with text-align: left
        self.setStyleSheet("""
            QPushButton#SoundButton {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 16px;
                color: #374151;
                font-weight: 500;
                /* Crucial for left alignment of icon and text */
                text-align: center;
            }

            QPushButton#SoundButton:hover {
                background-color: #f3f4f6;
            }

            QPushButton#SoundButton:pressed {
                background-color: #e5e7eb;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = ButtonIconDemo()
    demo.show()
    sys.exit(app.exec())