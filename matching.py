import cv2  
from pylab import *  
img1=cv2.imread('Data/cropped_frame_0.jpg',0)  
img2=cv2.imread('Data/frame_0.jpg',0)  
m_h,n_l=img1.shape  
sift=cv2.SIFT()  
kp1,des1=sift.detectAndCompute(img1,None)  
kp2,des2=sift.detectAndCompute(img2,None)  
bf=cv2.BFMatcher()  
matches=bf.knnMatch(des1,des2,k=2)  
good=[]  
for m,n in matches:  
    if m.distance<0.75*n.distance:  
        good.append([m])  
def appendimages(I,I1):  
    rows=I.shape[0]  
    rows_1=I1.shape[0]  
    if rows<rows_1:  
        I=concatenate((I,zeros((rows_1-rows,I.shape(1)))),axis=0)  
    elif rows>rows_1:  
        I1=concatenate((I1,zeros((rows-rows_1,I1.shape(0)))),axis=0)  
    return concatenate((I,I1),axis=1)  
I_12=appendimages(img1,img2)  
c_coord1=[]  
c_coord2=[]  
c_coord1_1=[]  
c_coord2_1=[]  
#for i in range(len(good)):  
for i in range(40):  
    c_coord1.append(kp1[good[i][0].queryIdx].pt[0])  
    c_coord2.append(kp1[good[i][0].queryIdx].pt[1])  
    c_coord1_1.append(kp2[good[i][0].trainIdx].pt[0])  
    c_coord2_1.append(kp2[good[i][0].trainIdx].pt[1])  
c_coord1_1_1=[k+n_l for k in c_coord1_1]  
imshow(I_12,cmap='gray')  
plot(c_coord1,c_coord2,'r*')  
plot(c_coord1_1_1,c_coord2_1,'bo')  
X=[c_coord1[:],c_coord1_1_1[:]]  
Y=[c_coord2[:],c_coord2_1[:]]  
plot(X,Y)  
show()
