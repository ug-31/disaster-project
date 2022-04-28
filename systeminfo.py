import socket
import platform
from requests import get


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