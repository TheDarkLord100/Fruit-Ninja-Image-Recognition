import Properties
import time 
import Object
import cv2
import keyboard
from Slice import sliceFruits 

isAppRunning = True

def init():
    global isAppRunning
    print("Hello World!")
    Properties.loadProperties()
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    framerate = Properties.props['frameRate']
    resolution = (Properties.props['width'], Properties.props['height'])
    Properties.Video = cv2.VideoWriter("output.mp4", codec, framerate, resolution)
    time.sleep(2)

def play():
    global isAppRunning
    print("playing")
    while isAppRunning:
        if keyboard.is_pressed('q'):
            isAppRunning = False
            Properties.Video.release()
            break
        fruits, bomb = Object.locateObject()
        sliceFruits(fruits, bomb)

if __name__ == "__main__":
    init()
    print("Starting the game")
    play()

