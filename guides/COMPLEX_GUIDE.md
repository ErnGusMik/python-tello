# Python Tello
This is a library for easy usage of the Ryze Tello drone education edition.
## Requirements:
* Python installed on your system or as a VS Code extension
* Ryze Tello EDU Edition (get one [here](https://www.ryzerobotics.com/tello-edu))
* This package

To see the Quickstart guide, see the [README.md file](README.md)
#### Be Cautious when using these functions. They can become confusing very quickly!

## COMPLEX Functions

### tello.go(x, y, z, s)
Goes to *x y z* location at speeed *s*. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Distance to go left-right in cm. Allowed values: -500-500
* y: Integer. Distance to go forwards-backwards in cm. Allowed values: -500-500
* z: Integer. Distance to go up-down in cm. Allowed values: -500-500
* s: Integer. Speed. Allowed values: 10-100
Example:
```python
tello.go(10, 50, 10, 50) # Goes 10 cm right, 50 cm forwards, 10 cm up at the speed of 50 cm/s
```

### tello.goMpad(x, y, z, s, mid)
Goes to *x y z* location at speeed *s*. <br />
Possible responses: `ok` / `error` <br />
Parameters:
* x: Integer. Distance to go left-right in cm. Allowed values: -500-500
* y: Integer. Distance to go forwards-backwards in cm. Allowed values: -500-500
* z: Integer. Distance to go up-down in cm. Allowed values: -500-500
* s: Integer. Speed. Allowed values: 10-100
* mid: String. Mission Pad ID. Allowed values: `'m1'`, `'m2'`, `'m3'`, `'m4'`, `'m5'`, `'m6'`, `'m7'`, `'m8'`
Example:
```python
tello.go(100, 40, 5, 50, m1) # Goes 100 cm right, 40 cm forwards, 50 cm up from Mission Pad 1 at the speed of 50 cm/s
```

### tello.curve(x1, x2, y1, y2, z1, z2, s)
Curve to the *x2 y2 z2* location, curving through the *x1 y1 z1* location at speeed *s*..<br />
**Not always works. Use at own risk!**<br />
Possible responses: `ok` / `error` <br />
Parameters:
* x1: Integer. Distance to go left-right in cm. Allowed values: -500-500
* x2: Integer. Distance to go left-right in cm. Allowed values: -500-500
* y1: Integer. Distance to go forwards-backwards in cm. Allowed values: -500-500
* y2: Integer. Distance to go forwards-backwards in cm. Allowed values: -500-500
* z1: Integer. Distance to go up-down in cm. Allowed values: -500-500
* z2: Integer. Distance to go up-down in cm. Allowed values: -500-500
Example:
```python
tello.curveMpad(20, 35, 47, 25, 9, 200, 40) # Curves to x=35 y=25 z=200 through x=20 y=47 z=9 at speed 40 cm/s
```

### tello.curveMpad(x1, x2, y1, y2, z1, z2, s, mid)
Curve to the *x2 y2 z2* location, curving through the *x1 y1 z1* location at speeed *s* from the *mid* coordinates.<br />
**Not always works. Use at own risk!**<br />
Possible responses: `ok` / `error` <br />
Parameters:
* x1: Integer. Distance to go left-right in cm. Allowed values: -500-500
* x2: Integer. Distance to go left-right in cm. Allowed values: -500-500
* y1: Integer. Distance to go forwards-backwards in cm. Allowed values: -500-500
* y2: Integer. Distance to go forwards-backwards in cm. Allowed values: -500-500
* z1: Integer. Distance to go up-down in cm. Allowed values: -500-500
* z2: Integer. Distance to go up-down in cm. Allowed values: -500-500
* s: Integer. Speed. Allowed values: 10-60
* mid: String. Mission Pad ID. Allowed values: `'m1'`, `'m2'`, `'m3'`, `'m4'`, `'m5'`, `'m6'`, `'m7'`, `'m8'`
Example:
```python
tello.curveMpad(100, 30, 40, 55, 5, 50, 30, m1) # Curves to x=30 y=55 z=50 through x=100 y=40 z=5 from Mission Pad m1 at speed 30 cm/s
```
