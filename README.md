# Python Tello
This is a library for easy usage of the Ryze Tello drone education edition. <br />
**Current Version:**
*1.0 Beta* <br />
SDK 3.0 Implementation under development!
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
tello.init() # Initializes SDK mode (more below)
```
*(WRITEHERE.py)*

## Usage
The library consists of callable functions.
To see `set` functions, please go [here](SET%26READ_GUIDE.md)
To see `complex` functions, please go [here](COMPLEX_GUIDE.md)
To see examples, please go [here]()

### tello.init()
Initializes SDK mode.
Must be run as the first function every time the script runs. <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.init()
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

### tello.streamon()
Enable video stream. <br />
**Instructions under development! Use at own risk!** <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.streamon()
```

### tello.streamoff()
Disable video stream. <br />
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
tello.emergency('Hit a wall')
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

### tello.throwFly()
Toss the drone in the air within 5 seconds of receiving response to takeoff <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.throwFly()
```

### tello.motoron()
Turns on motors (at a slow RPM)<br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.motoron()
```

### tello.throwFly()
Turns off motors (use tello.motoron() first)<br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.motoroff()
```

### tello.end()
Ends the program. <br />
Possible responses: `ok` / `error` <br />
Example:
```python
tello.end()
```

## Version history:
**1.0 Beta:**
* Implement most of Tello SDK 2.0 commands
* Documentation started
* `tello.run()` command for executing any command straight to the drone.
