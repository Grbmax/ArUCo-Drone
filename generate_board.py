import cv2
from cv2 import aruco 
from pathlib import Path
from utils import ARUCO_DICT, aruco_display

root = Path(__file__).parent.absolute

aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_5X5_100 )

markerLength = 2
markerSeparation = 0.5
path = "checkboard/"
name = path + "board" + ".jpg"

board = aruco.GridBoard_create(7, 7, markerLength, markerSeparation, aruco_dict)
img = board.draw((1920,1080))
cv2.imwrite(name,img)
exit

