import telloFile
tello = telloFile.Tello()
# DO NOT WRITE ABOVE THIS LINE
tello.init()
tello.getBattery()
# tello.takeoff()
# tello.setMon()
# tello.setMdirection(1)
# tello.curve(10, 10, 50, 0, 20, 10, 30)
tello.land()