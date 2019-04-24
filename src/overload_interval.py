#!/usr/bin/env python3
import sys, h5py
import numpy as np

def compute_overload_interval(data):
    return {
        cpu:_compute_overload_iterval(data[cpu][0],data[cpu][1])
        for cpu in data
    }

def _compute_overload_iterval(clock, size):
    clock, size = drop_last_zero(clock, size)
    assert len(clock) == len(size)
    N = len(clock)
    assert size[-1] != 0
    assert np.sum(size < 0) == 0
    sel_overloaded = size > 1
    if np.sum(sel_overloaded) == 0:
        # Never overloaded
        return  np.array([[],[]])
    sel_overloaded_next = np.concatenate((np.array([False]), sel_0[:-1]))
    overloaded_iterval = [clock[sel_overloaded_next], clock[sel_overloaded]]
    return overloaded_iterval

def drop_last_zero(clock, size):
    while size[-1] == 0:
        size = size[:-1]
        clock = clock[:-1]
    return clock, size
    
def main():
    idle_iterval_h5 = sys.argv[1]
    rqsize_h5 = sys.argv[2]
    with h5py.File(rqsize_h5, 'r') as f:
        data = {cpu:f[cpu] for cpu in f.keys()}
        data = compute_overload_interval(data)
        with h5py.File(idle_iterval_h5, 'w') as f:
            for cpu in data:
                f.create_dataset(cpu,data=data[cpu],compression="gzip",dtype='i8')

if __name__ == '__main__':
    main()
