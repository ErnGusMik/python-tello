# TODO:
# !! tello.curveMpad() -- ERROR: RUN TIMEOUT ???


# Import all needed libraries
from distutils.log import error
import numbers
import socket
import string
import sys
import time
import threading
import subprocess

# Set variables for connection to drone
host = ''
port = 9000
locaddr = (host,port)
operation_done = True
mids = 'm1 m2 m3 m4 m5 m6 m7 m8'

# Print starting info for the user
print('_________  ____                  ____ ')
print('    |      |      |      |      |    |')
print('    |      |___   |      |      |    |')
print('    |      |      |      |      |    |')
print('    |      |____  |____  |____  |____|\r\n')
print('             Drone Script             ')
print('             File edition!        \r\n')
time.sleep(0.5)
print('            Initializing...           \r\n')
time.sleep(1)

print('          Checking network...         \r\n')
time.sleep(1)


# Check what network is connected
if sys.platform == 'win32':
    wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
    data = wifi.decode('utf-8')
    wifi_val = 'Not connected'
    try:
        for line in data.split('\n'):
            if "SSID: " in line:
                key, val = line.split(': ')
                val = val.strip()
                wifi_val = val
    except:
        print('Error determining network. Continuing anyway.')
    if "TELLO-" in data:
        print('Network detected:', wifi_val)
        print('No errors. \r\n')
    else:
        print('Network detected:', wifi_val)
        print('It seems like you have joined a different network. Please make sure that you have joined the TELLO-XXXXX Wi-Fi.')
        approval = input("Are you sure you want to continue with the script? (y/n)")
        if approval == 'y':
            print('\r\n')
        else:
            sys.exit()
elif sys.platform == 'darwin':
    try:
        process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        process.wait()
        wifi_val = 'Not connected'
        for line in out.decode('utf-8').split('\n'):
            if "SSID: " in line:
                key, val = line.split(': ')
                val = val.strip()
                wifi_val = val
        if 'TELLO-' not in wifi_val:
            print('Network detected:', wifi_val)
            print('It seems like you have joined a different network. Please make sure that you have joined the TELLO-XXXXX Wi-Fi.')
            approval = input("Are you sure you want to continue with the script? (y/n)")
            if approval == 'y':
                print('\r\n')
            else:
                sys.exit()
        else:
            print('Network detected:', wifi_val)
            print('No errors. \r\n')
    except:
        print('\r\nSeems like there was an error checking the network.')
        print('Aborting script.\r\n')
        sys.exit()
else:
    print('Could not determine network.')
    print('Make sure that you are connected to the TELLO-XXXXX WiFi network.')


# Print info to the user
print('         Making UDP socket...         \r\n')
time.sleep(1)


# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)


# Function for receiving responses
def receive():
    global operation_done
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            data = data.decode(encoding='utf-8')
            print(data)
            operation_done = True
        except Exception:
            print('\nExiting...\n')
            sys.exit()


# Create receiving thread
recvThread = threading.Thread(target=receive)
recvThread.start()
print(recvThread)



