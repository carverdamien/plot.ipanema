#!/usr/bin/env python3
import datashader as ds, pandas as pd
import datashader.transfer_functions as tf
from datashader.utils import export_image
import h5py
import numpy as np

data = [
    [0,0,0],
    [1,1,0],
    [.5,.5,1],
]

df = pd.DataFrame([])
f = '/mnt/data/damien/storage/i80/hackbench/1.0-3/3d5625eec031d249757ecc716473030a/log/5nk2jIomejEZD6/sched_monitor/rqsize.hdf5'
with h5py.File(f, 'r') as h:
    for cpu in h:
        print(cpu)
        clock, size = h[cpu]
        cpu = float(cpu) * np.ones(np.shape(clock))
        df = df.append(pd.DataFrame({'y_col':cpu, 'x_col':clock, 'z_col':size}))

# df = pd.DataFrame(data,columns=['x_col', 'y_col', 'z_col'])

cvs = ds.Canvas(plot_width=1920, plot_height=1080)
agg = cvs.points(df, 'x_col', 'y_col', ds.mean('z_col'))
cmap = ['lightblue', 'darkblue']
cmap = ['lightblue', 'red']
img = tf.shade(agg, cmap=cmap, how='log')
export_image(img, "test")
