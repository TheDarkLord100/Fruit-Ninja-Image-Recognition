import mss
import mss.tools

import Properties

def getScreenCoords(x, y):
    x_game = x + Properties.props['left']
    y_game = y + Properties.props['top']
    return x_game, y_game

def pointify(x1, y1, x2, y2, ):
    pointCount = 10
    points = []
    for pointIndex in range(pointCount):
        ratio = pointIndex / pointCount
        points.append(( x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio))
    return points

def capture_screen():
    with mss.mss() as sct:
        monitor = {"top": Properties.props['top'], "left": Properties.props['left'], "width": Properties.props['width'], "height": Properties.props['height']}
        ss = sct.grab(monitor)
        # mss.tools.to_png(ss.rgb, ss.size, output="screen.png")
        return ss
    
