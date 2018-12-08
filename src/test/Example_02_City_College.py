# -*- coding: utf-8 -*-
"""Example_01_Living_Room.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/PooneetThaper/Depth-from-Disparity/blob/master/src/test/Example_02_City_College.ipynb

## Initial exploration

### Overview
Images were taken of my living room each aligned with the edge of a table and offset by a baseline of 25cm.

### Materials
- A small tripod and a phone camera mount adapter were used to provide stability
- A tape measure was used to measure 25 centimeter intervals from the left edge of the table
- A phone (Oneplus 6) was used to capture the photos with default settings

### Procedure
- Five intervals were measured (0cm, 25cm, 50cm, 75cm, 100cm from the left edge of the table)
- The left edge of the tripod was aligned with each of these intervals
- The front edge was aligned with the front edge of the table for each photo
- Images were mistankenly taken with autofocus which could have caused different focal lengths for each

### Discussion
- The focus (found afterwards by looking at the metadata of the photos) was found to be 4.25mm on all images
- Disparity equation can be used to find the depth of each area of the image:
$$ Z = D = f \frac{B}{d} $$
where:
$$ D = \textrm{depth} $$
$$ f = \textrm {focal length} $$
$$ B = \textrm{baseline} $$
$$ d = \textrm{disparity} = x_r - x_l $$
"""

import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

image_dir = '../../images/city_college/'

images_available = sorted(os.listdir(image_dir), key= lambda image_path: int(image_path.split("_")[-2]))

images = [Image.open(os.path.join(image_dir, image_path)).rotate(180) for image_path in images_available]
images = [image.resize((800,600), resample=Image.LANCZOS) for image in images]

# All 5 images
num_images = len(images)
fig, ax = plt.subplots(nrows=1, ncols=num_images, sharey=True, figsize=(20, 3))

for axis, image, image_path in zip(ax, images, images_available):
    axis.imshow(image)
    axis.set_title("Baseline {} cm".format(image_path.split("_")[-2]))

plt.show()

# The first and last image with a baseline of 44in
fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(20, 7))

for axis, image, image_path in zip(ax, [images[0]] + [images[-1]], [images_available[0]] + [images_available[-1]]):
    axis.imshow(image)
    axis.set_title("Baseline {} cm".format(image_path.split("_")[-2]))

plt.show()

import numpy as np

def coorespondance_2D(array_a, array_b):
  # convolves array_a across array_b but subtracts rather than multiplies
  # assumes dimensions of array_b greater than or equal to corresponding of array_a
#   print(array_a.shape)
#   print(array_b.shape)

  num_y_convolutions = len(array_b) - len(array_a) + 1
  num_x_convolutions = len(array_b[0]) - len(array_a[0]) + 1

  results = np.zeros((num_y_convolutions, num_x_convolutions))
  convs = 0

#   print(num_y_convolutions)
#   print(num_x_convolutions)

  for y in range(num_y_convolutions):
    for x in range(num_x_convolutions):
      if convs % 100 == 0:
        pass
      convs += 1
      for i in range(len(array_a)):
        for j in range(len(array_a[0])):
           results[y,x] += np.absolute(array_a[i,j]-array_b[y+i,x+j])
  print("Total coorespondances calcluated: ", convs)
  return results

def coorespondance_3D(array_a, array_b):
  # convolves array_a across array_b but subtracts rather than multiplies
  # assumes dimensions of array_b greater than or equal to corresponding of array_a
#   print(array_a.shape)
#   print(array_b.shape)

  num_y_convolutions = len(array_b) - len(array_a) + 1
  num_x_convolutions = len(array_b[0]) - len(array_a[0]) + 1

  results = np.zeros((num_y_convolutions, num_x_convolutions))
  convs = 0

#   print(num_y_convolutions)
#   print(num_x_convolutions)

  for y in range(num_y_convolutions):
    for x in range(num_x_convolutions):
      if convs % 100 == 0:
        pass
      convs += 1
      for i in range(len(array_a)):
        for j in range(len(array_a[0])):
          for k in range(3):
            results[y,x] += np.absolute(array_a[i,j,k]-array_b[y+i,x+j,k])
  print("Total coorespondances calcluated: ", convs)
  return results

def NTSC_Luminance_Equation(pixel):
    luminance_coefficients = [0.299, 0.587, 0.114]
    return np.dot(pixel, luminance_coefficients)

def get_intensity_image(image):
    img_array = np.array(image)
    return np.array([[NTSC_Luminance_Equation(img_array[i, j, :])
                    for j in range(img_array.shape[1])]
                   for i in range(img_array.shape[0])])

# The second and third image with a baseline of 11in
chosen_images = [1, 2]

fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(20, 7))

for axis, image, image_path in zip(ax, [images[chosen_images[0]]] + [images[chosen_images[1]]],
                                   [images_available[chosen_images[0]]] + [images_available[chosen_images[1]]]):
    axis.imshow(image)
    axis.set_title("Baseline {} cm".format(image_path.split("_")[-2]))

plt.show()

chosen_grayscale_images = [get_intensity_image(images[i])/255 for i in chosen_images]

fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(20, 7))

for axis, image, image_path in zip(ax, chosen_grayscale_images,
                                   [images_available[chosen_images[0]]] + [images_available[chosen_images[1]]]):
    axis.imshow(image, cmap='gray')
    axis.set_title("Normalized Grayscale Baseline {} cm".format(image_path.split("_")[-2]))

plt.show()

coorespondances = [[(-1,-1)]*chosen_grayscale_images[0].shape[1]]*chosen_grayscale_images[0].shape[0]
kernel_size = 41
i = kernel_size//2 + 1
j = kernel_size//2 + 1
search_range = 100

while i < chosen_grayscale_images[1].shape[0]- (kernel_size//2 + 1):
  while j < chosen_grayscale_images[1].shape[1]- (kernel_size//2 + 1):
    print(i,j)

    min_Y_window = max(i-search_range, (kernel_size//2 + 1))
    max_Y_window = min(chosen_grayscale_images[0].shape[0]-(kernel_size//2 + 1),i+search_range)
    min_X_window = max(j-search_range, (kernel_size//2 + 1))
    max_X_window = min(chosen_grayscale_images[0].shape[1]-(kernel_size//2 + 1),i+search_range)
    print(min_Y_window, max_Y_window, min_X_window, max_X_window)

    kernel_Y_min = i - (kernel_size//2 + 1)
    kernel_Y_max = i + (kernel_size//2 + 1)
    kernel_X_min = j - (kernel_size//2 + 1)
    kernel_X_max = j + (kernel_size//2 + 1)
    print(kernel_Y_min,kernel_Y_max,kernel_X_min,kernel_X_max)
    output = coorespondance_2D(chosen_grayscale_images[1][kernel_Y_min:kernel_Y_max, kernel_X_min:kernel_X_max],
                                            chosen_grayscale_images[0][min_Y_window:max_Y_window, min_X_window:max_X_window])
    try:
      max_coords = np.unravel_index(np.argmin(output, axis=None), output.shape)
    except:
      max_coords = (-1,-1)
    coorespondances[i][j] = max_coords
    print(max_coords)
    print()

    j += 1
  i += 1

coor_array = np.array(coorespondances)
np.savetxt('coor_array.gz', coor_array)
