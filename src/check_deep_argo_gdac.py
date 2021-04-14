#!/usr/bin/python

import bgcArgoDMQC as bgc
import argopy
argopy.set_options(mode='expert')
fetcher = argopy.DataFetcher()
    
wmos = [
    6902881,
    6902886,
    6902977,
    6903030,
    6903032,
    6903034
]

for w in wmos:
    bgc.io.get_argo(w, local_path=bgc.ARGO_PATH, ftype='summary', url='usgodae')