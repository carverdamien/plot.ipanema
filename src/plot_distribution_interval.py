#!/usr/bin/env python3
import sys, h5py, json
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

def main():
    output = sys.argv[1]
    inputs = sys.argv[2:]
    data = []
    for i in inputs:
        print(i)
        name = '/'.join([i.split('/')[8],i.split('/')[10]])
        dirpath = '/'.join(i.split('/')[:-4])
        scheduler = str(open(dirpath+'/scheduler').read())
        logpath = '/'.join(i.split('/')[:-2])
        jobs = json.loads(open(logpath+'/main.out.txt').readlines()[-1])['tasks']
        name = '{}-{}'.format(scheduler,jobs)
        name = '{}-{}'.format(jobs,scheduler)
        if jobs != 8000:
            continue
                durations = h5_to_durations(i)
        durations = np.sort(durations)
        x = np.unique(durations)
        y,x=np.histogram(durations, bins=x)
        y = np.cumsum(y)
        # y = y * 1/np.max(y)
        data.append(go.Scatter(
            x=x,
            name=name,
            y=y,
        ))
    fig = go.Figure(data=data)
    plot(fig, filename=output, auto_open=False)
    pass

def data_to_duration(data):
    return data[1] - data[0]

def h5_to_durations(path):
    with h5py.File(path, 'r') as data:
        durations = [data_to_duration(np.array(data[cpu])) for cpu in data]
        return np.concatenate(durations)

if __name__ == '__main__':
    main()

