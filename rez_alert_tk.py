import os
import sys
import subprocess
import time
from datetime import datetime
from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Checkbutton, filedialog
from threading import Thread
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient

# Load environment variables
load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")

# Initial default settings
default_alarm_file = "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3"
default_cancellation_file = "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\отбой.mp3"
default_timeout_before_alarm = 120
default_timeout_after_clear = 60
default_verification_timeout = 8

# Function definitions
def play_audio(file_path, devices, volume=0.99):
    """Plays audio on specified output devices using VLC."""
    for device in devices:
        subprocess.Popen([
            "vlc", "--no-loop", "--no-repeat", "--no-volume-save",
            f"--aout=mmdevice", f"--mmdevice-audio-device={device}",
            f"--mmdevice-volume={volume}", file_path
        ])

def kill_process(process_name):
    """Kills a process by name."""
    os.system(f'taskkill /IM {process_name} /F')

def restart_download_player():
    """Restarts the DownloadPlayer.exe process."""
    subprocess.Popen(download_player_path.get())

def handle_alert(alert_status, an_alarm_occurred):
    """Handles the alert logic based on the alert status."""
    if alert_status.is_no_alert():
        if an_alarm_occurred:
            an_alarm_occurred = False
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Alarm is over, starting cancellation.")
            kill_process("DownloadPlayer.exe")
            play_audio(cancellation_file.get(), output_devices)
            time.sleep(timeout_after_clear.get())
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Restarting DownloadPlayer.exe.")
            restart_download_player()
    else:
        if not an_alarm_occurred:
            an_alarm_occurred = True
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Alarm started, playing alarm sound.")
            kill_process("DownloadPlayer.exe")
            play_audio(alarm_file.get(), output_devices)
            time.sleep(timeout_before_alarm.get())

    return an_alarm_occurred

def monitor_alerts():
    if not TOKEN:
        print("No ALERTS_IN_UA_TOKEN found in environment variables.")
        sys.exit(1)

    alerts_client = AlertsClient(token=TOKEN)
    an_alarm_occurred = False

    while True:
        try:
            alert_kyiv_status = alerts_client.get_air_raid_alert_status(31)
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_kyiv_status.location_title}: is_no_alert = {alert_kyiv_status.is_no_alert()}")
            an_alarm_occurred = handle_alert(alert_kyiv_status, an_alarm_occurred)
        except Exception as e:
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Error: {e}. Retrying...")
        
        time.sleep(verification_timeout.get())

def start_monitoring():
    if auto_run.get():
        monitoring_thread = Thread(target=monitor_alerts)
        monitoring_thread.daemon = True
        monitoring_thread.start()

def manual_start_alarm():
    kill_process("DownloadPlayer.exe")
    play_audio(alarm_file.get(), output_devices)
    time.sleep(timeout_before_alarm.get())

def manual_stop_alarm():
    kill_process("DownloadPlayer.exe")
    play_audio(cancellation_file.get(), output_devices)
    time.sleep(timeout_after_clear.get())
    restart_download_player()

def select_alarm_file():
    file_path = filedialog.askopenfilename()
    alarm_file.set(file_path)

def select_cancellation_file():
    file_path = filedialog.askopenfilename()
    cancellation_file.set(file_path)

# GUI setup
root = Tk()
root.title("Air Raid Alert Monitor")

Label(root, text="Alarm File:").grid(row=0, column=0)
alarm_file = StringVar(value=default_alarm_file)
Entry(root, textvariable=alarm_file, width=50).grid(row=0, column=1)
Button(root, text="Browse", command=select_alarm_file).grid(row=0, column=2)

Label(root, text="Cancellation File:").grid(row=1, column=0)
cancellation_file = StringVar(value=default_cancellation_file)
Entry(root, textvariable=cancellation_file, width=50).grid(row=1, column=1)
Button(root, text="Browse", command=select_cancellation_file).grid(row=1, column=2)

Label(root, text="Timeout Before Alarm (sec):").grid(row=2, column=0)
timeout_before_alarm = IntVar(value=default_timeout_before_alarm)
Entry(root, textvariable=timeout_before_alarm).grid(row=2, column=1)

Label(root, text="Timeout After Clear (sec):").grid(row=3, column=0)
timeout_after_clear = IntVar(value=default_timeout_after_clear)
Entry(root, textvariable=timeout_after_clear).grid(row=3, column=1)

Label(root, text="Verification Timeout (sec):").grid(row=4, column=0)
verification_timeout = IntVar(value=default_verification_timeout)
Entry(root, textvariable=verification_timeout).grid(row=4, column=1)

auto_run = IntVar(value=1)
Checkbutton(root, text="Run Automatically", variable=auto_run).grid(row=5, columnspan=2)

Button(root, text="Start Alarm Manually", command=manual_start_alarm).grid(row=6, column=0)
Button(root, text="Stop Alarm Manually", command=manual_stop_alarm).grid(row=6, column=1)

Button(root, text="Start Monitoring", command=start_monitoring).grid(row=7, columnspan=2)

# Start the GUI event loop
root.mainloop()