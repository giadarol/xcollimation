import numpy as np
import pandas as pd

import xtrack as xt
import xline as xl

import logging
logger = logging.getLogger('xtrack')
logger.setLevel(logging.DEBUG)

df = pd.read_csv('Input.csv')

n_part = 20000
n_turns = 10

part_input = xt.Particles(
    p0c=7000e9,
    x=df.x.values[:n_part],
    px=df.xp.values[:n_part], # TODO proper transformation
    y=df.y.values[:n_part],
    py=df.yp.values[:n_part], # TODO proper transformation 
    s=df.s.values[:n_part])

sequence = xl.Line.from_json('MADX/lhcb1.json')

part = part_input.copy()

ref_collimator = 'tcp.c6l7.b1'
i_ref = sequence.element_names.index(ref_collimator)

# Find next drift
for ii in range(i_ref, len(sequence.element_names)):
    if sequence.elements[ii].__class__.__name__ == 'Drift':
        if sequence.elements[ii].length > 0:
            i_first_drift = ii
            coll_half_length=sequence.elements[ii].length 
            break
    elif sequence.elements[ii].__class__.__name__ in ['Multipole', 'Cavity']:
        raise ValueError('Multipole before end of collimator!')

s_ref = sequence.get_s_elements()[i_ref] - coll_half_length
s_start_track = s_ref +2*coll_half_length
i_start_track = i_first_drift + 1

part.s += s_ref # We got to the same reference system as for the sequence

# Drift all particles to end collimator
l_drifts = s_start_track - part.s
temp_drift = xl.Drift(length=l_drifts)
temp_drift.track(part)

part.at_element[:] = i_start_track # TODO To be checked!!!

# 
tracker = xt.Tracker(sequence=sequence)

tracker.track(part, ele_start=i_start_track)

# Get names of elements where particles are lost
part.at_element[part.state==0]

for i_turn in range(n_turns):
    part.s[part.state>0] = 0.
    tracker.track(part)
    n_alive = ((part.state)>0).sum()
    print(f'At turn: {i_turn} {n_alive=}')
    if n_alive<1:
        break

part_before_refinement = part.copy()

loss_loc_refinement = xt.LossLocationRefinement(tracker,
                                            n_theta = 360,
                                            r_max = 1., # m
                                            dr = 50e-6,
                                            ds = 0.1,
                                            save_refine_trackers=False)

import time
t0 = time.time()

loss_loc_refinement.refine_loss_location(part)

t1 = time.time()
print(f'Took\t{(t1-t0)*1e3:.2f} ms')

mask_lost = part.state<1

hist, bin_edges = np.histogram(part.s[mask_lost], range=(0, sequence.get_length()), bins=27000)

import matplotlib.pyplot as plt
plt.close('all')

plt.figure(1)
plt.semilogy(bin_edges[:-1], hist, '.')
for ii in range(9):
    plt.axvline(x=sequence.get_length()/8*ii)

plt.show()
