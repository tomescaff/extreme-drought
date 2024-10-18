"""RPI/LENS vs. GMST scatter plot.

This script provides a scatter plot of the RPI1 standardized precipitation
anomaly vs. GMST anomaly compared to the LENS1 (upper panel) and LENS2 (lower
panel) standardized precipitation anomalies. All time series are standardized
using their respective mean and standard deviation from 1920 to 2020. The GMST
anomaly is smoothed using a LOWESS filter from the statsmodels package, in the 
case of observations, and took as the ensemble mean in the case of LENS1 and
LENS2.  GMST anomalies are calculated with respecto to 2011-2020.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/result/repo/extreme-drought/')

from utilities import lens, rpi, gmst 

# access data
obs_rpi1 = rpi.rpi_timeseries()['rpi1']
obs_rpi1_mean = obs_rpi1.sel(time=slice('1920', '2020')).mean()
obs_rpi1_std = obs_rpi1.sel(time=slice('1920', '2020')).std()
obs_rpi1 = (obs_rpi1-obs_rpi1_mean)/obs_rpi1_std

lens1_cchile = lens.lens1_cchile_gridpoints()
lens1_cchile_mean = lens1_cchile.sel(time=slice('1920', '2020')).mean()
lens1_cchile_std = lens1_cchile.sel(time=slice('1920', '2020')).std()
lens1_cchile = (lens1_cchile-lens1_cchile_mean)/lens1_cchile_std

lens2_cchile = lens.lens2_cchile_gridpoints()
lens2_cchile_mean = lens2_cchile.sel(time=slice('1920', '2020')).mean()
lens2_cchile_std = lens2_cchile.sel(time=slice('1920', '2020')).std()
lens2_cchile = (lens2_cchile-lens2_cchile_mean)/lens2_cchile_std

obs_tglobal = gmst.annual_global_hadcrut_lowess_from_statsmodel()
obs_tglobal_mean = obs_tglobal.sel(time=slice('2011', '2020')).mean()
obs_tglobal_anom = obs_tglobal - obs_tglobal_mean 

lens1_tglobal = lens.lens1_annual_gmst_ensmean()
lens1_tglobal_mean = lens1_tglobal.sel(time=slice('2011', '2020')).mean()
lens1_tglobal_anom = lens1_tglobal - lens1_tglobal_mean

lens2_tglobal = lens.lens2_annual_gmst_ensmean()
lens2_tglobal_mean = lens2_tglobal.sel(time=slice('2011', '2020')).mean()
lens2_tglobal_anom = lens2_tglobal - lens2_tglobal_mean

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

# plot RPI/LENS1 standardized precipitation anomaly vs. GMST anomaly
plt.sca(axs[0])
y = lens1_cchile  # time x run
x = np.tile(lens1_tglobal_anom.values, (lens1_cchile.shape[1], 1)).T

plt.scatter(x, y, s=10, facecolor='grey',
            edgecolor='grey', label='LENS1', alpha=0.4)
plt.scatter(obs_tglobal_anom, obs_rpi1, s=10, c='red', label='RPI1')
plt.axhline(0, c='black', linestyle='--')
plt.legend()
plt.ylabel('Precipitation standardized anomaly')
plt.xlabel('GMST smoothed anomaly (ºC) [2011-2020]')

# plot RPI/LENS2 standardized precipitation anomaly vs. GMST anomaly
plt.sca(axs[1])
y = lens2_cchile  # time x run
x = np.tile(lens2_tglobal_anom.values, (lens2_cchile.shape[1], 1)).T
plt.scatter(x, y, s=10, facecolor='grey',
            edgecolor='grey', label='LENS2', alpha=0.4)
plt.scatter(obs_tglobal_anom, obs_rpi1, s=10, c='red', label='RPI1')
plt.axhline(0, c='black', linestyle='--')
plt.legend()
plt.ylabel('Precipitation standardized anomaly')
plt.xlabel('GMST smoothed anomaly (ºC) [2011-2020]')

plt.tight_layout()

# save plot
basedir = '/home/tcarrasco/result/images/extreme-drought/'
filename = 'HD_rpi_lens_gmst.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
