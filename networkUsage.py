import time
import psutil

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