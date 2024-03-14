import os
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient, Client
import time
import msvcrt

load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")
if TOKEN:
    while True:
        alerts_client: Client = AlertsClient(token=TOKEN)
        alert_status = alerts_client.get_air_raid_alert_status(31).status
        # or alert_status = alerts_client.get_air_raid_alert_status('Луганська область')
        print(alert_status)

        timeout = 5
        startTime = time.time()
        inp = None

        while True:
            if msvcrt.kbhit():
                inp = msvcrt.getch()
                break
            elif time.time() - startTime > timeout:
                break

        if inp:
            print("Exit selected...")
            break
        else:
            print("Timed out...")