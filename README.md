# Python Tello
This is a library for easy usage of the Ryze Tello drone education edition. <br />
**Current Version:**
*2.0.4 Alpha* <br />
SDK 3.0 is **here**! Documentation and testing in progress!
## Requirements:
* Python installed on your system or as a VS Code extension
* Ryze Tello EDU Edition (get one [here](https://www.ryzerobotics.com/tello-edu))
* This package

## Quickstart
This quickstart focuses on the file edition.
To get instructions for the live edition, go to [Tello Live Edition Guide]()
```python
import telloFile # Imports library
tello = telloFile.Tello() # Sets var tello as the class
tello.connect() # Initializes SDK mode (more below)
```
*(WRITEHERE.py)*

## Usage
The library consists of callable functions.
To see `set` functions, please go [here](SET%26READ_GUIDE.md)
To see `complex` functions, please go [here](COMPLEX_GUIDE.md)
To see examples, please go [here]()

### tello.connect()
Initializes SDK mode.
Must be run as the first function every time the script runs. <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.connect()
```
### tello.takeoff()
Automatic takeoff. <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.takeoff()
```

### tello.land()
Automatic landing. <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.land()
```

### tello.video_stream_on()
Enable video stream. <br />
**Camera functionality under development** <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.streamon()
```

### tello.video_stream_off()
Disable video stream. <br />
**Camera functionality under development** <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.streamoff()
```

### tello.emergency()
Stops all motors immediately. <br />
**Danger of drone falling!** <br />
Possible responses: `ok` / `error` <br />
Parameters:
* reason: String, *optional*. Reason for stopping motors.<br />
Example:
```python
tello.emergency('The drone has hit a wall')
```

### tello.stop()
Stops all movement and hovers in the air. <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.stop()
```

### tello.up(x)
Ascends to *x* cm off the ground. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Height in cm. Allowed values: 20-500<br />
Example:
```python
tello.up(30)
```

### tello.down(x)
Descends to *x* cm off the ground. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Height in cm. Allowed values: 20-500<br />
Example:
```python
tello.down(100)
```

### tello.left(x)
Goes left for *x* cm. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.left(249)
```

### tello.right(x)
Goes right for *x* cm. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.right(23)
```

### tello.forward(x)
Goes forwards for *x* cm. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.forward(500)
```

### tello.back(x)
Goes backwards for *x* cm. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.back(65)
```

### tello.cw(x)
Rotates clockwise for *x* degrees. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Degrees to turn.  Allowed values: 1-360<br />
Example:
```python
tello.cw(100)
```

### tello.ccw(x)
Rotates counter-clockwise for *x* degrees. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Degrees to turn.  Allowed values: 1-360<br />
Example:
```python
tello.ccw(359)
```

### tello.flip(x)
Flips drone in *x* direction. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: String. Direction to flip.  Allowed values: `'f'` (forwards), `'b'` (backwards), `'l'` (left), `'r'` (right)<br />
Example:
```python
tello.flip('l')
```

### tello.throw_fly()
Toss the drone in the air within 5 seconds of receiving response to takeoff <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.throw_fly()
```

### tello.motor_on()
Turns on motors (at a slow RPM)<br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.motor_on()
```

### tello.motor_off()
Turns off motors (use motor_on() first)<br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.motor_off()
```

### tello.throw_fly()
Turns off motors (use tello.motoron() first)<br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.motoroff()
```

### tello.end()
Ends the program. <br />
Possible responses: `ok` / Thrown `error` <br />
Example:
```python
tello.end()
```

## Version history:
**2.0.4-alpha**
* Readded .deepsource.toml
* Hopefully fixed pip 'No Description provided' issue

**2.0.3-alpha**
* Reorganized structure for PyPi
* Added LICENSE.txt (MIT License)
* Added setup.cfg
* Added setup.py and configured for PyPi
* Added tello-sdk/__init__.py
* We're pip installable now!

**2.0.2-alpha**
* Style fixes
* Started work on going pip-ready :)
* Changed all print to logging (for easier debugging)
* Added debugging and tips options to Tello class

**2.0.1-alpha**
* Small fixes

**2.0-alpha**
* All new Tello SDK 3.0 commands implemented!
* Small potential bug/style fixes
* This is an Alpha version, so it is **not** stable, by any means!


**1.1.2-alpha**
* Potential bug fixes
* Security issue fix
* Performance optimizations
* Remodel of __init__ function


**1.1-beta:**
* Implementation of some Tello SDK 3.0 commands
* Naming changes
* Functions now return the response
* In development: camera functions, customization, SDK 3.0 full implementation
* V1.1.1: spelling fix


**1.0-beta:**
* Implement most of Tello SDK 2.0 commands
* Documentation started
* `tello.run()` command for executing any command straight to the drone.
