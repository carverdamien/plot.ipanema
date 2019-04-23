#!/usr/bin/env python3
import sys, tarfile, parse, logging, multiprocessing, os
import numpy as np
import pandas as pd

def parse_tracer_file(f):
    p = parse.compile("""{clock:d} RQ_SIZE {pid:d} {size:d} {op:d}""")
    return pd.DataFrame([p.parse(l.decode("utf-8")).named for l in f.readlines()])

def load_tracer_tgz(path):
    data = { 'clock' : [], 'size' : [] }
    with tarfile.open(path) as tgz:
        members = { m.name:m for m in tgz.getmembers() if m.isreg() }
        for cpuid in range(len(members)):
            expected_member_name = 'tracer/{}'.format(cpuid)
            if expected_member_name not in members:
                logging.error('{} not in {}'.format(expected_member_name, path))
                sys.exit(0)
            f = tgz.extractfile(members[expected_member_name])
            df = parse_tracer_file(f)
            for k in data:
                data[k].append(np.array(df[k]))
    return {k:np.array(data[k]) for k in data}

def func(args):
    path, name = args
    with tarfile.open(path) as tgz:
        members = { m.name:m for m in tgz.getmembers() if m.isreg() }
        return parse_tracer_file(tgz.extractfile(members[name]))

def load_tracer_tgz_in_parallel(path, parallel):
    p = multiprocessing.Pool(parallel)
    data = { 'clock' : [], 'size' : [] }
    with tarfile.open(path) as tgz:
        members = { m.name:m for m in tgz.getmembers() if m.isreg() }
        dfs = p.map(func,[[path,'tracer/{}'.format(cpuid)] for cpuid in range(len(members))])
        for df in dfs:
            for k in data:
                data[k].append(np.array(df[k]))
    return {k:np.array(data[k]) for k in data}
        
def main():
    level = logging.ERROR
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)
    rqsize_npz = sys.argv[1]
    tracer_tgz = sys.argv[2]
    if 'PARALLEL' in os.environ:
        parallel = int(os.environ['PARALLEL'])
        data = load_tracer_tgz_in_parallel(tracer_tgz,parallel)
    else:
        data = load_tracer_tgz(tracer_tgz)
    with open(rqsize_npz, 'wb') as f:
        np.savez(f, **data)

if __name__ == '__main__':
    main()
