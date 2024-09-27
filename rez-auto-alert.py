import os
import sys
import subprocess
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient
import msvcrt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFileDialog

# Load environment variables
load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")

# File paths and settings
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "download_player_path": "C:\\DownloadPlayer\\DownloadPlayer.exe",
    "alert_mp3_start": "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3",
    "alert_mp3_finish": "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\отбой.mp3",
    "output_devices": [
        "{0.0.0.00000000}.{660f4c74-75e6-4d28-9ac3-85d7dfc15c29}",
        "{0.0.0.00000000}.{eaddd941-5181-44fd-a51c-958110f6b5b6}"
    ],
    "timeout": 15
}

settings = {}


def load_settings():
    global settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
    else:
        settings = DEFAULT_SETTINGS


def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)


def play_audio(file_path, devices, volume=0.99):
    """Plays audio on specified output devices using VLC."""
    for device in devices:
        subprocess.Popen([
            "vlc", "--no-loop", "--no-repeat", "--no-volume-save",
            f"--aout=mmdevice", f"--mmdevice-audio-device={device}",
            f"--mmdevice-volume={volume}", file_path
        ])


def play_audio_and_exit(file_path, devices, volume=0.99):
    """Plays audio on specified output devices using VLC."""
    for device in devices:
        subprocess.Popen([
            "vlc", "--no-loop", "--no-repeat", "--no-volume-save",
            f"--aout=mmdevice", f"--mmdevice-audio-device={device}",
            f"--mmdevice-volume={volume}", file_path
        ])
    sys.exit()

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.download_player_path_input = QLineEdit()
        self.download_player_path_input.setPlaceholderText("Download Player Path")
        layout.addWidget(QLabel("Download Player Path:"))
        layout.addWidget(self.download_player_path_input)

        self.alert_mp3_start_input = QLineEdit()
        self.alert_mp3_start_input.setPlaceholderText("Alert MP3 Start Path")
        layout.addWidget(QLabel("Alert MP3 Start Path:"))
        layout.addWidget(self.alert_mp3_start_input)

        self.alert_mp3_finish_input = QLineEdit()
        self.alert_mp3_finish_input.setPlaceholderText("Alert MP3 Finish Path")
        layout.addWidget(QLabel("Alert MP3 Finish Path:"))
        layout.addWidget(self.alert_mp3_finish_input)

        self.timeout_input = QLineEdit()
        self.timeout_input.setPlaceholderText("Timeout (seconds)")
        layout.addWidget(QLabel("Timeout:"))
        layout.addWidget(self.timeout_input)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_settings()

    def load_settings(self):
        self.download_player_path_input.setText(settings.get("download_player_path", ""))
        self.alert_mp3_start_input.setText(settings.get("alert_mp3_start", ""))
        self.alert_mp3_finish_input.setText(settings.get("alert_mp3_finish", ""))
        self.timeout_input.setText(str(settings.get("timeout", 15)))

    def save_settings(self):
        settings["download_player_path"] = self.download_player_path_input.text()
        settings["alert_mp3_start"] = self.alert_mp3_start_input.text()
        settings["alert_mp3_finish"] = self.alert_mp3_finish_input.text()
        settings["timeout"] = int(self.timeout_input.text())
        save_settings()
        print("Settings saved.")

def main():
    load_settings()
    app = QApplication(sys.argv)

    settings = load_settings()  # Load settings at the start

    main_window = QMainWindow()  # Assuming you have a MainWindow class defined
    settings_window = SettingsWindow()  # Create an instance of the settings window

    # Connect the settings window to the main window if needed
    main_window.settings_action.triggered.connect(settings_window.show)

    main_window.show()  # Show the main window
    sys.exit(app.exec_())  # Start the application event loop

if __name__ == "__main__":
    main()