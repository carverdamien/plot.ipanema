#!/usr/bin/env python3
import sys, tarfile, parse, logging, multiprocessing, os, h5py
import numpy as np

def parse_tracer_file(f):
    p = parse.compile("""{clock:d} RQ_SIZE {pid:d} {size:d} {op:d}""")
    data = {k:[] for k in ['clock', 'pid', 'size', 'op']}
    for l in f.readlines():
        r = p.parse(l.decode("utf-8")).named
        for k in r:
            data[k].append(int(r[k]))
    return data

def load_tracer_tgz(path):
    data = {}
    with tarfile.open(path) as tgz:
        members = { m.name:m for m in tgz.getmembers() if m.isreg() }
        for cpuid in range(len(members)):
            expected_member_name = 'tracer/{}'.format(cpuid)
            if expected_member_name not in members:
                logging.error('{} not in {}'.format(expected_member_name, path))
                sys.exit(0)
            f = tgz.extractfile(members[expected_member_name])
            df = parse_tracer_file(f)
            data[str(cpuid)] = [df['clock'],df['size']]
    return data

def func(args):
    path, name = args
    with tarfile.open(path) as tgz:
        members = { m.name:m for m in tgz.getmembers() if m.isreg() }
        return parse_tracer_file(tgz.extractfile(members[name]))

def load_tracer_tgz_in_parallel(path, parallel):
    p = multiprocessing.Pool(parallel)
    data = {}
    with tarfile.open(path) as tgz:
        members = { m.name:m for m in tgz.getmembers() if m.isreg() }
        df = p.map(func,[[path,'tracer/{}'.format(cpuid)] for cpuid in range(len(members))])
        for i in range(len(df)):
            data[str(i)] = [df[i]['clock'],df[i]['size']]
    return data
        
def main():
    level = logging.ERROR
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)
    rqsize_h5 = sys.argv[1]
    tracer_tgz = sys.argv[2]
    if 'PARALLEL' in os.environ:
        parallel = int(os.environ['PARALLEL'])
        data = load_tracer_tgz_in_parallel(tracer_tgz,parallel)
    else:
        data = load_tracer_tgz(tracer_tgz)
    with h5py.File(rqsize_h5, "w") as f:
        for k in data:
            f.create_dataset(k,data=data[k],compression="gzip",dtype='i8')
            #df = f.create_dataset(k, np.shape(data[k]), compression="gzip", dtype='i8')
            #df = data[k]

if __name__ == '__main__':
    main()
