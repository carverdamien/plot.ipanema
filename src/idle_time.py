#!/usr/bin/env python3
import sys
import numpy as np

def compute_idle_time(clock, size):
    assert len(clock) == len(size)
    N_CPU = len(clock)
    idle_time = tuple(_compute_idle_time(clock[cpu],size[cpu]) for cpu in range(N_CPU))
    idle_time = np.concatenate(idle_time)
    idle_time = np.sort(idle_time)
    return {'idle_time':idle_time}

def _compute_idle_time(clock, size):
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
    idle_time = clock[sel_0_next] - clock[sel_0]
    return idle_time

def drop_last_zero(clock, size):
    while size[-1] == 0:
        size = size[:-1]
        clock = clock[:-1]
    return clock, size
    
def main():
    idle_time_npz = sys.argv[1]
    rqsize_npz = sys.argv[2]
    with open(rqsize_npz, 'rb') as f:
        data = np.load(f)
        data = {n:data[n] for n in data.files}
        data = compute_idle_time(data['clock'], data['size'])
        with open(idle_time_npz, 'wb') as f:
            np.savez(f,**data)

if __name__ == '__main__':
    main()
