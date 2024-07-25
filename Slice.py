import time
import pyautogui
from Object import *

def slice(x1, y1, x2, y2):
    x1, y1 = getScreenCoords(x1, y1)
    x2, y2 = getScreenCoords(x2, y2)

    pyautogui.moveTo(x1, y1, _pause=False)
    pyautogui.mouseDown( _pause=False)
    pyautogui.sleep(0.01)
    pyautogui.moveTo(x2, y2, 0.04, _pause=False)
    pyautogui.sleep(0.03)
    pyautogui.mouseUp(_pause=False)
    pyautogui.sleep(0.01)

def sliceFruits(fruits, bombs):
    if len(fruits) > 0:

        minFruitBombDistance = 400
        fruitIndex = 0

        while True:
            selectedFruit = fruits[fruitIndex]
            isFruitSafe = True

            for bomb in bombs:
                bombDistance = getDistance(*bomb[:2], *selectedFruit[:2])

                if bombDistance < minFruitBombDistance:
                    fruitIndex += 1
                    if fruitIndex >= len(fruits):
                        return
                    isFruitSafe = False
                    break

            if isFruitSafe:
                break
        
        sliceLength = 200
        sliceStart = (selectedFruit[0], selectedFruit[1] + sliceLength * 0.5)
        sliceEnd = (selectedFruit[0], selectedFruit[1] - sliceLength * 0.5) 
        
        slicingCoords  =(*sliceStart, *sliceEnd)
        slice(*slicingCoords)
        points = pointify(*slicingCoords)

        if selectedFruit[3] != (210, 70, 60):
            for point in points:
                Properties.DiscardedPoints[point] = time.time() + 1.0
        else:
            slice(*slicingCoords)

