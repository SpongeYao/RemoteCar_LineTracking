import cv2 
import numpy as np
import imgProcess_tool
import utils_tool

def get_dir(arg_img):
    img= arg_img.copy()
    if len(img.shape)==3:
        img_gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_thr= imgProcess_tool.binarialization(img, 1, 60, False)
    
    #==== Apply Canny edge detection =====
    img_canny = cv2.Canny(img_thr,50,100,apertureSize = 3)
    ctrs_edge, _= imgProcess_tool.findContours(img_canny,img, False, False)
    ctrs_all, _= imgProcess_tool.findContours(img_thr,img, False, False)
    result= arg_img.copy()
    #print 'len(ctrs_edge)= ',len(ctrs_edge)
    #print 'len(ctrs_all)= ',len(ctrs_all)
    if len(ctrs_edge)==2 and len(ctrs_all)==1:
        _, angle1, _, _= imgProcess_tool.pca_contour(ctrs_edge[0])
        _, angle2, _, _= imgProcess_tool.pca_contour(ctrs_edge[1])
        center= (int(img.shape[1]/2), int(img.shape[0]-30))
        if angle1 is not False and angle2 is not False:
            if angle1>180:
                angle1= angle1-180
            if angle2>180:
                angle2= angle2-180

            angle_dir= (angle1+angle2 )/2.0
            
            endpt= (int(center[0]+np.cos(angle_dir*np.pi/180)*100), int(center[1]-np.sin(angle_dir*np.pi/180)*100))
            #===========================
            # Drawing the result in image
            #===========================
            result= imgProcess_tool.mark_cross_line(result,center[0],center[1], (0,0,255),2)
            cv2.arrowedLine(result, center, endpt, (0,0,255), 5, 8, 0, 0.2)
            cv2.putText(result, 'Angle: {0:.3f}'.format(angle_dir),(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        else:
            angle_dir=False
            cv2.putText(result, 'No Rout is found',(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))

    else: 
        angle_dir=False
        cv2.putText(result, 'No Rout is found',(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))

    #print angle_dir, type(result)
    return angle_dir, result

if __name__=='__main__':
    folder= 'Data/'
    debug_folder= 'Debug/'
    list_name= utils_tool.getList_path(folder)

    for filename in list_name:
        print '=== ', folder+filename+' ==='
        img= cv2.imread(folder+filename)
        img_gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img_cropped= img[227:img.shape[1]-1,0:img.shape[0]-1]
        img_cropped= img[0:200,0:img.shape[1]-1]
        cv2.imwrite(debug_folder+'debug_'+ filename.split('.')[0]+ '_cropped.jpg',img_cropped)
        #img_thr= imgProcess_tool.binarialization(img_cropped, 0, 60)
        img_thr= imgProcess_tool.binarialization(img_cropped, 1, 60, False)
        # Apply Canny edge detection, return will be a binary image
        img_canny = cv2.Canny(img_thr,50,100,apertureSize = 3)
        ctrs_edge, _= imgProcess_tool.findContours(img_canny,img_cropped, False, False)
        ctrs_all, _= imgProcess_tool.findContours(img_thr,img_cropped, False, False)
        result= img.copy()
        print 'len(ctrs)= ',len(ctrs_edge)
        if len(ctrs_edge)==2 and len(ctrs_all)==1:
            _, angle1, _, _= imgProcess_tool.pca_contour(ctrs_edge[0])
            _, angle2, _, _= imgProcess_tool.pca_contour(ctrs_edge[1])
            #center, _, _, _= imgProcess_tool.pca_contour(ctrs_all[0])
            center= (int(img.shape[1]/2), int(img.shape[0]/2))
            if angle1>180:
                angle1= angle1-180
            if angle2>180:
                angle2= angle2-180

            angle_dir= (angle1+angle2 )/2.0
            
            endpt= (int(center[0]+np.cos(angle_dir*np.pi/180)*100), int(center[1]-np.sin(angle_dir*np.pi/180)*100))
            #img_cropped= imgProcess_tool.mark_cross_line(img_cropped,center[0],center[1], (0,0,255),2)
            #cv2.arrowedLine(img_cropped, center, endpt, (0,0,255), 5, 8, 0, 0.2)
            result= imgProcess_tool.mark_cross_line(result,center[0],center[1], (0,0,255),2)
            cv2.arrowedLine(result, center, endpt, (0,0,255), 5, 8, 0, 0.2)
            cv2.putText(result, 'Angle: {0:.3f}'.format(angle_dir),(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
            '''
            for ctr in ctrs:
                center, angle, endpt1, endpt2= imgProcess_tool.pca_contour(ctr)
                angle_list 
                #cv2.line(result,center,endpt1,(0,255,255),2)
            '''
        '''
        #cv2.line(result,endpt2,endpt1,(0,255,255),2)
        #cv2.line(result,(100,0),(100,200),(0,0,0),2)
        cv2.line(result,center,pt_ref,(0,255,255),2)
        cv2.putText(result, 'Angle2: {0:.3f}'.format(angle2),(30,60),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        cv2.putText(result, 'Average: {0:.3f}'.format(angle_ref),(30,90),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        print angle_ref, ' average COS, SIN', np.cos(angle_ref*np.pi/180), np.sin(angle_ref*np.pi/180)
        '''
        #cv2.imwrite(debug_folder+'debug_'+ filename.split('.')[0]+ '_croppedContour.jpg',result)
        cv2.imwrite(debug_folder+'debug_'+ filename.split('.')[0]+ '_cropped.jpg',img_cropped)
        cv2.imwrite(debug_folder+'debug_'+ filename.split('.')[0]+ '_result.jpg',result)
        #img_thr=cv2.resize(img_thr,(224,224),interpolation=cv2.INTER_CUBIC)
        '''
        # Apply Hough Line Transform, minimum lenght of line is 200 pixels
        lines = cv2.HoughLines(img_canny,1,np.pi/180,100)
        print lines
        if lines is not None:
            # Print and draw line on the original image
            for rho,theta in lines[0]:
                #print(rho, theta)
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        '''


