#!/usr/bin/env python3
import intervals, h5py, sys, itertools
from tqdm import tqdm

def length(i):
    l = 0
    for e in i:
        l += e.upper - e.lower
    return l

def data_to_intervals(data):
    i = intervals.empty()
    for a,b,_ in itertools.zip_longest(data[0], data[1], tqdm(range(len(data[0])))):
        i = i | intervals.closed(a,b)
    return i

def h5_to_intervals(path):
    with h5py.File(path, 'r') as data:
        return {
            cpu : data_to_intervals(data[cpu])
            for cpu in data
        }

def intervals_to_data(i):
    data = {}
    for cpu in i:
        data[cpu]=[[],[]]
        for e in i[cpu]:
            data[cpu][0].append(e.lower)
            data[cpu][1].append(e.upper)
    
def data_to_h5(path, data):
    with h5py.File(path, 'w') as f:
        for cpu in data:
            f.create_dataset(cpu,data=data[cpu],compression="gzip",dtype='i8')
    
def main():
    notwc_h5 = sys.argv[1]
    idle_h5 = sys.argv[2]
    overload_h5 = sys.argv[3]
    print('Loading idle and overload into intervals')
    idle = h5_to_intervals(idle_h5)
    overload = h5_to_intervals(overload_h5)
    print('Computing union_overload')
    union_overload = intervals.empty()
    for cpu in overload:
        union_overload = union_overload | overload[cpu]
    print('Computing notwc[cpu] = idle[cpu] & union_overload')
    notwc = {
        cpu : idle[cpu] & union_overload
        for cpu in idle
    }
    print('Saving notwc into hdf5')
    data = intervals_to_data(notwc)
    data_to_h5(notwc_h5, data)

if __name__ == '__main__':
    main()
