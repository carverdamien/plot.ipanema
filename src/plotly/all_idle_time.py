#!/usr/bin/env python3
import sys, os, parse
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

def process(input_npz):
    for i in input_npz:
        with open(i,'rb') as f:
            data = np.load(f)
            data = {n:data[n] for n in data.files}
            idle_time = data['idle_time']
            x = np.arange(len(idle_time))
            y = idle_time
            log = os.path.dirname(os.path.dirname(i))
            config = os.path.dirname(os.path.dirname(log))
            bench = os.path.dirname(os.path.dirname(config))
            bench = os.path.basename(bench)
            assert bench == 'hackbench'
            result = log+'/main.out.txt'
            with open(result) as foo:
                r = parse.search(""""time":{time},"tasks":{task:d}""",foo.read())
                load = r.named['task']
            with open(config+'/scheduler') as foo:
                sched = foo.read()
            yield x, y, bench, load, sched

def main():
    output_dir = sys.argv[1]
    input_npz = sys.argv[2:]
    data = {}
    for x,y,bench,load,sched in process(input_npz):
        output_html = '{}/{}-{}.html'.format(output_dir,bench,load)
        d = go.Scatter(
            x=x,
            y=y,
            name=sched,
        )
        data[output_html] = data.get(output_html,[]) + [d]
    for output_html in data:
        fig = go.Figure(data=data[output_html])
        plot(fig, filename=output_html, auto_open=False)

if __name__ == '__main__':
    main()
