import xline as xl
from cpymad.madx import Madx

mad=Madx()
mad.call("job_sample_thin.madx")

twtable = mad.twiss()

sequence = xl.Line.from_madx_sequence(
                mad.sequence['lhcb1'],install_apertures=True, 
                apply_madx_errors=False)

out = sequence.to_dict()

out['twiss'] = {}
for kk in ['name', 's', 'x', 'y', 'px', 'py', 
           'betx', 'bety', 'l', 'keyword']:
    out['twiss'][kk] = twtable[kk].tolist()

import json
with open('lhcb1.json', 'w') as fid:
    json.dump(out, fid)



