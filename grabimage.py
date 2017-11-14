import cv2
import numpy as np
import sys

cam_id= int(sys.argv[1])
cap = cv2.VideoCapture(cam_id)
i=0
while cap.isOpened():
    ret , frame = cap.read()
    #frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

    cv2.imshow("result" , frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("Data/frame_{0}.jpg".format(i) , frame)
        i= i+1

cap.release()
cv2.destroyAllWindows()
