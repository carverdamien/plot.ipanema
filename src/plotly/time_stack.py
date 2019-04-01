#!/usr/bin/env python3

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
TIME_STACK = []
# TIME_STACK = ['fair','ipanema']
TIME_STACK += ['sched','system','user','idle']
TIME_STACK += ['softirq','irq','nice','steal','guest','guest_nice','iowait']
TIME_STACK += ['sm_idle']

def parseCmdLine():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('inputFile',
                        help='dataframe to use as input')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Output file to store the plot')
    parser.add_argument('-v', '--verbose', action='count')
    return parser.parse_args()

def get_y(df, load, scheduler, time):
    sel = df['load'] == load
    sel = np.logical_and(sel, df['scheduler'] == scheduler)
    return np.mean(df[time][sel])
    # return np.min(df[time][sel])
    # return np.array(df[time][sel])[1]

def save(output, df):
    LOADS      = np.unique(df['load'])
    SCHEDULERS = np.unique(df['scheduler'])
    
    ticktext = ['{}-{}'.format(pretty_label(sch),load) for load in LOADS for sch in SCHEDULERS]
    tickvals = np.arange(len(ticktext))
    data = [
        go.Bar(
            x=tickvals,
            y=[get_y(df, load, sch, time) for load in LOADS for sch in SCHEDULERS],
            name=time,
            )
        for time in TIME_STACK
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
    HEADER = ['load','scheduler'] + TIME_STACK
    if 'kernel' in df.columns:
        assert len(np.unique(df['kernel']))==1
        df.drop(columns=['kernel'],inplace=True)
    if 'clients' in df.columns:
        df.rename(columns={'clients':'load'},inplace=True)
    if 'tasks' in df.columns:
        df.rename(columns={'tasks':'load'},inplace=True)
    if 'client_sched' in df.columns or 'engine_sched' in df.columns:
        assert np.sum(df['client_sched'] == df['engine_sched']) == len(df)
        df.drop(columns=['client_sched'],inplace=True)
        df.rename(columns={'engine_sched':'scheduler'},inplace=True)
    # Unit conversion
    for header in ['user','system','idle','iowait','softirq','irq','nice','steal','guest','guest_nice']:
        header = "procstat_{}".format(header)
        # proc/stat is in USER_HZ ie 10**-2sec getconf CLK_TCK)
        # schedmonitor is in 10**-9sec
        # 9-2=7
        df[header] = 10**7 * df[header]
    logging.info('Mean difference between idle_total_ns and procstat_idle is {}.'.format(
        np.mean(df['idle_total_ns'] - df['procstat_idle'])))
    for header in ['procstat_idle','idle_total_ns']:
        logging.info('{} in [{};{}]'.format(header,np.min(df[header]),np.max(df[header])))
    columns = {
        'procstat_{}'.format(k):k
        for k in ['user','system','idle','iowait','softirq','irq','nice','steal','guest','guest_nice']
        }
    columns.update({
            'ipanema_total_ns':'ipanema',
            'fair_total_ns':'fair',
            'sched_total_ns':'sched',
            'idle_total_ns':'sm_idle',
            })
    df.rename(columns=columns,inplace=True)
    for header in HEADER:
        assert header in df.columns, "{} not in df.columns".format(header)
    df.drop(columns=[header for header in df.columns if header not in HEADER],inplace=True)
    df.dropna(inplace=True)
    df['system'] = df['system'] - df['sched']
    # df['sched'] = df['sched'] - (df['ipanema'] + df['fair'])
    # cpu sec
    for header in TIME_STACK:
        df[header] = df[header] / 160 / 10**9
    return df
    # Ratio conversion
    total = np.zeros(len(df))
    for header in TIME_STACK:
        total += df[header]
    logging.info('Total min:{}, max:{}, mean:{}, std:{}'.format(
            np.min(total),
            np.max(total),
            np.mean(total),
            np.std(total),
            )
                 )
    for header in TIME_STACK:
        df[header] = df[header] / total
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
    
    df = pd.read_csv(args.inputFile)
    df = unified_dataframe(df)
    if(len(df) == 0):
        logging.error('Empty dataframe')
    else:
        save(args.output, df)

if __name__ == '__main__':
    main()
