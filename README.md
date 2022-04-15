# Python Tello
This is a library for easy usage of the Ryze Tello drone education edition.
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
To see `set` functions, please go [here]()
To see `complex` functions, please go [here]()
To see examples, please go [here]()

### tello.init()
Initializes SDK mode.
Must be run as the first function every time the script runs. <br />
Example:
```python
tello.init()
```
### tello.takeoff()
Automatic takeoff. <br />
Example:
```python
tello.takeoff()
```

### tello.land()
Automatic landing. <br />
Example:
```python
tello.land()
```

### tello.streamon()
Enable video stream. <br />
**Instructions under development! Use at own risk!** <br />
Example:
```python
tello.streamon()
```

### tello.streamoff()
Disable video stream. <br />
Example:
```python
tello.streamoff()
```

### tello.emergency()
Stops all motors immediately. <br />
**Danger of drone falling!** <br />
Parameters:
* reason: String, *optional*. Reason for stopping motors.<br />
Example:
```python
tello.emergency('Hit a wall')
```

### tello.stop()
Stops all movement and hovers in the air. <br />
Example:
```python
tello.stop()
```

### tello.up(x)
Ascends to *x* cm off the ground. <br />
Parameters:
* x: Integer. Height in cm. Allowed values: 20-500<br />
Example:
```python
tello.up(30)
```

### tello.down(x)
Descends to *x* cm off the ground. <br />
Parameters:
* x: Integer. Height in cm. Allowed values: 20-500<br />
Example:
```python
tello.down(100)
```

### tello.left(x)
Goes left for *x* cm. <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.left(249)
```

### tello.right(x)
Goes right for *x* cm. <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.right(23)
```

### tello.forward(x)
Goes forwards for *x* cm. <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.forward(500)
```

### tello.back(x)
Goes backwards for *x* cm. <br />
Parameters:
* x: Integer. Distance in cm. Allowed values: 20-500<br />
Example:
```python
tello.back(65)
```

### tello.cw(x)
Rotates clockwise for *x* degrees. <br />
Parameters:
* x: Integer. Degrees to turn.  Allowed values: 1-360<br />
Example:
```python
tello.cw(100)
```

### tello.ccw(x)
Rotates counter-clockwise for *x* degrees. <br />
Parameters:
* x: Integer. Degrees to turn.  Allowed values: 1-360<br />
Example:
```python
tello.ccw(359)
```

### tello.flip(x)
Flips drone in *x* direction. <br />
Parameters:
* x: String. Direction to flip.  Allowed values: `'f'` (forwards), `'b'` (backwards), `'l'` (left), `'r'` (right)<br />
Example:
```python
tello.flip('l')
```
