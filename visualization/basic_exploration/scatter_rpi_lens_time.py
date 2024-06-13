"""RPI/LENS vs. time scatter plot.

This script provides a scatter plot of the RPI1 standardized precipitation
anomaly vs. time compared to the LENS1 (upper panel) and LENS2 (lower panel) 
standardized precipitation anomalies. All time series are standardized using 
their respective mean and standard deviation from 1920 to 2020. Additionally, 
the LENS1 and LENS2 ensemble averages are shown. The 5th percentile of the RPI1
time series is shown as a reference.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/result/repo/extreme-drought/')

from utilities import lens, rpi 

# access data
obs_rpi1 = rpi.rpi_timeseries()['rpi1']
obs_rpi1_mean = obs_rpi1.sel(time=slice('1920', '2020')).mean()
obs_rpi1_std = obs_rpi1.sel(time=slice('1920', '2020')).std()
obs_rpi1 = (obs_rpi1-obs_rpi1_mean)/obs_rpi1_std
obs_rpi1_p05 = obs_rpi1.sel(time=slice('1920', '2020')).quantile(0.05)

lens1_cchile = lens.lens1_cchile_gridpoints()
lens1_cchile_mean = lens1_cchile.sel(time=slice('1920', '2020')).mean()
lens1_cchile_std = lens1_cchile.sel(time=slice('1920', '2020')).std()
lens1_cchile = (lens1_cchile-lens1_cchile_mean)/lens1_cchile_std

lens2_cchile = lens.lens2_cchile_gridpoints()
lens2_cchile_mean = lens2_cchile.sel(time=slice('1920', '2020')).mean()
lens2_cchile_std = lens2_cchile.sel(time=slice('1920', '2020')).std()
lens2_cchile = (lens2_cchile-lens2_cchile_mean)/lens2_cchile_std

# visualize data

# basic plot settings
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = True

# create plot
_, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# plot RPI/LENS1 standardized precipitation anomaly vs. time
plt.sca(axs[0])
y = lens1_cchile  # time x run
x = np.tile(lens1_cchile.time.dt.year.values, (lens1_cchile.shape[1], 1)).T

y_mean = y.mean(['run'])
y_mean_time = y_mean.time.dt.year

plt.scatter(x, y, s=10, facecolor='grey',
            edgecolor='grey', label='LENS1', alpha=0.4)
plt.scatter(obs_rpi1.time.dt.year, obs_rpi1, s=10, c='red', label='RPI1')
plt.plot(y_mean_time, y_mean, c='fuchsia', label='LENS1 mean')
plt.axhline(0, c='black', linestyle='--')
plt.axhline(obs_rpi1_p05.values, c='b', ls='--', label='RPI1 5th perc.') 
plt.legend()
plt.ylabel('Precipitation standardized anomaly')
plt.xlabel('Time (yr)')

# plot RPI/LENS2 standardized precipitation anomaly vs. time
plt.sca(axs[1])
y = lens2_cchile  # time x run
x = np.tile(lens2_cchile.time.dt.year.values, (lens2_cchile.shape[1], 1)).T

y_mean = y.mean(['run'])
y_mean_time = y_mean.time.dt.year

plt.scatter(x, y, s=10, facecolor='grey',
            edgecolor='grey', label='LENS2', alpha=0.4)
plt.scatter(obs_rpi1.time.dt.year, obs_rpi1, s=10, c='red', label='RPI1')
plt.plot(y_mean_time, y_mean, c='fuchsia', label='LENS2 mean')
plt.axhline(0, c='black', linestyle='--')
plt.axhline(obs_rpi1_p05.values, c='b', ls='--', label='RPI1 5th perc.')
plt.legend()
plt.ylabel('Precipitation standardized anomaly')
plt.xlabel('Time (yr)')
plt.xlim([1850, 2100])

plt.tight_layout()

# save plot
basedir = '/home/tcarrasco/result/images/png/'
filename = 'HD_rpi_lens_timeseries.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
