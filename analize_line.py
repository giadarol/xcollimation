import numpy as np

import xline as xl
import xtrack as xt

apertures_are_identical = (
        xt.loss_location_refinement.loss_location_refinement.apertures_are_identical)

line = xl.Line.from_json('./MADX/lhcb1.json')
tracker = xt.Tracker(sequence=line)

llr = xt.LossLocationRefinement(tracker=tracker)

s_apertures = np.array(tracker.line.element_s_locations)[llr.i_apertures]

mask_zero_diff = np.diff(s_apertures)==0
i_aper_zero_diff = np.where(mask_zero_diff)[0]
i_ele0_zero_diff = np.array(llr.i_apertures)[:-1][mask_zero_diff]
i_ele1_zero_diff = np.array(llr.i_apertures)[1:][mask_zero_diff]

mask_discontinuity = mask_zero_diff.copy()
for ii in range(len(i_ele0_zero_diff)):
    ap0 = tracker.line.elements[i_ele0_zero_diff[ii]]
    ap1 = tracker.line.elements[i_ele1_zero_diff[ii]]
    if apertures_are_identical(ap0, ap1):
        mask_discontinuity[i_aper_zero_diff[ii]] = False

import matplotlib.pyplot as plt
plt.close('all')
plt.figure(1)
plt.plot(s_apertures)
plt.plot(np.where(mask_zero_diff)[0], s_apertures[:-1][mask_zero_diff], '.')
plt.plot(np.where(mask_discontinuity)[0], s_apertures[:-1][mask_discontinuity], 'r.')
plt.show()
