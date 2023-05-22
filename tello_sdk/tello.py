"""Unofficial Tello SDK for Python 3.6 or higher."""
# Class for all functions for user
class Tello:
    """Class for info commands to the Tello or RMTT drones"""
    def __init__(self, log_in_console: bool = True, tips: bool = True):
        """Checks network name, creates UDP socket and prints starting info to user"""
        import logging
        import sentry_sdk
        import sys
        import time
        import subprocess
        import socket
        import threading

        # Initialize Sentry (error catching)
        # Delete the following 4 lines to opt out
        # More: sentry.io

        # ------------------ #
        sentry_sdk.init(
            dsn="https://f2fcaa10be4f41958ab756183583ba81@o1400261.ingest.sentry.io/6728983",
            traces_sample_rate=1.0,
        )
        # ------------------ #
        # Configure self.logging
        if log_in_console:
            logging.basicConfig(
                format="%(asctime)s [%(levelname)s] %(message)s ",
                datefmt="%H:%M:%S",
                level=logging.INFO,
                handlers=[
                    logging.StreamHandler(sys.stdout),
                    logging.FileHandler("debug.log", mode="w"),
                ],
            )
        else:
            logging.basicConfig(
                format="%(asctime)s [%(levelname)s] %(message)s ",
                datefmt="%H:%M:%S",
                level=logging.DEBUG,
                filename="debug.log",
                filemode="w",
            )

        # Set self variables
        self.logging = logging
        self.tips = tips
        self.sock = None
        self.response = None
        self.tello_address = None
        self.abort = False
        self.response = None
        self.sent = None
        self.ip_addr = None
        self.status_port = 8889
        self.video_port = 11111

        # Set variables for connection to drone
        host = ""
        port = 9000
        locaddr = (host, port)
        self.mids = "m1 m2 m3 m4 m5 m6 m7 m8"

        # Print starting info for the user
        self.logging.info("--------------------------------------")
        self.logging.info("_________  ____                  ____ ")
        self.logging.info("    |      |      |      |      |    |")
        self.logging.info("    |      |___   |      |      |    |")
        self.logging.info("    |      |      |      |      |    |")
        self.logging.info("    |      |____  |____  |____  |____|\r\n")
        self.logging.info("             Drone Script             ")
        self.logging.info("--------------------------------------")

        self.logging.debug("Current port for UDP connection: %s", str(port))

        self.logging.info("          Checking network...         \r\n")
        time.sleep(0.5)

        # Check what network is connected
        if sys.platform == "win32":
            wifi = subprocess.check_output(
                ["/windows/system32/netsh", "WLAN", "show", "interfaces"])
            data = wifi.decode("utf-8")
            wifi_val = "Not connected"
            for line in data.split("\n"):
                if "SSID: " in line:
                    _, val = line.split(": ")
                    val = val.strip()
                    wifi_val = val
            if "TELLO-" in data or "RMTT-" in data:
                self.logging.debug("Required network detected.")
            else:
                self.logging.debug("Network detected")
                self.logging.warning(
                    "It seems like you have not joined the TELLO- or RMTT-network. Please make sure that you have joined the TELLO- or RMTT- Wi-Fi."
                )
        elif sys.platform == "darwin":
            process = subprocess.Popen(
                [
                    "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                    "-I",
                ],
                stdout=subprocess.PIPE,
            )
            out, _ = process.communicate()
            process.wait()
            wifi_val = "Not connected"
            for line in out.decode("utf-8").split("\n"):
                if "SSID: " in line:
                    _, val = line.split(": ")
                    val = val.strip()
                    wifi_val = val
            if "TELLO-" not in wifi_val or "RMTT-" not in wifi_val:
                self.logging.debug("Network detected: %s", wifi_val)
                self.logging.warning(
                    "It seems like you have joined a different network. Please make sure that you have joined the TELLO-XXXXX Wi-Fi."
                )
            else:
                self.logging.debug("Required network detected: %s", wifi_val)
        else:
            self.logging.warning("Could not determine network.")
            self.logging.warning(
                "Make sure that you are connected to the TELLO-XXXXX or RMTT-XXXXX WiFi networks."
            )

        # Print info to the user
        self.logging.info("         Making UDP socket...         \r\n")
        time.sleep(1)

        # Create UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = ("192.168.10.1", 8889)
        self.sock.bind(locaddr)
        self.logging.debug("Socket created.")
        self.logging.debug("Socket bound to: %s", str(locaddr))

        self.recv_thread = threading.Thread(target=self.receive)
        self.recv_thread.start()
        self.logging.debug("Receive thread started.")
        self.logging.debug("--------------------------------------\r\n")

    # Function to receive commands from the drone
    def receive(self):
        """Receives UDP messages from the drone"""
        import socket
        while True:
            try:
                self.response, self.ip_addr = self.sock.recvfrom(256)
            except socket.error as exc:
                self.logging.critical("Error receiving response: %s", exc)
                break

    def run(self,
            command: str,
            message: str = "No tips available for this command "):
        """Sends command to the drone and prints message to the user"""
        import threading
        self.abort = False
        timer = threading.Timer(10, self._set_abort)
        # Encode the message in the utf-8 encoding
        command = command.encode(encoding="utf-8")
        # Send the encoded message to the Tello
        self.sent = self.sock.sendto(command, self.tello_address)
        if self.tips:
            print("--:--:-- [TIP] " + message)
        self.response = None
        timer.start()
        while self.response is None:
            if self.abort is True:
                break
        timer.cancel()
        if self.response is None:
            self.logging.warning("Command timed out.")
            return "error"
        if self.abort is False:
            response = self.response.decode(encoding="utf-8")
            self.response = None
            self.logging.debug("Response to previous command: %s", response)
            return response
        return "error"

    def _set_abort(self):
        """Sets the abort variable to True"""
        self.abort = True

    # SDK 3.0 Commands
    def throw_fly(self):
        """Sends command to the drone to fly when tossed"""
        self.logging.debug("Sending command: throw_fly()")
        return self.run(
            "throwfly",
            "Gently toss the drone into the air within 5 seconds!\r\n")

    def motors_on(self):
        """Sends command to turn on motors"""
        self.logging.debug("Sending command: motor_on()")
        return self.run("motoron", "Turning on motors\r\n")

    def motors_off(self):
        """Sends command to turn off motors"""
        self.logging.debug("Sending command: motor_off()")
        return self.run("motoroff", "Turning off motors\r\n")

    def reboot(self):
        """Sends command to reboot the drone"""
        self.logging.debug("Sending command: reboot()")
        test = self.run("reboot", "Rebooting\r\n")
        if test == "error":
            self.logging.warning("Reboot failed.")
            return "error"
        self.logging.info("Rebooting. Please wait 30 seconds.")
        return "ok"

    # SDK 3.0 SET Commands
    def rc(self,
           roll: int = 0,
           pitch: int = 0,
           throttle: int = 0,
           yaw: int = 0):
        """Sends command to adjust lever force values (acc. to official docs)"""
        self.logging.debug("Sending command: rc()")
        if (100 >= roll >= -100 and 100 >= pitch >= -100 and 100 >= yaw >= -100
                and 100 >= throttle >= -100):
            self.run(f"rc {roll} {pitch} {throttle} {yaw}",
                     "Setting lever force values\r\n")
            return "ok"
        self.logging.warning("tello.rc(): Invalid value.")
        return "error"

    def set_ap(self, ssid: str, password: str):
        """Sends command to join access point, then reboot"""
        self.logging.debug("Sending command: ap()")
        return self.run(f"ap {ssid} {password}",
                        "Connecting to access point, then rebooting\r\n")

    def set_wifi_channel(self, channel: int):
        """Sends command to set the WiFi channel"""
        self.logging.debug("Sending command: set_wifi_channel()")
        return self.run(
            f"wifisetchannel {channel}",
            f"Setting Wi-Fi channel to {channel} channel\r\n",
        )

    def set_ports(self, status_port: int, video_port: int):
        """Sends command to set the ports for status and video"""
        self.logging.debug("Sending command: set_ports()")
        if 1025 <= status_port <= 65535 and 1025 <= video_port <= 65535:
            ports = self.run(
                f"port {status_port} {video_port}",
                "Setting new ports for status and video\r\n",
            )
            if ports == "ok":
                self.logging.info("New ports set by client: %s and %s", status_port,
                             video_port)
                # self.info_port = status_port
                # self.tello_address = ('192.168.10.1', info_port)
                #
                # SET VIDEO PORT
                #
                return "ok"
            self.logging.warning("tello.set_ports(): Failed to set ports.")
            self.logging.debug(
                "Failed to set ports due to an error response from the drone.")
            return "error"
        self.logging.warning("tello.set_ports(): Invalid value.")
        return "error"

    def set_fps(self, fps: str):
        """Sends command to set the video stream frame rate"""
        self.logging.debug("Sending command: set_fps()")
        if fps in ("h", "m", "l", "high", "medium", "low"):
            return self.run(f"setfps {fps}", f"Setting FPS to {fps} fps \r\n")
        self.logging.warning("tello.set_fps(): Invalid value.")
        return "error"

    def set_bitrate(self, bitrate: int):
        """Sends command to set the video stream bitrate"""
        self.logging.debug("Sending command: set_bitrate()")
        if 1 <= bitrate <= 5:
            return self.run(f"setbitrate {bitrate}",
                            f"Setting bitrate to {bitrate} Mbps\r\n")
        if bitrate == 0:
            return self.run(f"setbitrate {bitrate}",
                            "Setting bitrate to auto\r\n")
        self.logging.warning("tello.set_bitrate(): Invalid value.")
        return "error"

    def set_resolution(self, resolution: str):
        """Sends command to set the video stream resolution"""
        self.logging.debug("Sending command: set_resolution()")
        if resolution in ("h", "l", "high", "low"):
            return self.run(
                f"setresolution {resolution}",
                f"Setting resolution to {resolution} \r\n",
            )
        self.logging.warning("tello.set_resolution(): Invalid value.")
        return "error"

    def set_rmtt_wifi(self, ssid: str, password: str):
        """Sends command to set the RMTT WiFi SSID and password"""
        self.logging.debug("Sending command: set_rmtt_wifi()")
        return self.run(
            f"multwifi {ssid} {password}",
            f"Setting RMTT SSID and password to {ssid} {password} \r\n",
        )

    # SDK 2.0 Commands
    def init(self):
        """Sends command to initialize SDK mode"""
        self.logging.debug("Sending command: init()")
        return self.run("command", "Enabling SDK mode\r\n")

    def takeoff(self):
        """Sends command to take off"""
        self.logging.debug("Sending command: takeoff()")
        return self.run("takeoff", "Taking off, keep clear of drone!\r\n")

    def land(self):
        """Sends command to land"""
        self.logging.debug("Sending command: land()")
        return self.run("land", "Landing, keep space clear!\r\n")

    def video_stream_on(self):
        """Sends command to turn on video stream"""
        self.logging.debug("Sending command: video_stream_on()")
        return self.run("streamon", "Enabling video stream\r\n")

    def video_stream_off(self):
        """Sends command to turn off video stream"""
        self.logging.debug("Sending command: video_stream_off()")
        return self.run("streamoff", "Disabling video stream\r\n")

    def emergency(self, reason="No reason provided"):
        """Sends command to stop all motors"""
        import sys
        self.logging.debug("Sending command: emergency()")
        self.run("emergency", "Emergency stop. Attempting to stop motors.\r\n")
        self.logging.critical("Emergency stop. Exiting script.")
        self.logging.debug(
            "Emergency stop due to: %s. Unable to continue due to motor stop. Exiting.",
            reason,
        )
        sys.exit()

    def hover(self):
        """Sends command to stop all movement, hover"""
        self.logging.debug("Sending command: hover()")
        return self.run("stop", "Stopping all movement, hovering.\r\n")

    def up(self, x: int):
        """Sends command to move up x cm"""
        self.logging.debug("Sending command: up()")
        if 20 <= x <= 500:
            return self.run(f"up {str(x)}",
                            f"Ascending to {str(x)} cm from the ground \r\n")
        self.logging.warning("tello.up(): Invalid value.")
        return "error"

    def down(self, x: int):
        """Sends command to move down x cm"""
        self.logging.debug("Sending command: down()")
        if 20 <= x <= 500:
            return self.run(f"down {str(x)}",
                            f"Descending to {str(x)} cm from the ground \r\n")
        self.logging.warning("tello.down(): Invalid value.")
        return "error"

    def left(self, x: int):
        """Sends command to move left x cm"""
        self.logging.debug("Sending command: left()")
        if 20 <= x <= 500:
            return self.run(
                f"left {str(x)}",
                f"Moving left {str(x)} cm, keep clear of drone's path \r\n",
            )
        self.logging.warning("tello.left(): Invalid value.")
        return "error"

    def right(self, x: int):
        """Sends command to move right x cm"""
        self.logging.debug("Sending command: right()")
        if 20 <= x <= 500:
            return self.run(
                f"right {str(x)}",
                f"Moving right {str(x)} cm, keep clear of drone's path \r\n",
            )
        self.logging.warning("tello.right(): Invalid value.")
        return "error"

    def forward(self, x: int):
        """Sends command to move forward x cm"""
        self.logging.debug("Sending command: forward()")
        if 20 <= x <= 500:
            return self.run(
                f"forward {str(x)}",
                f"Moving forward {str(x)} cm, keep clear of drone's path \r\n",
            )
        self.logging.warning("tello.forward(): Invalid value.")
        return "error"

    def back(self, x: int):
        """Sends command to move back x cm"""
        self.logging.debug("Sending command: back()")
        if 20 <= x <= 500:
            return self.run(
                f"back {str(x)}",
                f"Moving forward {str(x)} cm, keep clear of drone's path \r\n",
            )
        self.logging.warning("tello.back(): Invalid value.")
        return "error"

    def rotate(self, direction: str, degrees: int):
        """Sends command to rotate clockwise or anti-clockwise for specified amount of degrees"""
        self.logging.debug("Sending command: cw()")
        if 1 <= degrees <= 360:
            if direction == "cw":
                return self.run(
                    f"cw {str(degrees)}",
                    f"Rotating clockwise {str(degrees)} degrees \r\n",
                )
            if direction == "ccw":
                return self.run(
                    f"ccw {str(degrees)}",
                    f"Rotating counter-clockwise {str(degrees)} degrees \r\n",
                )
            self.logging.warning("tello.rotate(): Invalid direction.")
            return "error"
        self.logging.warning("tello.rotate(): Invalid value.")
        return "error"

    def flip(self, direction: str):
        """Sends command to flip in direction specified"""
        self.logging.debug("Sending command: flip()")
        if direction in ("l", "r", "f", "b"):
            return self.run(f"flip {direction}",
                            f"Flipping {direction}, be careful \r\n")
        self.logging.warning("tello.flip(): Invalid value.")
        return "error"

    # SET Commands
    def set_speed(self, x: int):
        """Sends command to set speed to x cm/s"""
        self.logging.debug("Sending command: set_speed()")
        if 1 <= x <= 100:
            return self.run(f"speed {str(x)}",
                            f"Setting speed to {str(x)} cm/s \r\n")
        self.logging.warning("tello.set_speed(): Invalid value.")
        return "error"

    def set_wifi(self, ssid: str, passw: str):
        """Sends command to set wifi ssid and passw"""
        self.logging.debug("Sending command: set_wifi()")
        self.logging.info("SSID: %s, PASSWORD: %s", ssid, passw)
        self.logging.debug(
            "Please note that you will not be able to connect to the drone if you forget this password!"
        )
        return self.run(
            f"wifi {ssid}, {passw}",
            f"Setting wifi to {ssid}, with password {passw} then rebooting\r\n",
        )

    def set_mission_on(self):
        """Sends command to set mission pad detection on"""
        self.logging.debug("Sending command: set_mission_on()")
        return self.run("mon", "Enabling Mission Pad detection\r\n")

    def set_mission_off(self):
        """Sends command to set mission pad detection off"""
        self.logging.debug("Sending command: set_mission_off()")
        return self.run("moff", "Disabling Mission Pad detection\r\n")

    def set_mission_direction(self, x: int):
        """Sends command to set mission pad detection direction"""
        self.logging.debug("Sending command: set_mission_direction()")
        if 0 <= x <= 3:
            return self.run(
                f"mdirection {str(x)}",
                f"Setting Mission Pad Detection to setting {str(x)}\r\n",
            )
        self.logging.warning("tello.set_mission_direction(): Invalid value.")
        return "error"

    # GET Commands
    def get_speed(self):
        """Sends command to get speed"""
        self.logging.debug("Sending command: get_speed()")
        return self.run("speed?", "Obtaining current speed \r\n")

    def get_battery(self):
        """Sends command to get battery percentage"""
        self.logging.debug("Sending command: get_battery()")
        return self.run("battery?", "Obtaining battery level \r\n")

    def get_flight_time(self):
        """Sends command to get flight time"""
        self.logging.debug("Sending command: get_time()")
        return self.run("time?", "Obtaining current flight time \r\n")

    def get_wifi_snr(self):
        """Sends command to get wifi SNR"""
        self.logging.debug("Sending command: get_wifi_snr()")
        return self.run("wifi?", "Obtaining WiFi SNR \r\n")

    def get_sdk(self):
        """Sends command to get SDK version"""
        self.logging.debug("Sending command: get_sdk()")
        return self.run("sdk?", "Obtaining Tello SDK Version \r\n")

    def get_version(self):
        """Sends command to get Tello version"""
        self.logging.debug("Sending command: get_version()")
        return self.run("version?", "Obtaining Tello Version \r\n")

    def get_sn(self):
        """Sends command to get serial number"""
        self.logging.debug("Sending command: get_sn()")
        return self.run("sn?", "Obtaining Tello serial number \r\n")

    # SDK 3.0 GET Commands
    def get_hardware(self):
        """Sends command to get hardware (RMTT or Tello)"""
        self.logging.debug("Sending command: get_hardware()")
        return self.run("hardware?", "Obtaining  hardware status \r\n")

    def get_rmtt_wifi_version(self):
        """Sends command to get RMTT WiFi version"""
        self.logging.debug("Sending command: get_rmtt_wifi_version()")
        return self.run("wifiversion?", "Obtaining RMTT WiFi version \r\n")

    def get_ap(self):
        """Sends command to get RMTT AP info"""
        self.logging.debug("Sending command: get_ap()")
        return self.run("ap?",
                        "Obtaining RMTT Access Point SSID and password \r\n")

    def get_rmtt_wifi(self):
        """Sends command to get RMTT SSID"""
        self.logging.debug("Sending command: get_ssid()")
        return self.run("ssid?",
                        "Obtaining RMTT WiFi SSID and password (if any) \r\n")

    # COMPLEX Commands
    def go(self, x: int, y: int, z: int, s: int):
        """Sends command to move to x y z at speed s"""
        self.logging.debug("Sending command: go()")
        if 500 >= x >= -500 and 500 >= y >= -500 and 500 >= z >= -500:
            if 100 >= s >= 10:
                return self.run(
                    f"go {str(x)} {str(y)} {str(z)} {str(z)}",
                    f"Going to coordinates (x, y, z): {str(x)} {str(y)} {str(z)} at the speed of {str(s)} cm/s\r\n",
                )
            self.logging.warning("tello.go(): Invalid speed.")
            return "error"
        self.logging.warning("tello.go(): Invalid coordinates.")
        return "error"

    def curve(self, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int,
              s: int):
        """Sends command to curve from x1 y1 z1 at speed s to x2 y2 z2"""
        self.logging.debug("Sending command: curve()")
        if (500 >= x1 >= -500 and 500 >= x2 >= -500 and 500 >= y1 >= -500
                and 500 >= y2 >= -500 and 500 >= z1 >= -500
                and 500 >= z2 >= -500):
            if 60 >= s >= 10:
                return self.run(
                    f"curve {str(x1)} {str(y1)} {str(z1)} {str(x2)} {str(y2)} {str(z2)} {str(s)}",
                    f"Curving from (x, y, z): {str(x1)} {str(y1)} {str(z1)} to {str(x2)} {str(y2)} {str(z2)} at the speed of {str(s)} cm/s\r\n",
                )
            self.logging.warning("tello.curve(): Invalid speed.")
            return "error"
        self.logging.warning("tello.curve(): Invalid coordinates.")
        return "error"

    def go_mission_pad(self, x: int, y: int, z: int, s: int, mid: str):
        """Sends command to move to mission pad x y z at speed s and find Mpad mid"""
        self.logging.debug("Sending command: go_mission_pad()")
        mid_ok = False
        for current_mid in self.mids.split(" "):
            if current_mid == mid:
                mid_ok = True
                break
        if 500 >= x >= -500 and 500 >= y >= -500 and 500 >= z >= -500:
            if 100 >= s >= 10:
                if mid_ok:
                    return self.run(
                        f"go {str(x)} {str(y)} {str(z)} {str(s)} {str(mid)}",
                        f"Going to (x, y, z): {str(x)} {str(y)} {str(z)} at the speed of {str(s)} cm/s\r\n",
                    )
                self.logging.warning(
                    "tello.go_mission_pad(): Invalid mission pad ID.")
                return "error"
            self.logging.warning("tello.go_mission_pad(): Invalid speed.")
            return "error"
        self.logging.warning("tello.go_mission_pad(): Invalid coordinates.")
        return "error"

    def curve_mission_pad(self, x1: int, x2: int, y1: int, y2: int, z1: int,
                          z2: int, s: int, mid: str):
        """Sends command to curve from x y z 1 at speed s to x y z 2 and find Mpad mid"""
        self.logging.debug("Sending command: curve_mission_pad()")
        mid_ok = False
        for current_mid in self.mids.split(" "):
            if current_mid == mid:
                mid_ok = True
                break
        if (500 >= x1 >= -500 and 500 >= x2 >= -500 and 500 >= y1 >= -500
                and 500 >= y2 >= -500 and 500 >= z1 >= -500
                and 500 >= z2 >= -500):
            if 60 >= s >= 10:
                if mid_ok:
                    return self.run(
                        f"curve {str(x1)} {str(x2)} {str(z1)} {str(x2)} {str(y2)} {str(z2)} {str(s)} {str(mid)}",
                        f"Curving from (x, y, z): {x1} {y1} {z1} to {x2} {y2} {z2} at the speed of {str(s)} cm/s\r\n",
                    )
                self.logging.warning(
                    "tello.curve_mission_pad(): Invalid mission pad ID.")
                return "error"
            self.logging.warning("tello.curve_mission_pad(): Invalid speed.")
            return "error"
        self.logging.warning("tello.curve_mission_pad(): Invalid coordinates.")
        return "error"

    # SDK 3.0 DISPLAY Commands
    def set_light_off(self):  # TO TEST
        """Sends command to turn off the lights"""
        self.logging.debug("Sending command: set_light_off()")
        return self.run("EXT led 0 0 0", "Turning off the big light\r\n")

    def set_light_color(self, r: int, g: int, b: int):
        """Sends command to set the color of the LED"""
        self.logging.debug("Sending command: set_light_color()")
        if 255 >= r >= 0 and 255 >= g >= 0 and 255 >= b >= 0:
            return self.run(
                f"EXT led {str(r)} {str(g)} {str(b)}",
                f"Setting RMTT light color to (r, g, b): {str(r)}, {str(g)}, {str(b)}\r\n",
            )
        self.logging.warning("tello.set_light_color(): Invalid color.")
        return "led error"

    def set_light_pulse(self, r: int, g: int, b: int, p: float or int):
        """Sends command to set the color of the LED and pulse"""
        self.logging.debug("Sending command: set_light_pulse()")
        if 255 >= r >= 0 and 255 >= g >= 0 and 255 >= b >= 0 and 2.5 >= p >= 0.1:
            return self.run(
                f"EXT led br {str(p)} {str(r)} {str(g)} {str(b)}",
                f"Setting RMTT light color to (r, g, b):, {str(r)}, {str(g)}, {str(b)}, with pulse of, {str(p)} Hz\r\n",
            )
        self.logging.warning("tello.set_light_pulse(): Invalid values.")
        return "led error"

    def set_light_flash(self, r1: int, g1: int, b1: int, r2: int, g2: int,
                        b2: int, f: float or int):
        """Sends command to set the 2 colors of the LED to flash"""
        self.logging.debug("Sending command: set_light_flash()")
        if (255 >= r1 >= 0 and 255 >= g1 >= 0 and 255 >= b1 >= 0
                and 255 >= r2 >= 0 and 255 >= g2 >= 0 and 255 >= b2 >= 0
                and 10 >= f >= 0.1):
            return self.run(
                f"EXT led bl {str(f)} {str(r1)} {str(g1)} {str(b1)} {str(r2)} {str(g2)} {str(b2)}",
                f"Setting RMTT light color to (r, g, b): {str(r1)}, {str(g1)}, {str(b1)} and {str(r2)}, {str(g2)}, {str(b2)} with flash of {str(f)} Hz\r\n",
            )
        self.logging.warning("tello.set_light_flash(): Invalid values.")
        return "led error"

    def set_display_pattern(self, pattern: str = "0"):
        """Sends command to set the display pattern"""
        self.logging.debug("Sending command: set_display_pattern()")
        for char in pattern:
            if char not in "rbp0":
                self.logging.warning(
                    "tello.set_display_pattern(): Invalid pattern.")
                return "matrix error"
        return self.run(
            f"EXT mled g {str(pattern)}",
            f"Setting RMTT display pattern to: {str(pattern)} \r\n",
        )

    def set_display_blank(self):  # TO TEST
        """Sends command to make the display blank"""
        self.logging.debug("Sending command: set_display_off()")
        return self.run(
            "EXT mled g 0000000000000000000000000000000000000000000000000000000000000000",
            "Turning off the display\r\n",
        )

    def set_display_string(self, direction: str, color: str, frame_rate: float
                           or int, text: str):
        """Sends command to show a string on the display"""
        self.logging.debug("Sending command: set_display_string()")
        for char in direction:
            if char not in "lrud":
                self.logging.warning(
                    "tello.set_display_string(): Invalid direction.")
                return "matrix error"
        if color in ("r", "b", "p") and 10 >= frame_rate >= 0.1:
            return self.run(
                f"EXT mled {str(direction)} {str(color)} {str(frame_rate)} {str(text)}",
                f"Showing the string: {str(text)} with color: {str(color)}, frame rate (Hz): {str(frame_rate)} and in the diretion: {str(direction)} on the RMTT display \r\n",
            )
        self.logging.warning("tello.set_display_string(): Invalid values.")
        return "matrix error"

    def set_display_moving_image(self, direction: str,
                                 frame_rate: float or int, pattern: str):
        """Sends command to show a moving image on the display"""
        self.logging.debug("Sending command: set_display_moving_image()")
        for char in direction:
            if char not in "lrud":
                self.logging.warning(
                    "tello.set_display_moving_image(): Invalid direction.")
                return "matrix error"
        for char in pattern:
            if char not in "rbp0":
                self.logging.warning(
                    "tello.set_display_moving_image(): Invalid pattern.")
                return "matrix error"
        if 2.5 >= frame_rate >= 0.1:
            return self.run(
                f"EXT mled {str(direction)} g {str(frame_rate)} {str(pattern)}",
                f"Showing a moving image on the RMTT display in the direction: {str(direction)} with frame rate (Hz): {str(frame_rate)} and pattern: {str(pattern)} \r\n",
            )
        self.logging.warning("tello.set_display_moving_image(): Invalid values.")
        return "matrix error"

    def set_display_ascii_character(self, character: str, color: str):  # TEST
        """Sends command to display ascii character"""
        self.logging.debug("Sending command: set_display_ascii_character()")
        if (character == "heart"
                or character.encode("ascii") and color in ("r", "b", "p")):
            return self.run(
                # TEST
                f'EXT mled s {str(color)} {str(character.encode("ascii"))}',
                f"Displaying ASCII character: {str(character)} with color: {str(color)} \r\n",
            )
        self.logging.warning("tello.set_display_ascii_character(): Invalid values.")
        return "matrix error"

    def set_display_boot(self, pattern: str):
        """Sends command to set the display boot pattern"""
        self.logging.debug("Sending command: set_display_boot()")
        for char in pattern:
            if char not in "rbp0":
                self.logging.warning("tello.set_display_boot(): Invalid pattern.")
                return "error"
        return self.run(
            f"EXT mled sg {str(pattern)}",
            f"Setting RMTT boot display pattern to: {str(pattern)} \r\n",
        )

    def clear_display_boot(self):
        """Sends command to clear the display boot pattern"""
        self.logging.debug("Sending command: clear_display_boot()")
        return self.run("EXT mled sc",
                        "Clearing RMTT boot display pattern\r\n")

    def set_display_brightness(self, brightness: int):
        """Sends command to set the display brightness"""
        self.logging.debug("Sending command: set_display_brightness()")
        if 255 >= brightness >= 0:
            return self.run(
                f"EXT mled sl {str(brightness)}",
                f"Setting RMTT display brightness to: {str(brightness)} \r\n",
            )
        self.logging.warning("tello.set_display_brightness(): Invalid brightness.")
        return "matrix error"

    def get_tof(self):
        """Sends command to get the distance from the drone to the nearest obstacle in front"""
        self.logging.debug("Sending command: get_tof()")
        return self.run("EXT tof?",
                        "Getting ToF (read docs for more info)...\r\n")

    def get_esp32_version(self):
        """Sends command to get the ESP32 version"""
        self.logging.debug("Sending command: get_esp32_version()")
        return self.run("EXT version?", "Getting RMTT version...\r\n")

    # End command
    def end(self):
        """Closes the socket"""
        self.logging.debug("end(): Closing socket")
        self.sock.close()
        self.logging.debug("end(): Socket closed")
        return "ok"


