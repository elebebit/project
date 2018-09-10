import numpy as np
import cv2
import glob
import pickle

#获取像素点坐标

photo=open('../step2/recog/img_para.p','rb')
img=pickle.load(photo)

max_conf=max(img['conf'])
value_posi=img['conf'].index(max_conf)

item=img['label'][value_posi]
obj_pixel=img['pixel'][value_posi]

print(item)
print('pixel_coordinate:(%s, %s) (%s, %s)'%(obj_pixel[0],obj_pixel[1],obj_pixel[2],obj_pixel[3]))
x=np.mean([obj_pixel[0],obj_pixel[2]])
y=np.mean([obj_pixel[1],obj_pixel[3]])

# def rgb2gray(rgb):
# 	return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
 
# img_gray=rgb2gray(img)

#计算深度

depth_img=cv2.imread('1d.bmp',-1)
depth=depth_img[int(round(y))][int(round(x))][1]
print(depth*256)

