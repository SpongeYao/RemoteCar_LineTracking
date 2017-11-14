import cv2
import numpy as np
import sys
import time
from class_CameraMntr import CameraLink 
from class_ArduinoSerMntr import* 
from check_LineDir import get_dir  

if __name__== "__main__":
    print 'MAIN...'
    y_cropped= 200
    camera= CameraLink(0,'webcam','Para/',[False, True, False])
    arduino= MonitorThread()
    arduino.start()
    if camera.connect:
        while(True):
            frame= camera.get_frame()
            img_cropped= frame[0:y_cropped,0:frame.shape[1]-1]
            angle, img_dir= get_dir(img_cropped)
            result= frame.copy()
            result[0:y_cropped,0:frame.shape[1]-1]= img_dir
            cv2.line(result, (0,y_cropped),(frame.shape[1]-1,y_cropped), (0,255,0),2) 
            #img_dir= img_cropped.copy()
            if angle is not False:
                step= int(angle/9)
                if angle>80 and angle<100:
                    cmd= 'W2'
                elif angle>100:
                    #cmd= 'A{0}'.format(int((angle-90)/9+1))
                    cmd= 'A{0}'.format(2)
                elif angle<80:
                    #cmd= 'D{0}'.format(int((90-angle)/9+1))
                    cmd= 'D{0}'.format(2)
                arduino.serial_send(cmd)
                arduino.serial_send('W1')
                #time.sleep(0.5)
                
                cv2.putText(result, 'cmd: {0}'.format(cmd),(30,90),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
            cv2.imshow('Live Image', result)


            k= cv2.waitKey(1) & 0xFF
            if k is ord('q'):
                arduino.serial_send('Q')
                break
            if k is ord('x'):
                arduino.serial_send('Q')
        #camera.release_cap()
        camera.exit_all()
        arduino.exit= True 
        cv2.destroyAllWindows() 

