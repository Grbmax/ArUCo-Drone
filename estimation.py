import yaml
import cv2
import numpy as np
from utils import ARUCO_DICT, aruco_display

def pose_estimate(frame, aruco_dict_type, mtx_coeff, distort_coeff):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)

    if len(corners) > 0:
        for i in range(0, len(ids)):
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, mtx_coeff, distort_coeff)

            cv2.aruco.drawDetectedMarkers(frame, corners)
            distance = np.sqrt((tvec[0][0][2] ** 2 + tvec[0][0][0] ** 2 + tvec[0][0][1] ** 2))*1000
            aruco_display(corners, ids, rejected_img_points, frame, distance)
            cv2.drawFrameAxes(frame, mtx_coeff, distort_coeff, rvec, tvec, 0.03)
    
    return frame

aruco_type = "DICT_5X5_100"
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])
arucoParams = cv2.aruco.DetectorParameters_create()
with open('calibration.yaml') as f:
    l = yaml.safe_load(f)
    mtx = l.get('camera_matrix')
    dist = l.get('dist_coeff')
    mtx = np.array(mtx)
    dist = np.array(dist)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    ret, img = cap.read()
    output = pose_estimate(img, ARUCO_DICT[aruco_type],mtx,dist)
    cv2.imshow('Estimated Pose', output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release
cv2.destroyAllWindows()




