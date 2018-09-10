import numpy as np
from numpy import *
import cv2
import glob
import matplotlib.pyplot as plt

W=9
H=6
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((H*W,3), np.float32)
objp[:,:2] = np.mgrid[0:W, 0:H].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# Make a list of calibration images
images = glob.glob('*.jpg')

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (W,H), None)

    # If found, add object points, image points
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (W,H), corners, ret)
        #write_name = 'corners_found'+str(idx)+'.jpg'
        #cv2.imwrite(write_name, img)
        cv2.imshow('img', img)
        #print('objpoints= ',objpoints)
        #print('imgpoints= ',imgpoints)
        #cv2.waitKey(100)

#cv2.destroyAllWindows()


import pickle


# Test undistortion on an image
img = cv2.imread('1.jpg')
img_size = (img.shape[1], img.shape[0])

# Do camera calibration given object points and image points
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)


dst = cv2.undistort(img, mtx, dist, None, mtx)
#cv2.imwrite('test_undist.jpg',dst)

#print('rvecs= ',rvecs)

tvec=tvecs[0]

rmat, _ =cv2.Rodrigues(rvecs[0])

print('mtx= ',mtx)
# print('dist= ',dist)

#=====================求s平均和方差===============================
for wpoint,ppoint in zip(objpoints,imgpoints):

    #获取内参与外参R,t
    camera_m=np.asmatrix(mtx)
    R=np.asmatrix(rmat)
    t=np.asmatrix(tvec)

    #设置空矩阵存储各个点的s
    s_set=np.empty([1,W*H])
    #print(s_set)

    for line in range(W*H):

        #获取像素坐标与世界坐标
        world=np.asmatrix(wpoint[line,:]).T

        ori_pixel=np.asmatrix(ppoint[line]).T
        
        #转换得到[u v 1].T与[X Y 0].T
        world[2,:]=0
        w=world

        pixel=np.vstack((ori_pixel,ones([1,1])))

        #print(' ',pixel.T,'| ',w.T)

        #计算缩放参数s
        s=pixel.I*camera_m*(R*w+t)

        s_set[0,line]=s


#print('var=',s_set.var())
var=s_set.var()
if var >= 2:
    print('calibration fail')

else :
    print('calibration succeed')
    
#  参数写入文件
    camera_para={}
    camera_para["camera_m"] = camera_m
    camera_para["R"]=R
    camera_para["t"]=t
    camera_para["s"]=s_set.mean()
    pickle.dump( camera_para, open( "camera_para.p", "wb" ) )

#print('ave=',s_set.mean())

# world1=R.I*camera_m.I*s_set.mean()*pixel-R.I*t
# print('new world=',world1)
#===================================================================
