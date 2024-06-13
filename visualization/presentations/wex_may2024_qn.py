"""Quinta Normal precipitation timeseries for WEX May 2024 presentation.

This script provides two bar plots. The first one shows the precipitation 
timeseries at Quinta Normal from 1866 to 2022. The data is standardized using 
the mean and standard deviation from 1920 to 2020, and the x-axis spans from 
1850 to 2100. The second plot shows the same data but with a green, blue, and 
red background for the periods 1973-2022 (present), 1851-1900 (past), and 
2050-2099 (future), respectively. 

These plots were used for the Water and Extreme meeting in May 2024.
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/result/repo/extreme-drought/')

from utilities import lens, rpi  # pylint: disable=wrong-import-position

# access data
obs_qn = rpi.rpi_timeseries()['qn']
obs_qn_mean = obs_qn.sel(time=slice('1920', '2020')).mean()
obs_qn_std = obs_qn.sel(time=slice('1920', '2020')).std()
obs_qn = (obs_qn-obs_qn_mean)/obs_qn_std

q = (3-1)/(50-1)
th = np.quantile(obs_qn.sel(time=slice('1973','2022')).values, q)
obs_qn_low = obs_qn.where(obs_qn <= th, drop=True)

# visualize data

# basic plot settings
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# create first plot
_, axs = plt.subplots(1, 1, figsize=(10, 7))
plt.sca(axs)
plt.bar(obs_qn.time.dt.year, obs_qn, width=0.9, fc='lightgrey', ec='k', lw=1.0)
plt.ylabel('Precipitation at Quinta Normal (std. anomaly)')
plt.xlim([1850, 2100])
plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'HD_wex_d101.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)

# create second plot
_, axs = plt.subplots(1, 1, figsize=(10, 7))
plt.sca(axs)
plt.axvspan(1973, 2022, color='green', alpha=0.25)
plt.axvspan(1851, 1900, color='blue', alpha=0.25)
plt.axvspan(2050, 2099, color='red', alpha=0.25)
plt.bar(obs_qn.time.dt.year, obs_qn, width=0.9, fc='lightgrey', ec='k', lw=1.0)
plt.bar(obs_qn_low.time.dt.year, obs_qn_low, width=0.9, fc='red', ec='k', lw=1.0)
plt.axhline(th, color='fuchsia', lw=1.0, ls='--') # type: ignore
plt.ylabel('Precipitation at Quinta Normal (std. anomaly)')
plt.xlim([1850, 2100])
plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'HD_wex_d102.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)