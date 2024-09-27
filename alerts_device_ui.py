import os
import sys
import subprocess
import time
from datetime import datetime
from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Checkbutton, Listbox, filedialog, DISABLED, NORMAL, MULTIPLE
from threading import Thread
from alerts_in_ua import Client as AlertsClient
from dotenv import load_dotenv, set_key, dotenv_values

# File paths
config_file = 'settings.config'

# Initial settings (these will be loaded from .config if available)
settings = {
    "ALARM_FILE": "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3",
    "CANCELLATION_FILE": "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\отбой.mp3",
    "TIMEOUT_AFTER_ALARM": 120,
    "TIMEOUT_AFTER_CLEAR": 60,
    "VERIFICATION_TIMEOUT": 8,
    "DOWNLOAD_PLAYER_PATH": "C:\\DownloadPlayer\\DownloadPlayer.exe",
    "AUDIO_DEVICES": ["{0.0.0.00000000}.{660f4c74-75e6-4d28-9ac3-85d7dfc15c29}", # Output 3/4 (Komplete Audio 6 WDM Audio)
                  "{0.0.0.00000000}.{eaddd941-5181-44fd-a51c-958110f6b5b6}"] # Main Output (Komplete Audio 6 WDM Audio)
}

# Function to load config from file
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            global settings
            settings = json.load(file)

# Function to save config to file
def save_config():
    with open(config_file, 'w') as file:
        json.dump(settings, file, indent=4)
    print("Settings saved!")

# Function to browse file
def browse_file(var, setting_key):
    file_path = filedialog.askopenfilename()
    var.set(file_path)
    settings[setting_key] = file_path
    save_config()


# Function to get audio devices from PowerShell
def get_audio_devices():
    command = [
        "powershell",
        "-Command",
        "Get-ItemProperty",
        "HKLM:\SYSTEM\CurrentControlSet\Enum\SWD\MMDEVAPI\*",
        "|",
        "Where-Object {($_.FriendlyName -Match 'Audio') -and ($_.PSChildName -Match '0\.0\.0')}",
        "|",
        "Select-Object -Property FriendlyName,PSChildName"
        "|",
        "ConvertTo-Json"
    ]
    result = subprocess.run(command, capture_output=True)
    print(result)
    output = result.stdout.decode('utf-8').strip()  # Decode bytes to string

    devices = output.splitlines()  # Split into lines
    device_list = []

    for line in devices:
        print(line)
        if "FriendlyName" in line or "PSChildName" in line:
            device_list.append(line)

    return device_list


# Load environment variables
load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")

# Initial settings loaded from .env or default values
# default_alarm_file = os.getenv("ALARM_FILE", "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\тревога.mp3")
# default_cancellation_file = os.getenv("CANCELLATION_FILE", "C:\\Users\\IEVZPadmin\\OneDrive - Carlson Rezidor (1)\\IEVZP\\IEVZP Alerts\\отбой.mp3")
# default_timeout_before_alarm = int(os.getenv("TIMEOUT_AFTER_ALARM", 120))
# default_timeout_after_clear = int(os.getenv("TIMEOUT_AFTER_CLEAR", 60))
# default_verification_timeout = int(os.getenv("VERIFICATION_TIMEOUT", 8))
# default_download_player_path = os.getenv("DOWNLOAD_PLAYER_PATH", "C:\\DownloadPlayer\\DownloadPlayer.exe")

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
    """Monitors for air raid alerts and manages the alarm states."""
    global monitoring_active
    if not TOKEN:
        print("No ALERTS_IN_UA_TOKEN found in environment variables.")
        sys.exit(1)

    alerts_client = AlertsClient(token=TOKEN)
    an_alarm_occurred = False

    monitoring_active = True
    while monitoring_active:
        try:
            alert_kyiv_status = alerts_client.get_air_raid_alert_status(31)
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_kyiv_status.location_title}: is_no_alert = {alert_kyiv_status.is_no_alert()}")
            an_alarm_occurred = handle_alert(alert_kyiv_status, an_alarm_occurred)
        except Exception as e:
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Error: {e}. Retrying...")

        time.sleep(verification_timeout.get())

def start_monitoring():
    """Starts the monitoring thread and toggles button states."""
    start_button.config(state=DISABLED)
    stop_button.config(state=NORMAL)
    
    monitoring_thread = Thread(target=monitor_alerts)
    monitoring_thread.daemon = True
    monitoring_thread.start()

