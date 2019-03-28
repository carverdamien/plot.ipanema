#!/usr/bin/env python3

import argparse, logging
import pandas as pd
import numpy as np

description="""
Select utility for Dataframes.
Loads a Dataframe and select rows to create a smaller Dataframe.
"""

def parseCmdLine():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('selectors', nargs='+',
                        help='a list of KEY==VALUE or KEY>=VALUE')
    parser.add_argument('-i','--input',
                        required=True,
                        help='dataframe to use as input')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Output file to store the dataframe')
    parser.add_argument('-v', '--verbose', action='count')
    return parser.parse_args()

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

    df = pd.read_csv(args.input)
    sel = np.ones(len(df), dtype='bool')
    # TODO: add logical_or options.
    OP = {
        '==':lambda sel,key,value: np.logical_and(sel, df[key] == value),
        '!=':lambda sel,key,value: np.logical_and(sel, df[key] != value),
        '<=':lambda sel,key,value: np.logical_and(sel, df[key] <= float(value)),
        '>=':lambda sel,key,value: np.logical_and(sel, df[key] >= float(value)),
    }
    for op, key, value in [[op]+selector.split(op) for selector in args.selectors for op in OP if op in selector]:
        logging.info('Applying "{}"{}"{}"'.format(key, op, value))
        sel = OP[op](sel,key,value)
    df = df.loc[sel]
    df.to_csv(args.output)

if __name__ == '__main__':
    main()
