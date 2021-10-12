import xline as xl
from cpymad.madx import Madx

mad=Madx()
mad.call("job_sample_thin.madx")

sequence = xl.Line.from_madx_sequence(
                mad.sequence['lhcb1'],install_apertures=True, 
                apply_madx_errors=False)

sequence.to_json('lhcb1.json')
