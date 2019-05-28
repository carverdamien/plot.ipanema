#!/usr/bin/env python3
from status import remove_unstable
from common import *
from update_rows import update_rows
import argparse, logging, itertools, sys, os, json
import pandas as pd
import numpy as np

SCHED_MONITOR = ['sched_total_ns','idle_total_ns']
SCHED_DEBUG = ['cpu_clk','sched_clk','ktime']
STACK = ['sched_total_ns', 'application', 'idle_total_ns']

def get_y(df, load, scheduler, name):
    sel = df['load'] == load
    sel = np.logical_and(sel, df['scheduler'] == scheduler)
    return np.mean(df[name][sel])

def stacked(config, df):
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
    # Some conversions
    N_CPU = 160
    for header in SCHED_DEBUG:
        df[header] = 10**-3 * df[header]
    for header in SCHED_MONITOR:
        df[header] = 10**-9 / N_CPU * df[header]
    df.dropna(inplace=True)
    sel = df['ktime'] < (df['idle_total_ns'] + df['sched_total_ns'])
    count = np.sum(sel)
    if count > 0:
        logging.error('Dropping {} case out of {}, because ktime < idle_total_ns + sched_total_ns'.format(count,len(df)))
        df.loc[sel,['ktime']] = float('Nan')
        df.dropna(inplace=True)
    df['application'] = df['ktime'] - df['idle_total_ns'] - df['sched_total_ns']
    for header in HEADER:
        assert header in df.columns, "{} not in df.columns".format(header)
    df.drop(columns=[header for header in df.columns if header not in HEADER],inplace=True)
    LOADS      = np.unique(df['load'])
    SCHEDULERS = np.unique(df['scheduler'])
    stack = 'scheduler-load'
    columns = [stack] + ['{}-{}'.format(pretty_label(sch),int(load)) for load in LOADS for sch in SCHEDULERS]
    data = [
        [name] + [
            get_y(df, load, sch, name)
            for load,sch in itertools.product(LOADS,SCHEDULERS)
        ]
        for name in STACK
    ]
    df = pd.DataFrame(data=data,columns=columns)
    df = df.set_index(stack).T
    return df
    
description=""
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

def main(save):
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
    df = remove_unstable(df, 'st_mtime')
    with open(args.config) as f:
        config = json.load(f)
        df = update_rows(config['update_rows'], df)
        df = stacked(config, df)
        save(args.output, df)
