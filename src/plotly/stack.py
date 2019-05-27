#!/usr/bin/env python3

import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

def save(output, df):    
    ticktext = df[df.columns[0]]
    tickvals = np.arange(len(ticktext))
    data = [
        go.Bar(
            x=tickvals,
            y=df[name],
            name=name,
            )
        for name in df.columns[1:]
        ]
    layout = go.Layout(
        barmode='stack',
        xaxis=go.layout.XAxis(
            ticktext=ticktext,
            tickvals=tickvals,
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=output, auto_open=False)

if __name__ == '__main__':
    dummydf = {
        'columns' : [
            'Scheduler Tasks',
            'Time in scheduler',
            'Time in kernel',
            'Time in userspace',
            'Time in idle task'
        ],
        'data' : [
            ['sched0-32tsks',1,1,1,1],
            ['sched1-32tsks',1,1,1,1],
            ['sched2-32tsks',1,1,1,1],
            ['sched0-64tsks',2,2,2,2],
            ['sched1-64tsks',2,2,2,2],
            ['sched2-64tsks',2,2,2,2],
            ['sched0-128tsks',3,3,3,3],
            ['sched1-128tsks',3,3,3,3],
            ['sched2-128tsks',3,3,3,3],
        ],
    }
    save('stack.html', pd.DataFrame(**dummydf))
