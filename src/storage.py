#!/usr/bin/env python3

import argparse, os, logging
import pandas as pd
from parser import Oltp
from common import *

description="""
Dataframe utility for sysbench OLTP:
Goes through input Directories and parses files in ./data/ to produce and store a Dataframe.
"""

def parseCmdLine():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('inputDirectories', nargs='+',
                        help='Directories to use as input')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Output datafile')
    parser.add_argument('-v', '--verbose', action='count')

    return parser.parse_args()

def save(output, data):
    _, ext = os.path.splitext(output)
    if ext != '.csv':
        error = 'Unsupported output ext: {}'.format(ext)
        logging.error(error)
        raise ExtensionError
    logging.info("Converting into a dataframe...")
    df = pd.DataFrame([
        dict(row, **{k:d[k] for k in d if k!='data'})
        for d in data
        for row in d['data']
    ])
    logging.debug(str(df))
    logging.info("Saving to {}...".format(output))
    df.to_csv(output)
    pass

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

    oltp_parser = Oltp()
    data = []
    for d in args.inputDirectories:
        try:
            logging.info("Parsing {}...".format(d))
            data.append(oltp_parser.parse(d))
            logging.info("Parsing {}... Done".format(d))
        except ParsingError as e:
            logging.error("Parsing {} failed. Ignoring.".format(d))
    save(args.output, data)

if __name__ == '__main__':
    main()
