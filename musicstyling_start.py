import os
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient, Client
from datetime import datetime
import time
from time import sleep
import msvcrt
import sys
import subprocess

load_dotenv()
Download_Player_PATCH = "C:\\DownloadPlayer\\DownloadPlayer.exe"
ALERT_MP3_START = "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3"
ALERT_MP3_FINISH = "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\отбой.mp3"

# print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Starting DownloadPlayer.exe")
# subprocess.Popen(f"{Download_Player_PATCH}")
#print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - ALERT_MP3_START")
#subprocess.Popen('vlc --no-loop --no-repeat --no-volume-save --mmdevice-volume=0.99 --mmdevice-audio-device="{0.0.0.00000000}.{EADDD941-5181-44FD-A51C-958110F6B5B6}" "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3"')
# --mmdevice-audio-device="{0.0.0.00000000}.{5A4ECF41-2853-49D9-AF1A-B1B474B0A419}"
#  Main Output (Komplete Audio 6 WDM Audio) SWD\MMDEVAPI\{0.0.0.00000000}.{EADDD941-5181-44FD-A51C-958110F6B5B6}
subprocess.Popen(f"{Download_Player_PATCH}")

# --alsa-audio-device="Speakers (Synaptics HD Audio)"
#  SWD\MMDEVAPI\{0.0.0.00000000}.{5A4ECF41-2853-49D9-AF1A-B1B474B0A419} 
# vlc --no-loop --no-repeat --no-volume-save --mmdevice-volume=0.99 --mmdevice-audio-device="{0.0.0.00000000}.{5A4ECF41-2853-49D9-AF1A-B1B474B0A419}" "C:\Users\IEVZPadmin\OneDrive - Carlson Rezidor (1)\IEVZP\IEVZP Alerts\тревога.mp3"
print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Waiting 300 sec.")
# sleep(300)
