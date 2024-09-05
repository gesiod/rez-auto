import os
import sys
import subprocess
import time
from datetime import datetime
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient
import msvcrt

# Load environment variables
load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")

# File paths and settings
DOWNLOAD_PLAYER_PATH = "C:\\DownloadPlayer\\DownloadPlayer.exe"
ALERT_MP3_START = "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3"
ALERT_MP3_FINISH = "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\отбой.mp3"
OUTPUT_DEVICES = [
    "{0.0.0.00000000}.{660f4c74-75e6-4d28-9ac3-85d7dfc15c29}",  # Output 3/4 (Komplete Audio 6 WDM Audio)
    "{0.0.0.00000000}.{eaddd941-5181-44fd-a51c-958110f6b5b6}"   # Main Output (Komplete Audio 6 WDM Audio)
]
TIMEOUT = 15

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
            f"--mmdevice-volume={volume}", "--play-and-exit", file_path
        ])

def kill_process(process_name):
    """Kills a process by name."""
    os.system(f'taskkill /IM {process_name}')

def kill_process_immid(process_name):
    """Kills a process by name."""
    os.system(f'taskkill /IM {process_name} /F')

def restart_download_player():
    """Restarts the DownloadPlayer.exe process."""
    subprocess.Popen(DOWNLOAD_PLAYER_PATH)

def handle_alert(alert_status, an_alarm_occurred):
    """Handles the alert logic based on the alert status."""
    if alert_status.is_no_alert():
        if an_alarm_occurred:
            an_alarm_occurred = False
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Alarm is over, starting ALERT_MP3_FINISH.")
            kill_process("DownloadPlayer.exe")
            play_audio_and_exit(ALERT_MP3_FINISH, OUTPUT_DEVICES)
            time.sleep(60)
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Restarting DownloadPlayer.exe.")
            restart_download_player()
    else:
        if not an_alarm_occurred:
            an_alarm_occurred = True
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Alarm started, playing ALERT_MP3_START.")
            kill_process("DownloadPlayer.exe")
            play_audio_and_exit(ALERT_MP3_START, OUTPUT_DEVICES)
            time.sleep(120)

    return an_alarm_occurred

def main():
    if not TOKEN:
        print("No ALERTS_IN_UA_TOKEN found in environment variables.")
        sys.exit(1)

    alerts_client = AlertsClient(token=TOKEN)
    an_alarm_occurred = False

    while True:
        start_time = time.time()

        while time.time() - start_time <= TIMEOUT:
            if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
                print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - ESC pressed. Exiting...")
                return

        try:
            alert_kyiv_status = alerts_client.get_air_raid_alert_status(31)
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_kyiv_status.location_title}: is_no_alert = {alert_kyiv_status.is_no_alert()}")
            an_alarm_occurred = handle_alert(alert_kyiv_status, an_alarm_occurred)
        except Exception as e:
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Error: {e}. Retrying...")

        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Timed out {TIMEOUT} sec. Press ESC to exit...")

if __name__ == "__main__":
    main()