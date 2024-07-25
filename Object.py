import math
import time
import numpy as np
import cv2

import Properties
from Screen import *
from operator import add, sub

img = None
imgSize = None
imgData = None

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def sampleColor(region):
    getPixelColor = lambda x, y : imgData[y, x]

    dimensonalSamplingPoints = 3
    left, top, right, bottom = region
    width, height = right - left, bottom - top
    xStep, yStep = math.ceil(width / dimensonalSamplingPoints), math.ceil(height / dimensonalSamplingPoints)

    color = [0, 0, 0]
    pointsCount = 0

    for y in range(top, bottom, yStep):
        for x in range(left, right, xStep):
            pixelColor = getPixelColor(x, y)
            color = list(map(add, color, pixelColor))
            pointsCount += 1

    return [ c / pointsCount for c in color ]


def locateObject():
    global img, imgSize, imgData
    objectColors = ( 
        # Watermelon & GA   Mango             Apple           Kiwi              Bananna & Lemon
        ( 56, 119, 30 ), ( 255, 215, 50 ), ( 160, 10, 0 ), ( 130, 100, 15 ), ( 225, 220, 30 ), 
        # Coconut & PA      Orange           Peach             Pink Fruit       Bomb
        ( 191, 126, 65 ), ( 230, 130, 0 ), ( 225, 100, 20 ), ( 210, 70, 60 ), ( 40, 30, 30 )
    )

    objectColorShifts = (-3, -3, 0, 3, 2, 2, 0, 0, 0, -5)

    img = capture_screen()
    imgSize = img.size
    imgData = np.array(img)
    imgDataClone = imgData.copy()
    imgData = cv2.cvtColor(imgData, cv2.COLOR_BGRA2RGB)

    samplingSize = Properties.props['samplingSize']
    maxColorDiff = Properties.props['maxColorDiff']
    minObjectDistance = 150

    ConstraintX = lambda X : min(max(X, 0), imgSize[0])
    ConstraintY = lambda Y : min(max(Y, 0), imgSize[1])

    left, top, right, bottom = 0, 100, imgSize[0], imgSize[1]
    height, width = bottom - top, right - left
    xStep, yStep = math.ceil(width / Properties.props['xSampling']), math.ceil(height / Properties.props['ySampling'])

    fruits = []
    bombs = []

    for y in range(top, bottom, yStep):
        for x in range(left, right, xStep):
            sampleRegion = [
                ConstraintX(x - samplingSize // 2), ConstraintY(y - samplingSize // 2),
                ConstraintX(x + samplingSize // 2), ConstraintY(y + samplingSize // 2)
            ]

            regionColor = sampleColor(sampleRegion)

            for i, color in enumerate(objectColors):
                isFruit = i < len(objectColors) - 1
                
                colorDiff = list(map(sub, regionColor, color))
                absColorDiff = [ abs(c) for c in colorDiff ]
                objectColor = sum(absColorDiff)
                objectColor += objectColorShifts[i]

                if(objectColor <= maxColorDiff):
                    toAppend = True
                    checkObjects = fruits if isFruit else bombs

                    for object in checkObjects:
                        if(object[3] == color):
                            distance = getDistance(*object[:2], x, y)
                            
                            if(distance < minObjectDistance):
                                if(object[4] < objectColor):
                                    checkObjects.remove(object)
                                else:
                                    toAppend = False
                                break
                    
                    if(toAppend):
                        checkObjects.append(( x, y, regionColor, color, objectColor ))
                    break
                                            
            sampleBoxSize = 2
            if Properties.props['showSamplePoints'] : 
                cv2.rectangle(imgDataClone, pt1=(x, y), pt2=(x + sampleBoxSize, y + sampleBoxSize), color=(255, 255, 255), thickness=-1)
    
    fruits = sorted(fruits, key=lambda object : object[4] + abs(object[1] - Properties.props['height'] * 0.5) * 0.02)

    discardedCoordsClone = Properties.DiscardedPoints.copy()
    currentTime = time.time()

    for coords, ptime in discardedCoordsClone.items():
        if ptime <= currentTime:
            del Properties.DiscardedPoints[coords]

    for bomb in bombs:
        Properties.DiscardedPoints[bomb[:2]] = time.time() + 1.5

    fruitsClone = fruits.copy()
    maxDistanceToDiscard = 150

    for fruit in fruitsClone:
        for discardedCoords in Properties.DiscardedPoints.keys():
            fruitDiscardDistance = getDistance(*fruit[:2], *discardedCoords[:2])

            if fruitDiscardDistance < maxDistanceToDiscard:
                fruits.remove(fruit)
                break
    
    # Display the detected objects
    for i, object in enumerate(fruits + bombs):
        isFruit = i < len(fruits)
        boxCorner = (object[0] - 100, object[1] - 100)
        accuracy = max(math.sqrt((maxColorDiff - object[4]) / maxColorDiff) * 100.0, 1.0)

        cv2.rectangle(imgDataClone, pt1=boxCorner, pt2=(int(boxCorner[0] + 200), int(boxCorner[1] + 200)), color=(255, 255, 255), thickness=2)
        cv2.putText(imgDataClone, f"{ 'Fruit' if isFruit else 'Bomb' } - { accuracy:.2f}%", (boxCorner[0], boxCorner[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        sampleBoxCorner = (
            int(boxCorner[0] + 167),
            int(boxCorner[1] - 43)
        )

        sampleBoxSize = 40
        color = object[2][::-1]

        cv2.rectangle(imgDataClone, pt1=sampleBoxCorner, pt2=(sampleBoxCorner[0] + sampleBoxSize, sampleBoxCorner[1] + sampleBoxSize), color=color, thickness=-1)           

    
    imgDataClone = cv2.cvtColor(imgDataClone, cv2.COLOR_BGRA2BGR)
    Properties.Video.write(imgDataClone.astype("uint8"))

    return fruits, bombs