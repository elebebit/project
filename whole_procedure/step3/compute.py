
import pickle
import numpy as np
from numpy import *

#导入相机参数

f=open('camera_para.p','rb')
para=pickle.load(f)

camera_m=para['camera_m']
R=para['R']
t=para['t']
s=para['s']


#导入图片参数

photo=open('../step2/recog/img_para.p','rb')
img=pickle.load(photo)

max_conf=max(img['conf'])
value_posi=img['conf'].index(max_conf)

item=img['label'][value_posi]
obj_pixel=img['pixel'][value_posi]

print(item)

#获取像素点坐标

print('pixel_coordinate:(%s, %s) (%s, %s)'%(obj_pixel[0],obj_pixel[1],obj_pixel[2],obj_pixel[3]))
x=np.mean([obj_pixel[0],obj_pixel[2]])
y=np.mean([obj_pixel[1],obj_pixel[3]])
ori_pixel=np.asmatrix([x,y]).T

pixel=np.vstack((ori_pixel,ones([1,1])))


#计算世界坐标

world=R.I*camera_m.I*s*pixel-R.I*t

print('world=(%s, %s)'%(float(world[0]),float(world[1])))

world_coor={}
world_coor['X']=float(world[0])
world_coor['Y']=float(world[1])
pickle.dump( world_coor, open( "world_coor.p", "wb" ) )







