#!/usr/bin/python

import bgcArgoDMQC as bgc

# get core and bgc profiles for meds dac
gx = bgc.get_index(index='global')
bx = bgc.get_index()
gx = gx[gx.dac == 'meds']
bx = bx[bx.dac == 'meds']

# get arvor floats only
gx = gx[gx.profiler_type == 844]
bx = bx[bx.profiler_type == 844]

# get core files only
gx = gx[~gx.wmo.isin(bx.wmo)]