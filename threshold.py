import cv2
import numpy as np
import sys
def nothing(x):
    pass

def threshold_cvWindow(arg_img, arg_thrValue, arg_WindowPos):
    # Create a black image, a window
    #img = np.zeros((300,512,3), np.uint8)
    #img = cv2.imread("Debug/cover_1.jpg")
    
    img_gray = cv2.cvtColor(arg_img , cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('Threshold Setting')

    # create trackbars for color change
    cv2.createTrackbar('Threshold','Threshold Setting', arg_thrValue,255,nothing)
    ret, thresh = cv2.threshold(img_gray, 125, 255, 0)
    #print int(arg_WindowPos[1]-img_gray.shape[1]/2) 
    cv2.moveWindow('Threshold Setting', int(arg_WindowPos[0]-img_gray.shape[0]/2), int(arg_WindowPos[1]))
    while(1):
        cv2.imshow('Threshold Setting', thresh)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

        # get current positions of four trackbars
        threshold = cv2.getTrackbarPos('Threshold','Threshold Setting')
        ret, thresh = cv2.threshold(img_gray, threshold, 255, 0)
        try:
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            ctrs = filter(lambda x : cv2.contourArea(x) > 100 , contours)
            thresh = cv2.cvtColor(thresh , cv2.COLOR_GRAY2BGR)
            cv2.drawContours(thresh, ctrs, -1, (0,255,0), 1)
        except Exception as e:
            print e.args

    cv2.destroyAllWindows()
    return threshold

if __name__== '__main__':
    imgPath= sys.argv[1]
    image= cv2.imread(imgPath)

    thr= threshold_cvWindow(image, 122, (200,100))
    print 'Final threshold Value: ',thr
