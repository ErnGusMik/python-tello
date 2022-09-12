# TODO:
# !! tello.curveMpad() -- ERROR: RUN TIMEOUT ???
from operator import contains
import string
import sentry_sdk
sentry_sdk.init(
    dsn="https://f2fcaa10be4f41958ab756183583ba81@o1400261.ingest.sentry.io/6728983",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


# Import all needed libraries
import socket
import sys
import time
import threading
import subprocess

# Class for all functions for user
class Tello:
    def __init__(self, prints=True):

        # Set self variables
        self.sock = None
        self.response = None
        self.tello_address = None
        self.abort = False
        self.response = None
        self.sent = None
        self.ip = None

        # Set variables for connection to drone
        host = ''
        port = 9000
        locaddr = (host,port)
        self.mids = 'm1 m2 m3 m4 m5 m6 m7 m8'

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
            wifi = subprocess.check_output(['/windows/system32/netsh', 'WLAN', 'show', 'interfaces'])
            data = wifi.decode('utf-8')
            wifi_val = 'Not connected'
            for line in data.split('\n'):
                if "SSID: " in line:
                    key, val = line.split(': ')
                    val = val.strip()
                    wifi_val = val
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
        else:
            print('Could not determine network.')
            print('Make sure that you are connected to the TELLO-XXXXX or RMTT-XXXXX WiFi networks.')


        # Print info to the user
        print('         Making UDP socket...         \r\n')
        time.sleep(1)


        # Create UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = ('192.168.10.1', 8889)
        self.sock.bind(locaddr)

        self.recvThread = threading.Thread(target=self.receive)
        self.recvThread.start()

    # Function to receive commands from the drone
    def receive(self):
        while True:
            try:
                self.response, self.ip = self.sock.recvfrom(256)
            except Exception:
                break
    def run(self, string: str, message: str = "No message "):
        self.abort = False
        timer = threading.Timer(10, self._set_abort)
        # Encode the message in the utf-8 encoding
        string = string.encode(encoding='utf-8')
        # Send the encoded message to the Tello
        self.sent = self.sock.sendto(string, self.tello_address)
        print(message)
        self.response = None
        timer.start()
        while self.response is None:
            if self.abort is True:
                break
        timer.cancel()
        if self.response == None:
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
    def reboot(self):
        test = self.run('reboot', 'Rebooting\r\n')
        if test == 'error':
            return 'error'
        return 'ok'
    # SDK 3.0 SET Commands
    def rc(self, roll: int = 0, pitch: int = 0, yaw: int = 0, throttle: int = 0):
        if 100 >= roll >= -100 and 100 >= pitch >= -100 and 100 >= yaw >= -100 and 100 >= throttle >= -100:
            self.run('rc %s %s %s %s' % (roll, pitch, yaw, throttle), 'Setting lever force values\r\n')
            return 'ok'
        print('ERROR: Parameters must be between -100 and 100')
        print('ERROR LOCATION: tello.rc()')
        return 'error'
    def ap(self, ssid: str, password: str):
        return self.run('ap %s %s' % (ssid, password), 'Connecting to access point, then rebooting\r\n')
    def set_wifi_channel(self, channel: int):
        return self.run('wifi %s' % channel, 'Setting Wi-Fi channel to ' + channel + '\r\n')
    def set_port(self, info_port: int, video_port: int):
        if 1025 <= info_port <= 65535 and 1025 <= video_port <= 65535:
            ports = self.run('port %s %s' % (info_port, video_port), 'Setting new ports for status and video\r\n')
            if ports == 'ok':
                self.tello_address = ('192.168.10.1', info_port)
                #
                # SET VIDEO PORT
                #
                return 'ok'
            return 'error'
        return 'error'
    def set_fps(self, fps: str):
        if fps in ('h', 'm', 'l', 'high', 'medium', 'low'):
            return self.run('setfps %s' % fps, 'Setting FPS to ' + fps + '\r\n')
        return 'error'
    def set_bitrate(self, bitrate: int):
        if 1 <= bitrate <= 5:
            return self.run('setbitrate %s' % bitrate, 'Setting bitrate to ' + bitrate + ' Mbps\r\n')
        elif bitrate == 0:
            return self.run('setbitrate %s' % bitrate, 'Setting bitrate to auto\r\n')
        return 'error'
    def set_resolution(self, resolution: str):
        if resolution in ('h', 'l', 'high', 'low'):
            return self.run('setresolution %s' % resolution, 'Setting resolution to ' + resolution + '\r\n')
        return 'error'
    def set_rmtt_wifi(self, ssid: str, password: str):
        return self.run('multwifi %s %s' % (ssid, password), 'Setting RMTT SSID and password to %s %s\r\n' % (ssid, password))
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
    def up(self, x: int):
        if x >= 20 and x <= 500:
            a = ' '.join(['up', str(x)])
            message = ' '.join(['Ascending to', str(x), 'cm from the ground \r\n'])
            return self.run(a, message)
        print('\r\nERROR: Parameter must be between 20 and 500')
        print('ERROR LOCATION: tello.down()\r\n')
    def down(self, x: int):
        if x >= 20 and x <= 500:
            a = ' '.join(['down', str(x)])
            return self.run(a, ' '.join(['Descending to', str(x), 'cm from the ground \r\n']))
        print('\r\nERROR: Parameter must be between 20 and 500\r\n')
        print('ERROR LOCATION: tello.down()\r\n')
    def left(self, x: int):
        if x >= 20 and x <= 500:
            a = ' '.join(['left', str(x)])
            return self.run(a, ' '.join(['Moving left', str(x), 'cm, keep clear of drone\'s path \r\n']))
        print('\r\nERROR: Parameter must be between 20 and 500')
        print('ERROR LOCATION: tello.left()\r\n')
    def right(self, x: int):
        if x >= 20 and x <= 500:
            a = ' '.join(['right', str(x)])
            return self.run(a, ' '.join(['Moving right', str(x), 'cm, keep clear of drone\'s path \r\n']))
        print('\r\nERROR: Parameter must be between 20 and 500')
        print('ERROR LOCATION: tello.right()\r\n')
    def forward(self, x: int):
        if x >= 20 and x <= 500:
            a = ' '.join(['forward', str(x)])
            return self.run(a, ' '.join(['Moving forward', str(x), 'cm, keep clear of drone\'s path \r\n']))
        print('\r\nERROR: Parameter must be between 20 and 500')
        print('ERROR LOCATION: tello.forward()\r\n')
    def back(self, x: int ):
        if x >= 20 and x <= 500:
            a = ' '.join(['back', str(x)])
            return self.run(a, ' '.join(['Moving forward', str(x), 'cm, keep clear of drone\'s path \r\n']))
        print('\r\nERROR: Parameter must be between 20 and 500')
        print('ERROR LOCATION: tello.back()\r\n')
    def cw(self, x: int):
        if x >= 1 and x <= 360:
            a = ' '.join(['cw', str(x)])
            return self.run(a, ' '.join(['Rotating clockwise for', str(x), 'degrees \r\n']))
        print('\r\nERROR: Parameter must be between 1 and 360')
        print('ERROR LOCATION: tello.cw()\r\n')
    def ccw(self, x: int):
        if x >= 1 and x <= 360:
            a = ' '.join(['ccw', str(x)])
            return self.run(a, ' '.join(['Rotating counter-clockwise for', str(x), 'degrees \r\n']))
        print('\r\nERROR: Parameter must be between 1 and 360')
        print('ERROR LOCATION: tello.ccw()\r\n')
    def flip(self, x: int):
        if x in ('l', 'r', 'f', 'b'):
            a = ' '.join(['flip', x])
            return self.run(a, ' '.join(['Flipping', str(x), ', be careful \r\n']))
        print('\r\nERROR: Parameter must be either f, b, r, or l!')
        print('ERROR LOCATION: tello.flip()\r\n')
    def set_speed(self, x: int):
        if x >= 1 and x <= 100:
            a = ' '.join(['speed', str(x)])
            return self.run(a, ' '.join(['Setting speed to', str(x), 'cm/s \r\n']))
        print('\r\nERROR: Parameter must be between 10 and 100')
        print('ERROR LOCATION: tello.setSpeed()\r\n')
    def set_wifi(self, ssid: str, passw: str):
        return self.run(' '.join(['wifi', ssid, passw]), ' '.join(['Setting wifi to', ssid, 'with password', passw, 'then rebooting\r\n']))
    def set_mission_on(self):
        return self.run('mon', 'Enabling Mission Pad detection\r\n')
    def set_mission_off(self):
        return self.run('moff', 'Disabling Mission Pad detection\r\n')
    def set_mission_direction(self, x: int):
        if x >= 0 and x <= 3:
            a = ' '.join(['mdirection', str(x)])
            return self.run(a, ' '.join(['Setting Mission Pad Detection to setting', str(x), '\r\n']))
        else:
            print('\r\nERROR: Parameter must be between 0 and 3')
            print('ERROR LOCATION: tello.setMdircetion()\r\n')

    # GET Commands
    def get_speed(self):
        return self.run('speed?', 'Obtaining current speed \r\n')
    def get_battery(self):
        return self.run('battery?', 'Obtaining battery level \r\n')
    def get_time(self):
        return self.run('time?', 'Obtaining current flight time \r\n')
    def get_wifi(self):
        return self.run('wifi?', 'Obtaining WiFi SNR \r\n')
    def get_sdk(self):
        return self.run('sdk?', 'Obtaining Tello SDK Version \r\n')
    def get_sn(self):
        return self.run('sn?', 'Obtaining Tello serial number \r\n')
    #SDK 3.0 GET Commands
    def get_hardware(self):
        return self.run('hardware?', 'Obtaining  hardware status \r\n')
    def get_wifi_version(self):
        return self.run('wifi?', 'Obtaining RMTT WiFi version \r\n')
    def get_ap(self):
        return self.run('ap?', 'Obtaining RMTT Access Point SSID and password \r\n')
    def get_ssid(self):
        return self.run('ssid?', 'Obtaining RMTT WiFi SSID and password (if any) \r\n')
    


    # COMPLEX Commands
    def go(self, x: int, y: int, z: int, s: int):
        if 500 >= x >= -500 and 500 >= y >= -500 and 500 >= z >= -500:
            if 100 >= s >= 10:
                a = ' '.join(['go', str(x), str(y), str(z), str(s)])
                return self.run(a, ' '.join(['Going according to parameters coordinates (x, y, z):', str(x), str(y), str(z), 'at the speed of', str(s), 'cm/s\r\n']))
            print('\r\nERROR: Parameter \'s\' needs to be between 10 and 100!')
            print('ERROR LOCATION: tello.go()\r\n')
        else:
            print('\r\nERROR: Parameters x, y, z need to be between 500 and -500!')
            print('ERROR LOCATION: tello.go()\r\n')
    def curve(self, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, s: int):
        if 500 >= x1 >= -500 and 500 >= x2 >= -500 and 500 >= y1 >= -500 and 500 >= y2 >= -500 and 500 >= z1 >= -500 and 500 >= z2 >= -500:
            if 60 >= s >= 10:
                a = ' '.join(['curve', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), str(s)])
                return self.run(a, ' '.join(['Curving according to parameters (x1, x2, y1, y2, z1, z2):', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), 'at the speed of', str(s), 'cm/s\r\n']))
            print('\r\nERROR: Parameter \'s\' needs to be between 10 and 60!')
            print('ERROR LOCATION: tello.curve()\r\n')
        else:
            print('\r\nERROR: Parameters x1, x2, y1, y2, z1, z2 need to be between 500 and -500!')
            print('ERROR LOCATION: tello.curve()\r\n')
    def go_mission_pad(self, x: int, y: int, z: int, s: int, mid: str):
        mid_ok = False
        for id in self.mids.split(' '):
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
    def curve_mission_pad(self, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, s: int, mid: str):
        mid_ok = False
        for id in self.split(' '):
            if id == mid:
                mid_ok = True
                break
        if 500 >= x1 >= -500 and 500 >= x2 >= -500 and 500 >= y1 >= -500 and 500 >= y2 >= -500 and 500 >= z1 >= -500 and 500 >= z2 >= -500:
            if 60 >= s >= 10:
                if mid_ok:
                    a = ' '.join(['curve', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), str(s), str(mid)])
                    return self.run(a, ' '.join(['Curving according to parameters (x1, x2, y1, y2, z1, z2):', str(x1), str(x2), str(y1), str(y2), str(z1), str(z2), 'at the speed of', str(s), 'cm/s\r\n']))
                print('\r\nERROR: Parameter mid needs to be between m1 and m8!')
                print('ERROR LOCATION: tello.curveMpad()\r\n')
            else:
                print('\r\nERROR: Parameter \'s\' needs to be between 10 and 60!')
                print('ERROR LOCATION: tello.curveMpad()\r\n')
        else:
            print('\r\nERROR: Parameters x1, x2, y1, y2, z1, z2 need to be between 500 and -500!')
            print('ERROR LOCATION: tello.curveMpad()\r\n')
    #
    # SDK 3.0 DISPLAY Commands
    #
    def set_light_color(self, r: int, g: int, b: int):
        if 255 >= r >= 0 and 255 >= g >= 0 and 255 >= b >= 0:
            a = ' '.join(['EXT led', str(r), str(g), str(b)])
            return self.run(a, ' '.join(['Setting RMTT light color to (r, g, b):', str(r), str(g), str(b), '\r\n']))
        print('\r\nERROR: Parameters r, g, b need to be between 255 and 0!')
        print('ERROR LOCATION: tello.set_light_color()\r\n')
        return 'led error'
    def set_light_pulse(self, r: int, g: int, b: int, p: float or int):
        if 255 >= r >= 0 and 255 >= g >= 0 and 255 >= b >= 0 and 2.5 >= p >= 0.1:
            a = ' '.join(['EXT led', str(p), str(r), str(g), str(b)])
            return self.run(a, ' '.join(['Setting RMTT light color to (r, g, b):', str(r), str(g), str(b), 'with pulse of', str(p), 'Hz\r\n']))
        print('\r\nERROR: Parameters r, g, b need to be between 255 and 0!')
        print('ERROR LOCATION: tello.set_light_pulse()\r\n')
        return 'led error'
    def set_light_flash(self, r1: int, g1: int, b1: int, r2: int, g2: int, b2: int, f: float or int):
        if 255 >= r1 >= 0 and 255 >= g1 >= 0 and 255 >= b1 >= 0 and 255 >= r2 >= 0 and 255 >= g2 >= 0 and 255 >= b2 >= 0 and 2.5 >= f >= 0.1:
            a = ' '.join(['EXT led', str(f), str(r1), str(g1), str(b1), str(r2), str(g2), str(b2)])
            return self.run(a, ' '.join(['Setting RMTT light color to (r1, g1, b1):', str(r1), str(g1), str(b1), 'and (r2, g2, b2):', str(r2), str(g2), str(b2), 'with flash of', str(f), 'Hz\r\n']))
        print('\r\nERROR: Parameters r1, g1, b1, r2, g2, b2 need to be between 255 and 0, f between 0.1 and 10!')
        print('ERROR LOCATION: tello.set_light_flash()\r\n')
        return 'led error'
    def set_display_pattern(self, pattern: str):
        if pattern.split('') in ('r', 'b', 'p', '0') and 64 > pattern.length > 1:
            a = ' '.join(['EXT mled g', str(pattern)])
            return self.run(a, ' '.join(['Setting RMTT display pattern to:', str(pattern), '\r\n']))
        print('\r\nERROR: Parameter pattern needs to contain only r, b, p and 0, and must be between 1 and 64 characters!')
        print('ERROR LOCATION: tello.set_display_pattern()\r\n')
        return 'mled error'
    #
    # AWAITING TESTING
    #
    def set_display_string_direction(self, direction: str, color: str, frame_rate: float or int, pattern: str):
        if direction.split('') in ('l', 'r', 'u', 'd') and color in ('r', 'b', 'p') and 10 >= frame_rate >= 0.1 and 70 > pattern.length > 1 and pattern.split('') in ('r', 'b', 'p', '0'):
            a = ' '.join(['EXT mled', str(direction), str(color), str(frame_rate), str(pattern)])
            return self.run(a, ' '.join(['Setting RMTT string display direction to:', str(direction), 'with color:', str(color), 'and frame rate:', str(frame_rate), 'and pattern:', str(pattern), '\r\n']))
        print('\r\nERROR: Parameter pattern needs to contain only r, b, p and 0, and must be between 1 and 70 characters, color must contain r, b, or p, direction can contain only u, d, l, r, and frame rate can be a int or float between 0.1 and 10!')
        print('ERROR LOCATION: tello.set_display_string_direction()\r\n')
        return 'mled error'
    #
    # AWAITING TESTING
    #
    def set_display_image_direction(self, direction: str, color: str, frame_rate: float or int, pattern: str):
        if direction.split('') in ('l', 'r', 'u', 'd') and color in ('r', 'b', 'p') and 10 >= frame_rate >= 0.1 and 70 > pattern.length > 1 and pattern.split('') in ('r', 'b', 'p', '0'):
            a = ' '.join(['EXT mled', str(direction), str(color), str(frame_rate), str(pattern)])
            return self.run(a, ' '.join(['Setting RMTT string display direction to:', str(direction), 'with color:', str(color), 'and frame rate:', str(frame_rate), 'and pattern:', str(pattern), '\r\n']))
        print('\r\nERROR: Parameter pattern needs to contain only r, b, p and 0, and must be between 1 and 70 characters, color must contain r, b, or p, direction can contain only u, d, l, r, and frame rate can be a int or float between 0.1 and 10!')
        print('ERROR LOCATION: tello.set_display_image_direction()\r\n')
        return 'mled error'
    def set_display_ascii_character(self, character: str, color: str):
        if character == 'heart' or character == string.printable and color in ('r', 'b', 'p'):
            a = ' '.join(['EXT mled s', str(character), str(color)])
            return self.run(a, ' '.join(['Displaying ASCII character:', str(character), 'with color:', str(color), '\r\n']))
        print('\r\nERROR: Parameter character needs to be a printable character or "heart", and color must contain r, b, or p!')
        print('ERROR LOCATION: tello.set_display_ascii_character()\r\n')
        return 'mled error'
    def set_display_boot(self, pattern: str):
        if pattern.split('') in ('r', 'b', 'p', '0') and 64 > pattern.length > 1:
            a = ' '.join(['EXT mled sg', str(pattern)])
            return self.run(a, ' '.join(['Setting RMTT boot display pattern to:', str(pattern), '\r\n']))
        print('\r\nERROR: Parameter pattern needs to contain only r, b, p and 0, and must be between 1 and 64 characters!')
        print('ERROR LOCATION: tello.set_display_boot()\r\n')
        return 'mled error'
    def clear_display_boot(self):
        a = 'EXT mled sc'
        return self.run(a, ' '.join(['Clearing RMTT boot display pattern\r\n']))
    def set_display_brightness(self, brightness: int):
        if 255 >= brightness >= 0:
            a = ' '.join(['EXT mled sl', str(brightness)])
            return self.run(a, ' '.join(['Setting RMTT display brightness to:', str(brightness), '\r\n']))
        print('\r\nERROR: Parameter brightness needs to be between 0 and 255!')
        print('ERROR LOCATION: tello.set_display_brightness()\r\n')
        return 'mled error'
    def get_height(self):
        a = 'EXT tof?'
        return self.run(a, ' '.join(['Getting height...\r\n']))
    def get_rmtt_version(self):
        a = 'EXT version?'
        return self.run(a, ' '.join(['Getting RMTT version...\r\n']))
    
    # End command
    def end(self):
        self.sock.close()
        print('Exiting...')
        return 'ok'
