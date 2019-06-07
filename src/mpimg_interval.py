#!/usr/bin/env python3
import numpy as np
import matplotlib.image as mpimg
import h5py
import math

white = np.array([1,1,1])

height = 1080
height = 160
width  = 1920
width *= 20
image  = np.zeros((height, width,3))

# Example
# i = height//2
# j = width//2
# image[i,j,:] = white

f = '/mnt/data/damien/storage/i80/hackbench/1.0-3/3d5625eec031d249757ecc716473030a/log/5nk2jIomejEZD6/sched_monitor/idle_interval.hdf5'
h=h5py.File(f, 'r')
data = [np.array(h[cpu]) for cpu in sorted(list(h.keys()), key=lambda e:int(e))]
h.close()

assert(len(data) == height)

tmin = min(data[i][0][0] for i in range(height))
tmax = max(data[i][1][-1] for i in range(height))
T = float((tmax+1) - tmin)
W = float(width)

print(T,W)

for i in range(height):
    print(i)
    for j in range(width):
        if (j+1)*T/W+tmin < data[i][0][0]:
            image[i,j,:] = white
        else:
            break
    for j in range(width-1,-1,-1):
        if (j)*T/W+tmin > data[i][1][-1]:
            image[i,j,:] = white
        else:
            break
    for n in range(len(data[i][0])):
        _a = data[i][0][n]
        _b = data[i][1][n]
        a = math.floor((_a-tmin)*W/T)
        b = math.ceil((_b-tmin)*W/T)
        # print(a,b)
        for j in range(a,b):
            _c = j*T/W+tmin
            _d = (j+1)*T/W+tmin
            # print(_a,_b)
            # print(_c,_d)
            inf = max(_a,_c)
            sup = min(_b,_d)
            r = (sup - inf) * W/T
            if r < 0:
                r = 0
            # print(r)
            # a =1/0
            image[i,j,:] += r*white

mpimg.imsave("image-{}.png".format(width), image)
