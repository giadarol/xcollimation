import numpy as np

import xline as xl
import xtrack as xt

line = xl.Line.from_json('./MADX/lhcb1.json')
tracker = xt.Tracker(sequence=line)

llr = xt.LossLocationRefinement(tracker=tracker)

s_apertures = np.array(tracker.line.element_s_locations)[llr.i_apertures]

mask_zero_diff = np.diff(s_apertures)==0

import matplotlib.pyplot as plt
plt.close('all')
plt.figure(1)
plt.plot(s_apertures)
plt.plot(np.where(mask_zero_diff)[0], s_apertures[:-1][mask_zero_diff], '.')
plt.show()
