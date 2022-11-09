# Support for this has ended. This will no lonegr be updated.
# A new real-time Tello control script is coming soon
import socket
import subprocess
import sys
import threading
import time

host = ""
port = 9000
locaddr = (host, port)

# Print general info for the user
print("_________  ____                  ____ ")
print("    |      |      |      |      |    |")
print("    |      |___   |      |      |    |")
print("    |      |      |      |      |    |")
print("    |      |____  |____  |____  |____|\r\n")
print("             Drone Script             ")
print("         Live editing edition!        \r\n")
time.sleep(0.5)
print("            Initializing...           \r\n")
time.sleep(1)

print("          Checking network...         \r\n")
time.sleep(1)

try:
    process = subprocess.Popen(
        [
            "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
            "-I",
        ],
        stdout=subprocess.PIPE,
    )
    out, err = process.communicate()
    process.wait()
    wifi_val = {}
    for line in out.decode("utf-8").split("\n"):
        if "SSID: " in line:
            key, val = line.split(": ")
            val = val.strip()
            wifi_val = val
    if "TELLO-" not in wifi_val:
        print("Network detected:", wifi_val)
        print(
            "It seems like you have joined a different network. Please make sure that you have joined the TELLO-XXXXX Wi-Fi."
        )
        approval = input(
            "Are you sure you want to continue with the script? (y/n)")
        if approval == "y":
            print("\r\n")
        else:
            sys.exit()
    else:
        print("Network detected:", wifi_val)
        print("No errors. \r\n")
except subprocess.SubprocessError:
    print("\r\nSeems like there was an error checking the network.")
    print("Continuing.\r\n")

print("         Making UDP socket...         \r\n")
time.sleep(1)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ("192.168.10.1", 8889)

sock.bind(locaddr)


# Receiving Functionality
def recv():
    """Receive the response from Tello."""
    while True:
        try:
            data, _ = sock.recvfrom(1518)
            data = data.decode(encoding="utf-8")
            if data == "ok":
                print("Operation successful\r\n")
            elif "error" in data:
                print(data)
            else:
                print("Next time, try writing something valid!")
                print(data)
        except Exception:
            print("\nExiting...\n")
            break


print("\r\nTo view all available functions, type",
      "\033[1m" + "help" + "\033[0m")
print("\r\nTo quit the script, type", "\033[1m" + "end" + "\033[0m")
print(
    "\r\n(For emergencies) To immediately quit the script, press",
    "\033[1m" + "Ctrl + C" + "\033[0m",
)
print(
    "\r\nIMPORTANT! Do",
    "\033[1m" + "not" + "\033[0m",
    "type until a response is received!",
)
print("\r\nTo begin, type", "\033[1m" + "command" + "\033[0m: \r\n")

# recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

# Main loop: what happens repeatedly
while True:
    try:
        msg = input("")

        if not msg:
            break

        # Ending functionality (when typed 'end')
        if msg == "end":
            print("...")
            print("Make sure the drone has fully landed! \r\n")
            endmsg = input("Continue? (y/n)")
            if endmsg == "y":
                sock.close()
                break
            print("OK\r\n")
        # Help functionality (when typed 'help')
        elif msg == "help":
            print("\r\nSimple functions:")
            print("     command -- Initiate SDK mode (first command)")
            print("     takeoff -- Automatic takeoff")
            print("     land -- Automatic landing")
            print("     streamon -- Enable video stream")
            print("     streamoff -- Disable video stream")
            print("     emergency -- Stop motors immediately")
            print("     up/down x -- Ascend/descend to x cm (20-500)")
            print(
                "     left/right/forward/back x -- Fly forward/backward/left/right for x cm (20-500)"
            )
            print(
                "     cw/ccw x -- Rotate clockwise/counterclockwise x degrees (1-360)"
            )
            print(
                "     flip x -- Flip in the x direction (l (left), r (right), f (forw.), b (backw.))"
            )
            print("     stop -- Hover in the air")
            print(
                "\r\nTo view set, read and hard functions, type 'help set', 'help read' or 'help hard' \r\n\r\n"
            )
        elif msg == "help hard":
            print("\r\nHard functions:")
            print("     go x y z s -- Fly to x y z at speed s")
            print("                   x = left to right (500 to -500)")
            print("                   y = forwards, backwards (-500 to 500)")
            print("                   z = up, down (-500 to 500)")
            print("                   s = cm/s (10 to 100)")
            print(
                "     curve x1 y1 z1 x2 y2 z2 s -- Fly at a curve (make corner from coordinates) at s speed (arc radius must be between 0.5m and 10m)"
            )
            print("                   x1, x2 = left, right (-500 to 500)")
            print(
                "                   y1, y2 = forwards, backwards (-500 to 500)"
            )
            print("                   z1, z2 = up, down (-500 to 500)")
            print("                   s = cm/s (10 to 60)")
            print(
                "     go x y z s mid -- Fly to x y z at speed s of the mission pad"
            )
            print("                   x = left, right (-500 to 500)")
            print("                   y = forwards, backwards (-500 to 500)")
            print("                   z = up, down (-500 to 500)")
            print("                   s = cm/s (10 to 100)")
            print("                   mid1, mid2 = mission pad id (m1 to m8)")
            print(
                "     curve x1 y1 z1 x2 y2 z2 s mid -- Fly at a curve (make corner from coordinates) at s speed (arc radius must be between 0.5m and 10m) of the mission pad"
            )
            print("                   x1, x2 = left, right (-500 to 500)")
            print(
                "                   y1, y2 = forwards, backwards (-500 to 500)"
            )
            print("                   z1, z2 = up, down (-500 to 500)")
            print("                   s = cm/s (10 to 60)")
            print(
                "     jump x y z s yaw mid1 mid2 -- Fly to x, y, z of mid1 and recognize 0, 0, z of mid2 and rotate yaw"
            )
            print("                   x = left, right (-500 to 500)")
            print("                   y = forwards, backwards (-500 to 500)")
            print("                   z = up, down (-500 to 500)")
            print("                   s = cm/s (10 to 100)")
            print("                   mid1, mid2 = ?? (m1 to m8)")
            print(
                "\r\nTo view set, read and hard functions, type 'help set', 'help read' or 'help hard' \r\n\r\n"
            )
        elif msg == "help set":
            print("\r\nSet commands:")
            print("     speed x -- Set speed to x (10 to 100 cm/s)")
            print(
                "     wifi name pass -- Set Wi-Fi ssid to name and password to pass"
            )
            print("     mon -- Enable mission pad detection")
            print("     moff -- Disable mission pad detection")
            print(
                "     mdirection x -- Sets mission pad detection to x: either downward (0), forward (1), or both (2)"
            )
            print(
                "\r\nTo view set, read and hard functions, type 'help set', 'help read' or 'help hard' \r\n\r\n"
            )
        elif msg == "help read":
            print("\r\nRead commands:")
            print("     speed? -- Obtain current set speed (10 to 100 cm/s)")
            print("     battey? -- Obtain battery percentage (0 to 100)")
            print("     time? -- Obtain current flight time")
            print("     wifi? -- Obtain current Wi-Fi SNR")
            print("     sdk? -- Obtain current Tello SDK version")
            print("     sn? -- Obtain current Tello serial number")
            print(
                "\r\nTo view set, read and hard functions, type 'help set', 'help read' or 'help hard' \r\n\r\n"
            )
        else:
            # Send data
            msg = msg.encode(encoding="utf-8")
            sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print("\n . . .\n")
        sock.close()
        break
