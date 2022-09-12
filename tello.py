# TODO:
# !! tello.curveMpad() -- ERROR: RUN TIMEOUT ???


# Import all needed libraries
import socket
import sys
import time
import threading
import subprocess

# Set variables for connection to drone
host = ''
port = 9000
locaddr = (host,port)
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
    if "TELLO-" in data or "RMTT-" in data:
        print('Required network detected.')
    else:
        print('Network detected')
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
        if 'TELLO-' not in wifi_val or 'RMTT-' not in wifi_val:
            print('Network detected:', wifi_val)
            print('It seems like you have joined a different network. Please make sure that you have joined the TELLO-XXXXX Wi-Fi.')
            approval = input("Are you sure you want to continue with the script? (y/n)")
            if approval == 'y':
                print('\r\n')
            else:
                sys.exit()
        else:
            print('Required network detected:', wifi_val)
    except:
        print('\r\nSeems like there was an error checking the network.')
        print('Aborting script.\r\n')
        sys.exit()
else:
    print('Could not determine network.')
    print('Make sure that you are connected to the TELLO-XXXXX or RMTT-XXXXX WiFi networks.')


# Print info to the user
print('         Making UDP socket...         \r\n')
time.sleep(1)


# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)


# Class for all functions for user
class Tello:
    def __init__(self):
        self.abort = False
        self.response = None
        self.recvThread = threading.Thread(target=self.receive)
        self.recvThread.start()
    def receive(self):
        while True:
            try:
                self.response, ip = sock.recvfrom(256)
            except Exception:
                break
    def run(self, string, message="No message "):
        self.abort = False
        timer = threading.Timer(10, self._set_abort)
        # Encode the message in the utf-8 encoding
        string = string.encode(encoding='utf-8')
        # Send the encoded message to the Tello
        sent = sock.sendto(string, tello_address)
        print(message)
        self.response = None
        timer.start()
        while self.response is None:
            if self.abort is True:
                break
        timer.cancel()
        if self.response is None:
            print("ERROR: No response to latest command! \n")
            return 'error'
        if self.abort is False:
            response = self.response.decode(encoding='utf-8')
            print(response)
            self.response = None
            return response
        return 'error'
    def _set_abort(self):
        self.abort = True
    # SDK 3.0 Commands
    def throw_fly(self):
        return self.run('throwfly', 'Gently toss the drone into the air within 5 seconds!\r\n')
    def motor_on(self):
        return self.run('motoron', 'Turning on motors\r\n')
    def motor_off(self):
        return self.run('motoroff', 'Turning off motors\r\n')
    # SDK 2.0 Commands
    def connect(self):
        return self.run('command', '\r\nEnabling SDK mode\r\n')
    def takeoff(self):
        return self.run('takeoff', 'Taking off, keep clear of drone!\r\n')
    def land(self):
        return self.run('land', 'Landing, keep space clear!\r\n')
    def video_stream_on(self):
        return self.run('streamon', 'Enabling video stream\r\n')
    def video_stream_off(self):
        return self.run('streamoff', 'Disabling video stream\r\n')
    def emergency(self, reason='No reason provided'):
        print('EMERGENCY: Reason:', reason, '\r\n')
        print('EMERGENCY: Exiting script')
        self.run('emergency', 'EMERGENCY: Disabling motors\r\n')
        sys.exit()
    def stop(self):
        return self.run('stop', 'Stopping all movement, hovering.\r\n')
    def up(self, x):
        x = int(x)
        if x >= 20 and x <= 500:
            a = ' '.join(['up', str(x)])
            message = ' '.join(['Ascending to', str(x), 'cm from the ground \r\n'])
            return self.run(a, message)
        print('\r\nERROR: Parameter must be between 20 and 500')
        print('ERROR LOCATION: tello.down()\r\n')
    def down(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['down', str(x)])
                return self.run(a, ' '.join(['Descending to', str(x), 'cm from the ground \r\n']))
            print('\r\nERROR: Parameter must be between 20 and 500\r\n')
            print('ERROR LOCATION: tello.down()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.down()\r\n')
    def left(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['left', str(x)])
                return self.run(a, ' '.join(['Moving left', str(x), 'cm, keep clear of drone\'s path \r\n']))
            print('\r\nERROR: Parameter must be between 20 and 500')
            print('ERROR LOCATION: tello.left()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.left()\r\n')
    def right(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['right', str(x)])
                return self.run(a, ' '.join(['Moving right', str(x), 'cm, keep clear of drone\'s path \r\n']))
            print('\r\nERROR: Parameter must be between 20 and 500')
            print('ERROR LOCATION: tello.right()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.right()\r\n')
    def forward(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['forward', str(x)])
                return self.run(a, ' '.join(['Moving forward', str(x), 'cm, keep clear of drone\'s path \r\n']))
            print('\r\nERROR: Parameter must be between 20 and 500')
            print('ERROR LOCATION: tello.forward()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.forward()\r\n')
    def back(self, x):
        try:
            x = int(x)
            if x >= 20 and x <= 500:
                a = ' '.join(['back', str(x)])
                return self.run(a, ' '.join(['Moving forward', str(x), 'cm, keep clear of drone\'s path \r\n']))
            print('\r\nERROR: Parameter must be between 20 and 500')
            print('ERROR LOCATION: tello.back()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.back()\r\n')
    def cw(self, x):
        try:
            x = int(x)
            if x >= 1 and x <= 360:
                a = ' '.join(['cw', str(x)])
                return self.run(a, ' '.join(['Rotating clockwise for', str(x), 'degrees \r\n']))
            print('\r\nERROR: Parameter must be between 1 and 360')
            print('ERROR LOCATION: tello.cw()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.cw()\r\n')
    def ccw(self, x):
        try:
            x = int(x)
            if x >= 1 and x <= 360:
                a = ' '.join(['ccw', str(x)])
                return self.run(a, ' '.join(['Rotating counter-clockwise for', str(x), 'degrees \r\n']))
            print('\r\nERROR: Parameter must be between 1 and 360')
            print('ERROR LOCATION: tello.ccw()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.ccw()\r\n')
    def flip(self, x):
        try:
            x = str(x)
            if x in ('l', 'r', 'f', 'b'):
                a = ' '.join(['flip', x])
                return self.run(a, ' '.join(['Flipping', str(x), ', be careful \r\n']))
            print('\r\nERROR: Parameter must be either f, b, r, or l!')
            print('ERROR LOCATION: tello.flip()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be a letter!')
            print('ERROR LOCATION: tello.flip()\r\n')
    def set_speed(self, x):
        try:
            x = int(x)
            if x >= 1 and x <= 100:
                a = ' '.join(['speed', str(x)])
                return self.run(a, ' '.join(['Setting speed to', str(x), 'cm/s \r\n']))
            print('\r\nERROR: Parameter must be between 10 and 100')
            print('ERROR LOCATION: tello.setSpeed()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.setSpeed()\r\n')
    @staticmethod
    def set_wifi(ssid, passw):
        try:
            if ssid and passw:
                print('ERROR: 403 -- Operation Denied')
                print('ERROR LOCATION: tello.setWifi()')
                print('ERROR: Figure out another way.  :)\r\n')
                return 'error'
            print('\r\nERROR: Parameters must be strings!')
            print('ERROR LOCATION: tello.setWifi()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.setWifi()\r\n')
    def set_mission_on(self):
        return self.run('mon', 'Enabling Mission Pad detection\r\n')
    def set_mission_off(self):
        return self.run('moff', 'Disabling Mission Pad detection\r\n')
    def set_mission_direction(self, x):
        try:
            x = int(x)
            if x >= 0 and x <= 3:
                a = ' '.join(['mdirection', str(x)])
                return self.run(a, ' '.join(['Setting Mission Pad Detection to setting', str(x), '\r\n']))
            print('\r\nERROR: Parameter must be between 0 and 3')
            print('ERROR LOCATION: tello.setMdircetion()\r\n')
        except:
            print('\r\nERROR: Parameter needs to be an integer!')
            print('ERROR LOCATION: tello.setMdirection()\r\n')
    def get_speed(self):
        return self.run('speed?', 'Obtaining current speed: \r\n')
    def get_battery(self):
        return self.run('battery?', 'Obtaining battery level: \r\n')
    def get_time(self):
        return self.run('time?', 'Obtaining current flight time: \r\n')
    def get_wifi(self):
        return self.run('wifi?', 'Obtaining WiFi SNR: \r\n')
    def get_sdk(self):
        return self.run('sdk?', 'Obtaining Tello SDK Version: \r\n')
    def get_sn(self):
        return self.run('sn?', 'Obtaining Tello serial number: \r\n')
    def go(self, x, y, z, s):
        x = int(x)
        y = int(y)
        z = int(z)
        s = int(s)
        if 500 >= x >= -500 and 500 >= y >= -500 and 500 >= z >= -500:
            if 100 >= s >= 10:
                a = ' '.join(['go', str(x), str(y), str(z), str(s)])
                return self.run(a, ' '.join(['Going according to parameters coordinates (x, y, z):', str(x), str(y), str(z), 'at the speed of', str(s), 'cm/s\r\n']))
            print('\r\nERROR: Parameter \'s\' needs to be between 10 and 100!')
            print('ERROR LOCATION: tello.go()\r\n')
        else:
            print('\r\nERROR: Parameters x, y, z need to be between 500 and -500!')
            print('ERROR LOCATION: tello.go()\r\n')
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
                    return self.run(a, ' '.join(['Curving according to parameters (x1, x2, y1, y2, z1, z2):', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), 'at the speed of', str(s), 'cm/s\r\n']))
                print('\r\nERROR: Parameter \'s\' needs to be between 10 and 60!')
                print('ERROR LOCATION: tello.curve()\r\n')
            else:
                print('\r\nERROR: Parameters x1, x2, y1, y2, z1, z2 need to be between 500 and -500!')
                print('ERROR LOCATION: tello.curve()\r\n')
        except:
            print('\r\nERROR: Parameters need to be integers!')
            print('ERROR LOCATION: tello.curve()\r\n')
    def go_mission_pad(self, x, y, z, s, mid: str):
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
                        return self.run(a, ' '.join(['Going according to parameters coordinates (x, y, z):', str(x), str(y), str(z), 'at the speed of', str(s), 'cm/s\r\n']))
                    print('\r\nERROR: Parameter mid needs to be between m1 and m8!')
                    print('ERROR LOCATION: tello.goMpad()\r\n')
                else:
                    print('\r\nERROR: Parameter \'s\' needs to be between 10 and 100!')
                    print('ERROR LOCATION: tello.goMpad()\r\n')
            else:
                print('\r\nERROR: Parameters x, y, z need to be between 500 and -500!')
                print('ERROR LOCATION: tello.goMpad()\r\n')
        except:
            print('\r\nERROR: Parameters need to be integers!')
            print('ERROR LOCATION: tello.goMpad()\r\n')
    def curve_mission_pad(self, x1, x2, y1, y2, z1, z2, s, mid):
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
                        return self.run(a, ' '.join(['Curving according to parameters (x1, x2, y1, y2, z1, z2):',str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), 'at the speed of', str(s), 'cm/s\r\n']))
                    print('\r\nERROR: Parameter mid needs to be between m1 and m8!')
                    print('ERROR LOCATION: tello.curveMpad()\r\n')
                else:
                    print('\r\nERROR: Parameter \'s\' needs to be between 10 and 60!')
                    print('ERROR LOCATION: tello.curveMpad()\r\n')
            else:
                print('\r\nERROR: Parameters x1, x2, y1, y2, z1, z2 need to be between 500 and -500!')
                print('ERROR LOCATION: tello.curveMpad()\r\n')
        except:
            print('\r\nERROR: Parameters need to be integers!')
            print('ERROR LOCATION: tello.curveMpad()\r\n')
    @staticmethod
    def end():
        sock.close()
        print('Exiting...')
        return 'ok'
