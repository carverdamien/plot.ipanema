#!/usr/bin/env python3

import logging
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def save(output, df):
    sns.set()
    ax = df.plot(kind='bar', stacked=True)
    fig = ax.get_figure()
    fig.set_size_inches(6.4*3, 4.8*1.8)
    plt.tight_layout()
    fig.savefig(output)

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
    df = pd.DataFrame(**dummydf)
    df = df.set_index('Scheduler Tasks')
    save('stack.pdf', df)
