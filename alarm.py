from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
import sys, time, msvcrt
import subprocess

url = "https://alarmmap.online/"
# drive = webdriver.Chrome("C:\ProgramData\chromedriver\chromedriver.exe")
drive = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

drive.get(url)
drive.maximize_window()
timeout = 5
startTime = time.time()
inp = None

alarm_name_runned = ""
alarm_status = False
alarm_have_k = False
loop_skip = False

while True:
    if msvcrt.kbhit():
        inp = msvcrt.getch()
        print("Key  " + f'{inp}' + " pressed. Exit ...")
        drive.close()
        break
    else:
        try:
            alarm_lists = drive.find_elements_by_class_name("amo-map-alarms-list-item-name")
            alarm_ids = drive.find_elements_by_class_name("amo-map-alarms-list-item-info-proceed")
        except:
            alarm_lists = []
            alarm_ids = []

        zip_alarms = zip(alarm_lists, alarm_ids)
        alarm_have_k = False
        for entry, id in zip_alarms:
            try:
                if id.text.find('\n') > 1:
                    id_text = id.text.split('\n')[0].strip()
                entry_text = entry.text.strip()
            except:
                id_text = ''
                entry_text = ''
            if len(id_text) > 0:
                loop_skip = False
                print(time.time(), ' ::: id: [', id_text, '] entry: [', entry_text, ']', sep='')
                if (entry_text == 'місто Київ'):
                    alarm_have_k = True
                if (entry_text == 'місто Київ') and id_text != 'триває' and alarm_status == True:
                    alarm_status = False

                    print(f'{time.time()}' + ": ", id_text, "Cancell Alarm")
                    os.system('taskkill /IM vlc.exe /F')
                    # subprocess.Popen(r'vlc https://online.radiorelax.ua/RadioRelax')

                if (entry_text == 'місто Київ') and id_text == 'триває' and alarm_status == False:
                    os.system('taskkill /IM vlc.exe /F')
                    subprocess.Popen(
                        r'vlc --no-loop --no-repeat --no-volume-save "C:\Users\Admin1\rez-auto\IEVZP тревога v1.mp3"')
                    print(f'{time.time()}' + ": Sleeping...")
                    alarm_name_runned = entry_text
                    alarm_status = True
                if alarm_status == True:
                    print(f'{time.time()}' + ": ", entry_text, "Alarm Inprogress")
            else:
                loop_skip = True
                print("Skip step")
        if alarm_have_k == False and alarm_status == True and loop_skip == False:
            alarm_status = False
            print(f'{time.time()}' + ": ", id_text, "Cancell Alarm")
            os.system('taskkill /IM vlc.exe /F')
            subprocess.Popen(
                r'vlc --no-loop --no-repeat --no-volume-save "C:\Users\Admin1\rez-auto\IEVZP отмена v1.mp3"')
            sleep(66)
            os.system('taskkill /IM vlc.exe /F')
            # subprocess.Popen(r'vlc https://online.radiorelax.ua/RadioRelax')
    print("Press any key to exit or wait " + f'{timeout}' + " seconds ...")
    sleep(timeout)


