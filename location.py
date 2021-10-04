from geolite2 import geolite2
import socket, subprocess


print ("""
 __ _  _  _      ____  ____   __    ___  __ _ 
(  ( \/ )( \ ___(_  _)(  _ \ / _\  / __)(  / )
/    /) __ ((___) )(   )   //    \( (__  )  ( 
\_)__)\_)(_/     (__) (__\_)\_/\_/ \___)(__\_)
""")
print ("[+] Connecting to Databases........")
time.sleep(2)
print ("[+] Getting and Colecting More Info.....")
time.sleep(1)
print ("""
                                                    _       
                                                   | |      
__      _____    __ _ _ __ ___   _ __ ___  __ _  __| |_   _ 
\ \ /\ / / _ \  / _` | '__/ _ \ | '__/ _ \/ _` |/ _` | | | |
 \ V  V /  __/ | (_| | | |  __/ | | |  __/ (_| | (_| | |_| |
  \_/\_/ \___|  \__,_|_|  \___| |_|  \___|\__,_|\__,_|\__, |
                                                       __/ |
                                                      |___/ 
""")
cmd = r'C:\Program Files\Wireshark\tshark.exe -i "Wi-Fi 2"'

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
my_ip = socket.gethostbyname(socket.gethostname())
reader = geolite2.reader()

def get_ip_location(ip):
    location = reader.get(ip)

    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown"
    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown"

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown"

    return country, subdivision, city

for line in iter(process.stdout.readline, b""):
    columns = str(line).split(" ")

    if "SKYPE" in columns or "UDP" in columns:

        if "->" in columns:
            src_ip = columns[columns.index("->") - 1]
        elif "\\xe2\\x86\\x92" in columns:
            src_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
        else:
            continue

        if src_ip == my_ip:
            continue

        try:
            country, sub, city = get_ip_location(src_ip)
            print(">>> " + country + ", " + sub + ", " + city)
        except:
            try:
                real_ip = socket.gethostbyname(src_ip)
                country, sub, city = get_ip_location(real_ip)
                print ("\033[1;91m[+] Found Country: " + country + "\n Sub: " + sub + "\nCity " + city)
            except:
                print ("[-] Sorry But Not Found")
