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
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")
timeout = 15
an_alarm_occurred = False
output_devices = ["{660F4C74-75E6-4D28-9AC3-85D7DFC15C29}", # Output 3/4 (Komplete Audio 6 WDM Audio)
                  "{0.0.0.00000000}.{EADDD941-5181-44FD-A51C-958110F6B5B6}", # Main Output (Komplete Audio 6 WDM Audio)
]



if TOKEN:
    alerts_client = AlertsClient(token=TOKEN)
    inp = None
    while True:
        startTime = time.time()
        while True:
            if msvcrt.kbhit():
                inp = msvcrt.getch()
                break
            elif time.time() - startTime > timeout:
                break

        if inp == b'\x1b':
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {inp} pressed. Exit selected.")
            break
        else:
            if alerts_client != 0:
                try:
                    alert_kyiv_status = alerts_client.get_air_raid_alert_status(31)                    
                except:
                    print("Skip...")
                    print("Skip...")

                if alert_kyiv_status:
                    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_kyiv_status.location_title}: is_no_alert = {alert_kyiv_status.is_no_alert()}")
                    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - an_alarm_occurred = {an_alarm_occurred}")
                    if alert_kyiv_status.is_no_alert() != True and an_alarm_occurred != True:
                        an_alarm_occurred = True
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Killing DownloadPlayer.exe")
                        os.system('taskkill /IM DownloadPlayer.exe /F')
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Killing VLC")
                        os.system('taskkill /IM vlc.exe /F')
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - ALERT_MP3_START")
                        for output_device in output_devices:                            
                            subprocess.Popen(f'vlc --no-loop --no-repeat --no-volume-save --aout=mmdevice --mmdevice-audio-device={output_device} --mmdevice-volume=0.99 "{ALERT_MP3_START}"')
                        
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Waiting 120 sec.")
                        sleep(120)
                        
                    if alert_kyiv_status.is_no_alert() and an_alarm_occurred:
                        an_alarm_occurred = False
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Killing DownloadPlayer.exe")
                        os.system('taskkill /IM DownloadPlayer.exe /F')
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Starting ALERT_MP3_FINISH")
                        os.system('taskkill /IM vlc.exe /F')
                        
                        for output_device in output_devices: 
                            subprocess.Popen(f'vlc --no-loop --no-repeat --no-volume-save --aout=mmdevice --mmdevice-audio-device={output_device} --mmdevice-volume=0.99 --play-and-exit "{ALERT_MP3_FINISH}"')
                        
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Waiting 60 sec.")
                        sleep(60)
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Killing VLC")
                        os.system('taskkill /IM vlc.exe /F')
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Killing DownloadPlayer.exe")
                        os.system('taskkill /IM DownloadPlayer.exe /F')
                        
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Waiting 30 sec.")
                        sleep(30)
                        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Starting DownloadPlayer.exe")                  
                        subprocess.Popen(f"{Download_Player_PATCH}")
                    
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Timed out {timeout} sec. Press ECS to exit...")