def stop_monitoring():
    """Stops the monitoring and toggles button states."""
    global monitoring_active
    monitoring_active = False
    start_button.config(state=NORMAL)
    stop_button.config(state=DISABLED)

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
    save_to_env("ALARM_FILE", file_path)

def select_cancellation_file():
    file_path = filedialog.askopenfilename()
    cancellation_file.set(file_path)
    save_to_env("CANCELLATION_FILE", file_path)

def update_timeout_before_alarm(*args):
    save_to_env("TIMEOUT_BEFORE_ALARM", str(timeout_before_alarm.get()))

def update_timeout_after_clear(*args):
    save_to_env("TIMEOUT_AFTER_CLEAR", str(timeout_after_clear.get()))

def update_verification_timeout(*args):
    save_to_env("VERIFICATION_TIMEOUT", str(verification_timeout.get()))

def update_download_player_path(*args):
    save_to_env("DOWNLOAD_PLAYER_PATH", download_player_path.get())

# Function to update audio device list and save to config
def update_audio_devices(selected_devices):
    selected_device_names = [audio_devices_listbox.get(i) for i in selected_devices]
    settings["AUDIO_DEVICES"] = selected_device_names
    save_config()

# GUI setup
root = Tk()
root.title("Air Raid Alert Monitor")

# Load configuration
load_config()
# GUI Components
Label(root, text="Alarm File:").grid(row=0, column=0)
alarm_file = StringVar(value=settings["ALARM_FILE"])
Entry(root, textvariable=alarm_file, width=50).grid(row=0, column=1)
Button(root, text="Browse", command=lambda: browse_file(alarm_file, "ALARM_FILE")).grid(row=0, column=2)
alarm_file.trace_add("write", lambda *args: update_config("ALARM_FILE", alarm_file.get()))

Label(root, text="Cancellation File:").grid(row=1, column=0)
cancellation_file = StringVar(value=settings["CANCELLATION_FILE"])
Entry(root, textvariable=cancellation_file, width=50).grid(row=1, column=1)
Button(root, text="Browse", command=lambda: browse_file(cancellation_file, "CANCELLATION_FILE")).grid(row=1, column=2)
cancellation_file.trace_add("write", lambda *args: update_config("CANCELLATION_FILE", cancellation_file.get()))

Label(root, text="Timeout Before Alarm (sec):").grid(row=2, column=0)
timeout_before_alarm = IntVar(value=settings["TIMEOUT_AFTER_ALARM"])
Entry(root, textvariable=timeout_before_alarm).grid(row=2, column=1)
timeout_before_alarm.trace_add("write", lambda *args: update_config("TIMEOUT_AFTER_ALARM", timeout_before_alarm.get()))

Label(root, text="Timeout After Clear (sec):").grid(row=3, column=0)
timeout_after_clear = IntVar(value=settings["TIMEOUT_AFTER_CLEAR"])
Entry(root, textvariable=timeout_after_clear).grid(row=3, column=1)
timeout_after_clear.trace_add("write", lambda *args: update_config("TIMEOUT_AFTER_CLEAR", timeout_after_clear.get()))

Label(root, text="Verification Timeout (sec):").grid(row=4, column=0)
verification_timeout = IntVar(value=settings["VERIFICATION_TIMEOUT"])
Entry(root, textvariable=verification_timeout).grid(row=4, column=1)
verification_timeout.trace_add("write", lambda *args: update_config("VERIFICATION_TIMEOUT", verification_timeout.get()))

Label(root, text="DownloadPlayer Path:").grid(row=5, column=0)
download_player_path = StringVar(value=settings["DOWNLOAD_PLAYER_PATH"])
Entry(root, textvariable=download_player_path, width=50).grid(row=5, column=1)
download_player_path.trace_add("write", lambda *args: update_config("DOWNLOAD_PLAYER_PATH", download_player_path.get()))

Label(root, text="Select Audio Devices:").grid(row=6, column=0)
audio_devices = get_audio_devices()
audio_devices_listbox = Listbox(root, selectmode=MULTIPLE)
for device in audio_devices:
    audio_devices_listbox.insert("end", device)
audio_devices_listbox.grid(row=6, column=1, rowspan=4)
Button(root, text="Save Selected Devices", command=lambda: update_audio_devices(audio_devices_listbox.curselection())).grid(row=6, column=2)

# Start the GUI event loop
root.mainloop()