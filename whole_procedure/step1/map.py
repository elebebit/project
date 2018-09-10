import numpy as np
from PIL import Image
import shutil

mapping_matrix_name = 'trans.txt'
color_image_name = 'color.bmp'
mapping_matrix = open(mapping_matrix_name, 'r').readlines()
color_image = np.array(Image.open(color_image_name))

mapped_color_image = np.zeros((424, 512, 3), dtype = 'uint8')
for i in range(424):
	for j in range(512):
		matrix_indices = i*512 + j
		color_x = mapping_matrix[matrix_indices].split()[0]
		color_y = mapping_matrix[matrix_indices].split()[1]
		if not (color_x == '-1.#INF' or color_y == '-1.#INF'):
			color_x = int(round(float(color_x)))
			color_y = int(round(float(color_y)))
			if color_x>=0 and color_x<1920 and color_y>=0 and color_y<1080:
				mapped_color_image[i][j][0] = int(color_image[color_y][color_x][0])
				mapped_color_image[i][j][1] = int(color_image[color_y][color_x][1])
				mapped_color_image[i][j][2] = int(color_image[color_y][color_x][2])

img = Image.fromarray(mapped_color_image)
img.save('color_trans.png')
