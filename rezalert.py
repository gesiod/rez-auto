import os

import e
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient, Client
from datetime import datetime
import time
import msvcrt

load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")
timeout = 15

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

        if inp:
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {inp} pressed. Exit selected.")
            break
        else:
            if alerts_client != 0:
                try:
                    alert_kyiv_status = alerts_client.get_air_raid_alert_status(31)
                    alert_donetsk_status = alerts_client.get_air_raid_alert_status(28)
                except:
                    print("Skip...")
                    print("Skip...")
                    print("Skip...")
                    print("Skip...")
                    print("Skip...")
                    print("Skip...")
                if alert_kyiv_status and alert_donetsk_status:
                    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_kyiv_status.location_title}: is_no_alert = {alert_kyiv_status.is_no_alert()}")
                    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_donetsk_status.location_title}:  is_no_alert = {alert_donetsk_status.is_no_alert()}")
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Timed out {timeout} sec. Press any key to exit...")