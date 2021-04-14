#!/usr/bin/python

from pathlib import Path
import pandas as pd

import matplotlib.pyplot as plt

import argopy

argopy.set_options(mode='expert')

fetcher = argopy.IndexFetcher(src='localftp')
df = pd.read_hdf(Path('../data/pts-flt-meds.h5'))
high_res = df[df.pts > 500]

idx = fetcher.float(high_res.wmo)
ix = idx.to_dataframe()
fig, ax = idx.plot('trajectory')