# Class for all functions for user
class Tello:
    def run(self, string):
        global operation_done
        while operation_done == False:
            if operation_done:
                break
            else:
                time.sleep(0.2)
        if operation_done:
            string = string.encode(encoding='utf-8')
            operation_done = False
            sent = sock.sendto(string, tello_address)
    def init(self):
        self.run('command')
        print('\r\nEnabling SDK mode\r\n')
        operation_done = False
    def takeoff(self):
        self.run('takeoff')
        print('Taking off, keep clear of drone!\r\n')
    def land(self):
        self.run('land')
        print('Landing, keep space clear!\r\n')
    def streamon(self):
        self.run('streamon')
        print('Enabling video stream\r\n')
    def streamoff(self):
        self.run('streamoff')
        print('Disabling video stream\r\n')
    def emergency(self, reason='No reason provided'):
        self.run('emergency')
        print('EMERGENCY: Disabling motors\r\n')
        print('EMERGENCY: Reason:', reason, '\r\n')
        print('EMERGENCY: Exiting script')
        sys.exit()
    def stop(self):
        self.run('stop')
        print('Stopping all movement, hovering.\r\n')
    def up(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['up', str(x)])
                self.run(a)
                print('Ascending to', x, 'cm from the ground \r\n')
            else:
                print('\r\nERROR: Parameter must be between 20 and 500')
                print('ERROR LOCATION: tello.down()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.up()\r\n')
            global operation_done
            operation_done = True
    def down(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['down', str(x)])
                self.run(a)
                print('Descending to', x, 'cm from the ground')
            else:
                print('\r\nERROR: Parameter must be between 20 and 500\r\n')
                print('ERROR LOCATION: tello.down()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.down()\r\n')
            global operation_done
            operation_done = True
    def left(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['left', str(x)])
                self.run(a)
                print('Moving left', x, 'cm, keep clear of drone\'s path! \r\n')
            else:
                print('\r\nERROR: Parameter must be between 20 and 500')
                print('ERROR LOCATION: tello.left()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.left()\r\n')
            global operation_done
            operation_done = True
    def right(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['right', str(x)])
                self.run(a)
                print('Moving right', x, 'cm, keep clear of drone\'s path!\r\n')
            else:
                print('\r\nERROR: Parameter must be between 20 and 500')
                print('ERROR LOCATION: tello.right()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.right()\r\n')
            global operation_done
            operation_done = True
    def forward(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['forward', str(x)])
                self.run(a)
                print('Moving forward', x, 'cm, keep clear of drone\'s path!\r\n')
            else:
                print('\r\nERROR: Parameter must be between 20 and 500')
                print('ERROR LOCATION: tello.forward()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.forward()\r\n')
            global operation_done
            operation_done = True
    def back(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['back', str(x)])
                self.run(a)
                print('Moving back', x, 'cm, keep clear of drone\'s path!\r\n')
            else:
                print('\r\nERROR: Parameter must be between 20 and 500')
                print('ERROR LOCATION: tello.back()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.back()\r\n')
            global operation_done
            operation_done = True
    def cw(self, x):
        try:
            x = int(x)
            if x >= 1 and x <= 360:
                a = ' '.join(['cw', str(x)])
                self.run(a)
                print('Rotating clockwise for', x, 'degrees \r\n')
            else:
                print('\r\nERROR: Parameter must be between 1 and 360')
                print('ERROR LOCATION: tello.cw()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.cw()\r\n')
            global operation_done
            operation_done = True
    def ccw(self, x):
        try:
            x = int(x)
            if x >= 1 and x <= 360:
                a = ' '.join(['ccw', str(x)])
                self.run(a)
                print('Rotating counterclockwise for', x, 'degrees \r\n')
            else:
                print('\r\nERROR: Parameter must be between 1 and 360')
                print('ERROR LOCATION: tello.ccw()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.ccw()\r\n')
            global operation_done
            operation_done = True
    def flip(self, x):
        try:
            x = str(x)
            if x == 'l' or x == 'r' or x == 'f' or x == 'b':
                a = ' '.join(['flip', x])
                self.run(a)
                print('Flipping', x + ', be careful! \r\n')
            else:
                print('\r\nERROR: Parameter must be either f, b, r, or l!')
                print('ERROR LOCATION: tello.flip()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be a letter!')
            print('ERROR LOCATION: tello.flip()\r\n')
            global operation_done
            operation_done = True
    def setSpeed(self, x):
        try:
            x = int(x)
            if x >= 1 and x <= 100:
                a = ' '.join(['speed', str(x)])
                self.run(a)
                print('Setting speed to', x, 'cm/s \r\n')
            else:
                print('\r\nERROR: Parameter must be between 10 and 100')
                print('ERROR LOCATION: tello.setSpeed()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.setSpeed()\r\n')
            global operation_done
            operation_done = True
    def setWifi(self, ssid, passw):
        try:
            if ssid and passw:
                print('ERROR: 403 -- Operation Denied')
                print('ERROR LOCATION: tello.setWifi()')
                print('ERROR: Figure out another way.\r\n')
                global operation_done
                operation_done = True
            else:
                print('\r\nERROR: Parameters must be strings!')
                print('ERROR LOCATION: tello.setWifi()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.setWifi()\r\n')
            global operation_done
            operation_done = True
    def setMon(self):
        self.run('mon')
        print('Enabling Mission Pad detection\r\n')
    def setMoff(self):
        self.run('moff')
        print('Disabling Mission Pad detection\r\n')
    def setMdirection(self, x):
        try:
            x = int(x)
            if x >= 0 and x <= 3:
                a = ' '.join(['mdirection', str(x)])
                self.run(a)
                print('Setting Mission Pad Detection to setting', x)
            else:
                print('\r\nERROR: Parameter must be between 0 and 3')
                print('ERROR LOCATION: tello.setMdircetion()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.setMdirection()\r\n')
            global operation_done
            operation_done = True
    def getSpeed(self):
        self.run('speed?')
        print('\r\nObtaining current speed:')
    def getBattery(self):
        self.run('battery?')
        print('\r\nObtaining battery level:')
    def getTime(self):
        self.run('time?')
        print('\r\nObtaining current flight time:')
    def getWifi(self):
        self.run('wifi?')
        print('\r\nGathering WiFi SNR:')
    def getSDK(self):
        self.run('sdk?')
        print('\r\nGetting Tello SDK Version:')
    def getSN(self):
        self.run('sn?')
        print('\r\nGetting Tello serial number:')
    def go(self, x, y, z, s):
        x = int(x)
        y = int(y)
        z = int(z)
        s = int(s)
        if 500 >= x >= -500 and 500 >= y >= -500 and 500 >= z >= -500:
            if 100 >= s >= 10:
                a = ' '.join(['go', str(x), str(y), str(z), str(s)])
                self.run(a)
                print('Going according to parameters coordinates (x, y, z):', x, y, z, 'at the speed of', s, 'cm/s')
            else:
                print('\r\nERROR: Parameter \'s\' needs to be between 10 and 100!')
                print('ERROR LOCATION: tello.go()\r\n')
                global operation_done
                operation_done = True
        else:
            print('\r\nERROR: Parameters x, y, z need to be between 500 and -500!')
            print('ERROR LOCATION: tello.go()\r\n')
            global operation_done
            operation_done = True
    def curve(self, x1, x2, y1, y2, z1, z2, s):
        try:
            x1 = int(x1)
            y1 = int(y1)
            z1 = int(z1)
            x2 = int(x2)
            y2 = int(y2)
            z2 = int(z2)
            s = int(s)
            if 500 >= x1 >= -500 and 500 >= x2 >= -500 and 500 >= y1 >= -500 and 500 >= y2 >= -500 and 500 >= z1 >= -500 and 500 >= z2 >= -500:
                if 60 >= s >= 10:
                    a = ' '.join(['curve', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), str(s)])
                    self.run(a)
                    print('Curving according to parameters (x1, x2, y1, y2, z1, z2):', x1, x2, y1, y2, z1, z2, 'at the speed of', s, 'cm/s')
                else:
                    print('\r\nERROR: Parameter \'s\' needs to be between 10 and 60!')
                    print('ERROR LOCATION: tello.curve()\r\n')
                    global operation_done
                    operation_done = True
            else:
                print('\r\nERROR: Parameters x1, x2, y1, y2, z1, z2 need to be between 500 and -500!')
                print('ERROR LOCATION: tello.curve()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameters need to be integers!')
            print('ERROR LOCATION: tello.curve()\r\n')
            global operation_done
            operation_done = True
    def goMpad(self, x, y, z, s, mid: str):
        global mids
        try:
            x = int(x)
            y = int(y)
            z = int(z)
            s = int(s)
            mid = str(mid)
            mid_ok = False
            for id in mids.split(' '):
                if id == mid:
                    mid_ok = True
                    break
            if 500 >= x >= -500 and 500 >= y >= -500 and 500 >= z >= -500:
                if 100 >= s >= 10:
                    if mid_ok:
                        a = ' '.join(['go', str(x), str(y), str(z), str(s), str(mid)])
                        self.run(a)
                        print('Going according to parameters coordinates (x, y, z):', x, y, z, 'at the speed of', s, 'cm/s')
                    else:
                        print('\r\nERROR: Parameter mid needs to be between m1 and m8!')
                        print('ERROR LOCATION: tello.goMpad()\r\n')
                        global operation_done
                        operation_done = True
                else:
                    print('\r\nERROR: Parameter \'s\' needs to be between 10 and 100!')
                    print('ERROR LOCATION: tello.goMpad()\r\n')
                    global operation_done
                    operation_done = True
            else:
                print('\r\nERROR: Parameters x, y, z need to be between 500 and -500!')
                print('ERROR LOCATION: tello.goMpad()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameters need to be integers!')
            print('ERROR LOCATION: tello.goMpad()\r\n')
            global operation_done
            operation_done = True
    def curveMpad(self, x1, x2, y1, y2, z1, z2, s, mid):
        global mids
        try:
            x1 = int(x1)
            y1 = int(y1)
            z1 = int(z1)
            x2 = int(x2)
            y2 = int(y2)
            z2 = int(z2)
            s = int(s)
            mid = str(mid)
            mid_ok = False
            for id in mids.split(' '):
                if id == mid:
                    mid_ok = True
                    break
            if 500 >= x1 >= -500 and 500 >= x2 >= -500 and 500 >= y1 >= -500 and 500 >= y2 >= -500 and 500 >= z1 >= -500 and 500 >= z2 >= -500:
                if 60 >= s >= 10:
                    if mid_ok:
                        a = ' '.join(['curve', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), str(s), str(mid)])
                        self.run(a)
                        print('Curving according to parameters (x1, x2, y1, y2, z1, z2):', x1, x2, y1, y2, z1, z2, 'at the speed of', s, 'cm/s')
                    else:
                        print('\r\nERROR: Parameter mid needs to be between m1 and m8!')
                        print('ERROR LOCATION: tello.curveMpad()\r\n')
                        global operation_done
                        operation_done = True
                else:
                    print('\r\nERROR: Parameter \'s\' needs to be between 10 and 60!')
                    print('ERROR LOCATION: tello.curveMpad()\r\n')
                    global operation_done
                    operation_done = True
            else:
                print('\r\nERROR: Parameters x1, x2, y1, y2, z1, z2 need to be between 500 and -500!')
                print('ERROR LOCATION: tello.curveMpad()\r\n')
                global operation_done
                operation_done = True
        except:
            print('\r\nERROR: Parameters need to be integers!')
            print('ERROR LOCATION: tello.curveMpad()\r\n')
            global operation_done
            operation_done = True
    def end(self):
        sock.close()
        print('Exiting...')
        sys.exit()
