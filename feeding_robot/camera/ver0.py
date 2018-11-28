import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm

try:
	pipeline=rs.pipeline()

	while True:
		frames=pipeline.wait_for_frams()
		depth=frames.get_depth_fram()
		depth_data=depth.as_frame().get_data()
		np_image=np.asanyarray(depth_data)
		break
except Exception as e:
	print('fail')

print (np_image.shape())
plt.imshow(np_image,cmap=cm.hot,norm=LogNorm())
plt.colorbar()
plt.show()
