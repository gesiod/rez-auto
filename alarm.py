from selenium import webdriver 
from time import sleep
import os
import sys, time, msvcrt
import subprocess
url = "https://alarmmap.online/"
drive = webdriver.Chrome("C:\ProgramData\chromedriver\chromedriver.exe")

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
        print ("Key  " + f'{inp}' + " pressed. Exit ...")
        drive.close()        
        break
    else:
        try: 
            alarm_lists = drive.find_elements_by_class_name("amo-map-alarms-list-item-name")
            alarm_ids = drive.find_elements_by_class_name("amo-map-alarms-list-item-info-proceed")
        except: 
            alarm_lists = []
            alarm_ids = []
   
        zip_alarms =  zip(alarm_lists, alarm_ids)
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
                if (entry_text == 'місто Київ' ):
                    alarm_have_k = True    
                if (entry_text == 'місто Київ') and id_text  != 'триває' and alarm_status == True:
                    alarm_status = False
                    
                    print(f'{time.time()}' + ": ", id_text, "Cancell Alarm")
                    os.system('taskkill /IM vlc.exe /F')
                    subprocess.Popen('"D:\DownloadPlayer\DownloadPlayer.exe"')
                    #subprocess.Popen('vlc --loop --random --volume-save "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\AllMusic.xspf"')
                    
                if (entry_text == 'місто Київ') and id_text  == 'триває' and alarm_status == False:
                    os.system('taskkill /IM vlc.exe /F')
                    os.system('taskkill /IM DownloadPlayer.exe /F')
                    subprocess.Popen('vlc --no-loop --no-repeat --no-volume-save --mmdevice-volume=0.99 "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\VUP2T alarm start eng ukr.mp3"')
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
            subprocess.Popen('vlc --no-loop --no-repeat --no-volume-save --mmdevice-volume=0.99 "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\VUP1T alarm cancel eng ukr.mp3"')
            sleep(66)
            subprocess.Popen('"D:\DownloadPlayer\DownloadPlayer.exe"')
            # subprocess.Popen('vlc --loop --random --volume-save "C:\AllSyncClouds\One\OneDrive - Carlson Rezidor\IEVZH\IEVZH Air Raid\AllMusic.xspf"')
    print ("Press any key to exit or wait " + f'{timeout}' + " seconds ...")
    sleep(timeout)


