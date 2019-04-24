#!/usr/bin/env python3
import sys, h5py
import numpy as np

def compute_idle_interval(data):
    return {
        cpu:_compute_idle_iterval(data[cpu][0],data[cpu][1])
        for cpu in data
    }

def _compute_idle_iterval(clock, size):
    clock, size = drop_last_zero(clock, size)
    assert len(clock) == len(size)
    N = len(clock)
    assert size[-1] != 0
    assert np.sum(size < 0) == 0
    sel_0 = size == 0
    if np.sum(sel_0) == 0:
        # Never idle
        return  np.array([])
    sel_0_next = np.concatenate((np.array([False]), sel_0[:-1]))
    assert np.sum(size[sel_0_next] == 0) == 0
    idle_iterval = [clock[sel_0_next], clock[sel_0]]
    return idle_iterval

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
        data = compute_idle_interval(data)
        with h5py.File(idle_iterval_h5, 'w') as f:
            for cpu in data:
                f.create_dataset(cpu,data=data[cpu],compression="gzip",dtype='i8')

if __name__ == '__main__':
    main()
