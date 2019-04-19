#!/usr/bin/env python3

from status import remove_unstable
from common import *
import argparse, logging, itertools, sys, os, json
import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

description="""
Plot utility:
Loads a Dataframe and plots a view of the data.
"""
ENQ_STACK = ['enQ_no_reason', 'enQ_new', 'enQ_wakeup', 'enQ_wakeup_mig', 'enQ_lb_mig']
ENQ_WC_STACK = ['enQ_wc_no_reason', 'enQ_wc_new', 'enQ_wc_wakeup', 'enQ_wc_wakeup_mig', 'enQ_wc_lb_mig']
def stack():
    for i in itertools.chain(ENQ_STACK, ENQ_WC_STACK):
        yield i
STACK = [e for e in stack()]

def parseCmdLine():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('inputFile',
                        help='dataframe to use as input')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Output file to store the plot')
    parser.add_argument('-c', '--config',
                        required=False,
                        help='Unused argument config.json')
    parser.add_argument('-v', '--verbose', action='count')
    return parser.parse_args()

def get_y(df, load, scheduler, name):
    sel = df['load'] == load
    sel = np.logical_and(sel, df['scheduler'] == scheduler)
    return np.mean(df[name][sel])
    # return np.min(df[name][sel])
    # return np.array(df[name][sel])[1]

def save(output, df):
    LOADS      = np.unique(df['load'])
    SCHEDULERS = np.unique(df['scheduler'])
    
    ticktext = ['{}-{}'.format(pretty_label(sch),load) for load in LOADS for sch in SCHEDULERS]
    tickvals = np.arange(len(ticktext))
    data = [
        go.Bar(
            x=tickvals,
            y=[get_y(df, load, sch, name) for load in LOADS for sch in SCHEDULERS],
            name=name,
            )
        for name in STACK
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

def unified_dataframe(df):
    HEADER = ['load','scheduler'] + STACK
    if 'kernel' in df.columns:
        assert len(np.unique(df['kernel']))<=1
        df.drop(columns=['kernel'],inplace=True)
    if 'clients' in df.columns:
        df.rename(columns={'clients':'load'},inplace=True)
    if 'tasks' in df.columns:
        df.rename(columns={'tasks':'load'},inplace=True)
    if 'client_sched' in df.columns or 'engine_sched' in df.columns:
        assert np.sum(df['client_sched'] == df['engine_sched']) == len(df)
        df.drop(columns=['client_sched'],inplace=True)
        df.rename(columns={'engine_sched':'scheduler'},inplace=True)
    N_CPU = 160
    df.dropna(inplace=True)
    for i in range(len(ENQ_STACK)):
        sel = df[ENQ_WC_STACK[i]] > df[ENQ_STACK[i]]
        count = np.sum(sel)
        if count > 0:
            logging.error('Dropping {} case out of {}, because {} > {}'.format(count,len(df),ENQ_WC_STACK[i],ENQ_STACK[i]))
            df.loc[sel,[ENQ_STACK[i]]] = float('Nan')
            df.dropna(inplace=True)
        df[ENQ_STACK[i]] = df[ENQ_STACK[i]] - df[ENQ_WC_STACK[i]]
    for header in HEADER:
        assert header in df.columns, "{} not in df.columns".format(header)
    df.drop(columns=[header for header in df.columns if header not in HEADER],inplace=True)
    return df
    
def main():
    args = parseCmdLine()

    # Configure logging
    if args.verbose is None:
        level = logging.ERROR
    elif args.verbose == 1:
        level = logging.WARN
    elif args.verbose == 2:
        level = logging.INFO
    elif args.verbose == 3:
        level = logging.DEBUG
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)
    
    df = remove_unstable(pd.read_csv(args.inputFile), 'st_mtime')
    df = unified_dataframe(df)
    if(len(df) == 0):
        logging.error('Empty dataframe')
    else:
        save(args.output, df)

if __name__ == '__main__':
    main()
