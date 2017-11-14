import threading
import json
import Queue
import random
import math
import yaml
import time
from copy import deepcopy 
import Tkinter
import tkMessageBox
import tkFont
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
import utils_tool
import imgProcess_tool
import class_MyThread

class CameraLink:
    def __init__(self, arg_camera_id, arg_camera_name='Cam', arg_readPath= 'Para/',arg_mapCoord_image_List= [False, False ,False]):
        self.__camera_idMatrix= [0, 1, 2, 3]
        self.camera_id= arg_camera_id
        self.__camera_name= arg_camera_name
        self.__newcameramtx, self.__roi, self.__mtx_1, self.__dist_1= False, False, False, False
        self.clean_buffer_judge= True
        self.connect= False
        self.connect_camera(self.camera_id)
        self.set_mapCoord_params(arg_mapCoord_image_List)
        self.readPath= arg_readPath 
        self.thread_clean_buffer= threading.Thread(target= self.clean_buffer) 
        self.thread_clean_buffer.start()

    def set_mapCoord_params(self, arg_params):
        self.__mapCoord_image_List= deepcopy(arg_params)
        self.__mapCoord_image_List[1]= not(self.__mapCoord_image_List[1])

    def connect_camera(self, arg_camera_id):
        if (self.connect):
            self.cap.release()
            print 'RELEASE...'
        self.camera_id= arg_camera_id
        print '>>> Cam ID ',self.camera_id
        self.cap= cv2.VideoCapture(self.camera_id)
        print 'cap.isOpened:', self.cap.isOpened()
        if not (self.cap.isOpened()):
            for tmp_id in self.__camera_idMatrix:
                try:
                    self.cap= cv2.VideoCapture(tmp_id)
                    print 'Cam ID ',tmp_id,': connected successfully!'
                    self.connect= True
                    self.camera_id= tmp_id
                    break
                except:
                    print 'Cam ID ',tmp_id,': connection Refused!'
                    self.connect= False
            if not(self.connect):
                tkMessageBox.showerror("Error","Connection of Camera refused!")
        else:
            self.connect= True
    
    def get_frame(self):
        if self.cap.isOpened():
            tmp_frame= self.cap.grab()
            _, tmp_frame= self.cap.retrieve()
            #print '@@@ ', self.__mapCoord_image_List
            tmp_frame= imgProcess_tool.mapCoord_image(tmp_frame, self.__mapCoord_image_List)
            return tmp_frame
        else:
            self.connect= False
            #print 'get_frame() Failed...'
            return -1

    def get_CalibratedFrame(self):
        if self.__mtx_1 is False:
            self.get_DistortionParams()
        frame= self.get_frame()
        dst = cv2.undistort(frame, self.__mtx_1, self.__dist_1, None, self.__newcameramtx)
	x,y,w,h = self.__roi
	dst = dst[y:y+h, x:x+w]
        #print 'get_frame.shape', frame.shape
        #print 'get_CalibratedFrame.shape', dst.shape
        return dst
        #pass
    
    def get_DistortionParams(self):
	with open(self.readPath+ self.__camera_name+ '_distortion.yaml') as f:
	    loadeddict = yaml.load(f)
	mtx = loadeddict.get('camera_matrix')
	dist = loadeddict.get('dist_coeff')
	self.__mtx_1 = np.array(mtx)
	self.__dist_1 = np.array(dist)

        frame= self.get_frame()
	h,  w = frame.shape[:2]
	self.__newcameramtx, self.__roi=cv2.getOptimalNewCameraMatrix(self.__mtx_1,self.__dist_1,(w,h),1,(w,h))
	

    def calibrate_length(self, arg_outputPath, arg_contourMinMaxArea, arg_contourCircularity):
        debugFolder= 'Debug/'
        utils_tool.check_path(arg_outputPath)

        #img= self.get_frame()
        '''
        img= self.get_CalibratedFrame()
        cv2.imwrite(debugFolder+self.__camera_name+'_rawImage.jpg', img)
        '''
        img= cv2.imread(debugFolder+self.__camera_name+'_rawImage.jpg')
        
        try: 
	    img_result= img.copy()
	    img_gray= cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
	    tmp= np.zeros(( img_gray.shape[0], img_gray.shape[1] , 1) , np.uint8)
	    gray = np.float32(img_gray)
	    #=====================================
	    # Binary Threshold
	    #=====================================
	    kernel_size= 5
	    blur= cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)
	    img_thr = cv2.adaptiveThreshold(blur.copy(), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	    ctrs ,hier = cv2.findContours(img_thr.copy(), cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)
	    print '* len(ctrs):',len(ctrs)
            for x in ctrs:
                c= (cv2.arcLength(x,True)*cv2.arcLength(x,True))
                if c== 0:
                    cir= 99999
                else:
                    cir=  4.0*np.pi*cv2.contourArea(x)/(cv2.arcLength(x,True)*cv2.arcLength(x,True))
                print 'Area, Cir',cv2.contourArea(x), cir
                #print 'Area, Cir',cv2.contourArea(x), 4.0*np.pi*cv2.contourArea(x)/(cv2.arcLength(x,True)*cv2.arcLength(x,True))
	    ctrs = filter(lambda x : arg_contourMinMaxArea[1]>cv2.contourArea(x) > arg_contourMinMaxArea[0] , ctrs)
	    ctrs = filter(lambda x : 1 > 4.0*np.pi*cv2.contourArea(x)/(cv2.arcLength(x,True)*cv2.arcLength(x,True)) > arg_contourCircularity , ctrs)
	    #'''
	    list_center=[]
	    corner_list = list()
	    print '*** len(ctrs):',len(ctrs)
            print arg_contourMinMaxArea, arg_contourCircularity
	    if len(ctrs)==4:
		for cntr in ctrs:
		    cv2.drawContours(img_result, [cntr], 0, (0, 0, 255), 1)
		    x,y,w,h = cv2.boundingRect(cntr)
		    list_center.append([x+w/2, y+h/2])
		    imgProcess_tool.mark_cross_line(img_result, int(x+w/2), int(y+h/2), (0,255,255), 2)           
		    cv2.putText(img_result,'('+str(int(x+w/2))+','+str(int(y+h/2))+')',(x+int(w/2),y+int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2) 
		list_angle=[]
		for i in range(0,2):
		    list_center= np.asarray(list_center)
		    center_sort= list_center[list_center[:,int(i)].argsort()]
		    corner_list.append(center_sort[0])
		    corner_list.append(center_sort[-1])
		    x_sublength= (center_sort[-1][0]- center_sort[0][0])
		    y_sublength= (center_sort[-1][1]- center_sort[0][1])
		    tmp_angle= 180-np.arctan2(y_sublength, x_sublength)*180/np.pi
		    print i,' Delta length X, Y: ',x_sublength, y_sublength
		    list_angle.append(tmp_angle)
		    print 'Angle:', tmp_angle
		    cv2.line(img_result, (center_sort[0][0], center_sort[0][1]) , (center_sort[-1][0], center_sort[-1][1]) , (0,0,255) , 1)
		
		if len(corner_list)==4:
		    #store_paras(corner_list)
                    outputfile= arg_outputPath+ self.__camera_name+"_calibration.json"
                    if utils_tool.check_file(outputfile):
		        with open(outputfile, 'r') as json_file:
			    data = json.load(json_file)
                    else:
                        data= dict()

		    print type(corner_list), corner_list
		    data["centroid_x"]  = np.sum(corner_list , axis = 0)[0] / 4
		    data["centroid_y"]  = np.sum(corner_list , axis = 0)[1] / 4
		    print 'line 24'
		    data["y_actual"] = 20.0 / abs(corner_list[0][0] - corner_list[1][0])
		    data["x_actual"] = 20.0 / abs(corner_list[2][1] - corner_list[3][1])
		    with open(outputfile , 'w') as json_file:
			json.dump(data , json_file)
		tmp_centroidX  = np.sum(corner_list , axis = 0)[0] / 4
		tmp_centroidY  = np.sum(corner_list , axis = 0)[1] / 4
		imgProcess_tool.mark_cross_line(img_result, tmp_centroidX, tmp_centroidY, (0,0,255),2)
	        #img_result= imgProcess_tool.mirror_image(img_result, 0)
                #cv2.putText(img_result, 'Angle : {0:.2f}, {1:.2f}'.format(list_angle[0], list_angle[1]),(20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,255),2)
                cv2.putText(img_result, 'Center : {0:.2f}, {1:.2f}'.format(tmp_centroidX, tmp_centroidY),(20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,255),2)
	    else:
		#cv2.putText(img_result,'More than 4 points Found',(20,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),1) 
                img_result= img_thr.copy()
	        #img_result= imgProcess_tool.mirror_image(img_result, 0)
    
        #'''
        except Exception as e:
            img_result= img.copy()
            print '[Center not Found] Error Message: ', e.message , e.args
            cv2.putText(img_result, 'Center Not found',(20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),1)

        return img_result

    def release_cap(self):
        self.connect= False
        self.cap.release()
        print 'Release Cap()'

    def clean_buffer(self):
        while self.clean_buffer_judge:
            try: 
                tmp_frame= self.cap.grab()
            except:
                self.connect= False

    def stop_clean_buffer(self):
        self.clean_buffer_judge= False

    def exit_all(self):
        self.stop_clean_buffer()
        self.release_cap()
    
    def subract_test(self):
        tmp_frame= self.cap.grab()
        _, tmp_frame= self.cap.retrieve()
        plastic_golden= cv2.imread('Data/Para/background.png')
        test= cv2.subtract(tmp_frame, plastic_golden)
        return test 
