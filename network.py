import subprocess

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