#!/usr/bin/env python3

from status import remove_unstable
from common import *
import argparse, logging, itertools, sys, os, json
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import seaborn as sns

description="""
Plot utility:
Loads a Dataframe and plots a view of the data.
"""

def parseCmdLine():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('inputFile',
                        help='dataframe to use as input')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Output file to store the plot')
    parser.add_argument('-c', '--config',
                        required=True,
                        help='xkey and keys config.json')
    parser.add_argument('-v', '--verbose', action='count')

    return parser.parse_args()

def box_view(df, metric, xkey, keys, values):
    color = {}
    colors = itertools.cycle(materialpalette_colors)
    def new_color():
        return next(colors)
    for names in itertools.product(*values):
        names=list(names)
        sel = np.ones(len(df), dtype='bool')
        for i in range(len(names)):
            sel = np.logical_and(sel, df[keys[i]] == names[i])
        if np.sum(sel) == 0:
            continue
        x = np.array(df[xkey][sel])
        y = np.array(df[metric][sel])
        name = ','.join(names)
        name = pretty_label(name)
        color[name] = color.get(name, new_color())
        marker = dict(color=color[name])
        yield x, name, y, marker
    pass

def line_view(df, metric, xkey, keys, values):
    color = {}
    colors = itertools.cycle(materialpalette_colors)
    def new_color():
        return next(colors)
    for names in itertools.product(*values):
        names=list(names)
        sel = np.ones(len(df), dtype='bool')
        for i in range(len(names)):
            sel = np.logical_and(sel, df[keys[i]] == names[i])
        if np.sum(sel) == 0:
            continue
        X = []
        Y = []
        for x in np.sort(np.unique(df[xkey][sel])):
            sel_x = np.logical_and(sel, df[xkey] == x)
            X.append(x)
            Y.append(np.mean(df[metric][sel_x]))
        name = 'mean({})'.format(','.join(names))
        color[name] = color.get(name, new_color())
        marker = dict(color=color[name])
        yield X, name, Y, marker
    pass

def filterout_if_single_value(keys, values):
    values_ignored = [v for v in values if len(v)==1]
    keys_ignored = [keys[i] for i in range(len(keys)) if len(values[i])==1]
    values = [v for v in values if v not in values_ignored]
    keys = [k for k in keys if k not in keys_ignored]
    return keys, values, keys_ignored, values_ignored

def save(config, metric, output, df):
    xkey = config['xkey']
    keys = config['keys']
    assert(xkey not in keys)
    values = [list(np.unique(df[k])) for k in keys]
    keys, values, keys_ignored, values_ignored = filterout_if_single_value(keys, values)
    logging.info("Ignoring keys {}".format(','.join(keys_ignored)))
    title = "{}".format(','.join([
        "{}={}".format(k,v[0])
        for k,v in itertools.zip_longest(keys_ignored,values_ignored)
        ])
    )
    box_data = pd.DataFrame([
        {
            xkey:x,
            metric:y,
            'hue':name,
        }
        for X, name, Y, marker in box_view(df, metric, xkey, keys, values)
        for x,y in itertools.zip_longest(X,Y)
    ])
    tickvals = np.unique([x for X,_,_,_ in box_view(df, metric, xkey, keys, values) for x in X])
    ax = sns.lineplot(x=xkey,y=metric,hue='hue',data=box_data,err_style="bars")
    ax.set_title(title)
    ax.set_xticks(tickvals)
    fig = ax.get_figure()
    fig.set_size_inches(6.4*3, 4.8*1.2)
    fig.savefig(output)

def update_rows(updates, df):
    for op in updates:
        assert(op["op"] == "cas")
        sel = df[op["key"]] == op["old"]
        df[op["key"]][sel] = op["new"]
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

    metric = os.path.basename(sys.argv[0])
    metric = os.path.splitext(metric)[0]
    logging.info('metric={}'.format(metric))
    
    df = remove_unstable(pd.read_csv(args.inputFile), 'st_mtime')
    if(len(df) == 0):
        logging.error('Empty dataframe')
    else:
        with open(args.config) as f:
            config = json.load(f)
            df = update_rows(config['update_rows'], df)
            save(config, metric, args.output, df)

if __name__ == '__main__':
    main()
