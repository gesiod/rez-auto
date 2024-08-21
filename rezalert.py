import os
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient, Client
from datetime import datetime
import time
import msvcrt

load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")
timeout = 8

if TOKEN:
    alerts_client: Client = AlertsClient(token=TOKEN)
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
            alert_status = alerts_client.get_air_raid_alert_status(31).status
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {alert_status}")
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Timed out {timeout} sec. Press any key to exit...")