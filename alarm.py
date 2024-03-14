from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
import os
import sys, time, msvcrt
import subprocess

url = "https://alarmmap.online/"
# drive = webdriver.Chrome("C:\ProgramData\chromedriver\chromedriver.exe")
drive = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

drive.get(url)
drive.maximize_window()
timeout = 15
timeour_refresh = 15
timeout_iterator = 0
startTime = time.time()
inp = None
exepttimes = 0

alarm_name_runned = ""
alarm_status = False
alarm_have_k = False
loop_skip = False

while True:
    if msvcrt.kbhit() and msvcrt.getch() == b'C':
        inp = msvcrt.getch()
        print("Key  " + f'{inp}' + " pressed. Exit ...")
        if inp != b'\xe0' and inp != b'R' and inp != b'\x00':
            drive.close()
            break
    else:
        try:
            alarm_lists = WebDriverWait(drive, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                             'amo-map-alarms-list-item-name')))  # drive.find_elements_by_class_name("amo-map-alarms-list-item-name")
            alarm_ids = WebDriverWait(drive, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                           'amo-map-alarms-list-item-info-proceed')))  # drive.find_elements_by_class_name("amo-map-alarms-list-item-info-proceed")
        except:
            alarm_lists = []
            alarm_ids = []
            print(f'There was an exception in 1st try. We reset the alarms and wait {timeout} seconds')
            sleep(timeout)
        zip_alarms = zip(alarm_lists, alarm_ids)
        # print(*zip_alarms, sep='\n')
        # print('zip_alarm len is ', zip_alarms)
        alarm_have_k = False
        print('alarm_have_k set false')
        for entry, id in zip_alarms:
            try:
                if id.text.find('\n') > 1:
                    id_text = id.text.split('\n')[0].strip()
                    entry_text = entry.text.strip()
            except:
                id_text = ''
                entry_text = ''

                exepttimes = exepttimes + 1
                if exepttimes > 3:
                    exepttimes = -1
                    print('Refresh page')
                    drive.refresh()

                print(
                    f'There was an exception 2nd try number {exepttimes}. We reset the alarms and wait {timeout} seconds')
                sleep(timeout)
            if len(id_text) > 0:
                loop_skip = False
                print(f'{datetime.now():%Y-%m-%d %H-%M-%S}', ' ::: id: [', id_text, '] entry: [', entry_text, ']',
                      sep='')
                if (entry_text == 'місто Київ'):
                    alarm_have_k = True
                    print("alarm_have_k set True")
                if (entry_text == 'місто Київ') and id_text != 'триває' and alarm_status == True:
                    alarm_status = False
                    print("alarm_status set False")
                    print(f'{datetime.now():%Y-%m-%d %H-%M-%S} :  {id_text} -- {alarm_status}')
                    os.system('taskkill /IM vlc.exe /F')
                    os.system('taskkill /IM DownloadPlayer.exe /F')
                    subprocess.Popen('"D:\DownloadPlayer\DownloadPlayer.exe"')

                if (entry_text == 'місто Київ') and id_text == 'триває' and alarm_status == False:
                    os.system('taskkill /IM vlc.exe /F')
                    os.system('taskkill /IM DownloadPlayer.exe /F')
                    subprocess.Popen(
                        'vlc --no-loop --no-repeat --no-volume-save --mmdevice-volume=0.99 "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\VUP2T alarm start eng ukr.mp3"')
                    print(f'{datetime.now():%Y-%m-%d_%H-%M-%S} : Killed DownloadPlayer.exe and run alarm...')
                    alarm_name_runned = entry_text
                    alarm_status = True
                    print("alarm_status set True")
                    print("Sleep 300 s")
                    sleep(300)
                if (alarm_status == True) and (entry_text == 'місто Київ'):
                    print(f'{datetime.now():%Y-%m-%d %H-%M-%S} -- {entry_text} -- {alarm_status} . Alarm Inprogress')
            else:
                try:
                    loop_skip = True
                    drive.refresh()
                    print(f'{datetime.now():%Y-%m-%d %H-%M-%S} -- Refresh page, skip step and wait {timeout} sec')
                    print("Refresh page, skip step and wait 5 sec")
                    sleep(timeout)
                except:
                    print("skip step and wait 5 sec")
                    sleep(timeout)
        if alarm_have_k == False and alarm_status == True and loop_skip == False:
            alarm_status = False
            print("alarm_status set False")
            print(f'{datetime.now():%Y-%m-%d %H-%M-%S} -- {id_text} -- {alarm_status} . Cancell Alarm')
            print("kill vlc and DownloadPlayer.exe")
            os.system('taskkill /IM vlc.exe /F')
            os.system('taskkill /IM DownloadPlayer.exe /F')
            subprocess.Popen(
                'vlc --no-loop --no-repeat --no-volume-save --mmdevice-volume=0.99 "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\VUP1T alarm cancel eng ukr.mp3"')
            sleep(300)
            subprocess.Popen('"D:\DownloadPlayer\DownloadPlayer.exe"')
            # subprocess.Popen('vlc --loop --random --volume-save "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\AllMusic.xspf"')
    print("Press C key to exit or wait " + f'{timeout}' + " seconds ...")
    timeout_iterator += 5
    if timeout_iterator > timeour_refresh:
        try:
            exepttimes = exepttimes + 1
            if drive.current_url != 'url':
                drive.get(url)
                print('Get url')
            elif exepttimes > 3:
                exepttimes = -1
                drive.refresh()
                print('Refresh page')
            print(drive.current_url)
            print(f'There was an exception 115 code. Try number {exepttimes}. Wait {timeout} seconds')
        except:
            print(f'{datetime.now():%Y-%m-%d %H-%M-%S} .Refresh skiped and waiting {timeout} second')
        timeout_iterator = 0
        sleep(timeout)
    sleep(timeout)


