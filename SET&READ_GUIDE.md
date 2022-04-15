# Python Tello
This is a library for easy usage of the Ryze Tello drone education edition.

## Requirements:
* Python installed on your system or as a VS Code extension
* Ryze Tello EDU Edition (get one [here](https://www.ryzerobotics.com/tello-edu))
* This package

To see the Quickstart guide, see the [README.md file](README.md)
## Set & Read Functions

### Set Functions

### tello.setSpeed(x)
Sets speed to *x* cm/s. <br />
Possible responses: ok / error <br />
Parameters:
* x: Integer. Speed in cm/s. Allowed values: 10-100 <br />
Example:
```python
tello.setSpeed(50) # Sets speed to 50 cm/s
```

### tello.setWifi(ssid, passw)
Sets WiFi SSID to *ssis* and password to *passw*. <br />
Possible responses: ok / error <br />
Parameters:
* ssid: String. New SSID for WiFi. Allowed values: any string <br />
* passw: String. New password for WiFi. Allowed values: any string <br />
Example:
```python
tello.setWifi('TELLO-XYZ', '1234567') # Sets WiFi SSID to TELLO-XYZ and password to 1234567
```

### tello.setMon()
Sets Mission Pad detection to on.<br />
Possible responses: ok / error <br />
Example:
```python
tello.setMon() # Turns M. Pad detection on
```

### tello.setMoff()
Sets Mission pad detection to off. <br />
Possible responses: ok / error <br />
Example:
```python
tello.setMoff() # Turns M. Pad detection off
```

### tello.setMdirection(x)
Sets Mission Pad detection direction(s). <br />
Possible responses: ok / error <br />
Parameters:
* x: Integer. 0 = downward detection, 1 = forward detection, 2 = downward and forward detection. Allowed values: 0-2 <br />
Example:
```python
tello.setMdirection(1) # Mission Pad detection direction: forward only.
```
