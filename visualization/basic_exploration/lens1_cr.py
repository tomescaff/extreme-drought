"""LENS1 control run visualization.

This script provides a basic visualization of the LENS1 control run. It shows
a two-panel plot with the yearly precipitation data from 1920 to 2100 in the
first panel and a histogram of the data in the second panel with fitted
distribution curves.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import gamma, norm, lognorm

sys.path.append('/home/tcarrasco/result/repo/extreme-drought/')

from utilities import lens

# access data
pr_cr = lens.lens1_cchile_gridpoints_cr()

# visualize data

# basic plot settings
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# create plot
_, axs = plt.subplots(1, 2, figsize=(10, 5))

# plot yearly precipitation data
plt.sca(axs[0])
plt.bar(pr_cr.time.dt.year, pr_cr)
plt.ylabel('Precipitation (mm/year)')
plt.title('LENS1 CR')

# plot histogram with fitted distribution curves
plt.sca(axs[1])
xmin = 0
xmax = 2500
data = np.ravel(pr_cr.values)
bins = np.linspace(xmin, xmax, 100)
hist, bins = np.histogram(data, bins=bins, density=True)
width = 0.85 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width, edgecolor='k',
    facecolor='grey', alpha=0.7, lw=0.2, label='CR')
plt.xlim([xmin, xmax])
x = np.linspace(xmin, xmax, 100)
fit_gamma = gamma.fit(data, floc=0)
fit_norm = norm.fit(data)
fit_lognorm = lognorm.fit(data)
plt.plot(x, gamma.pdf(x, *fit_gamma), c='r', linewidth=2, label='Gamma')
plt.plot(x, norm.pdf(x, *fit_norm), c='b', linewidth=2, label='Norm')
plt.plot(x, lognorm.pdf(x, *fit_lognorm), c='k', linewidth=2, label='LN')
plt.legend()

plt.tight_layout()

# save plot
basedir = '/home/tcarrasco/result/images/png/'
filename = 'HD_lens1_cr.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)