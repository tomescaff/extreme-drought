"""Intensity vs. frequency for corrected data.

This script plots the intensity vs. frequency for corrected data. The corrected 
data is obtained by applying a transfer function to the modeled data. The 
transfer function is obtained by fitting a gamma distribution to the modeled 
data. The intensity is defined as the precipitation deficit with respect to the 
1971-2020 period. The frequency is defined as the percentage of events below a 
given threshold. The HD threshold is defined as the 5th percentile of the 
modeled data for the 1971-2020 period. 

The script also plots the HD frequency and intensity for the corrected data.
"""

import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy import stats
from scipy.stats import gamma

sys.path.append('/home/tcarrasco/result/repo/extreme-drought/')

from utilities import lens, stations  

# access data
obs_qn = stations.yearly_precip_QN_1866_2022()
obs_qn_mean = obs_qn.sel(time=slice('1971', '2020')).mean()
mod_lens2 = lens.lens2_cchile_gridpoints()

obs_qn_1921_2020 = obs_qn.sel(time=slice('1921', '2020')).values
mod_lens2_1921_2020 = np.ravel(mod_lens2.sel(time=slice('1921', '2020')).values)

# transfer function
def transfer(z):
    return gamma.ppf(gamma.cdf(z, *gamma.fit(mod_lens2_1921_2020, floc=0)), 
                     *gamma.fit(obs_qn_1921_2020, floc=0))
transfer_fun = np.vectorize(transfer)

# p -> v
def invcdf_from_mod_ens(mod_data, p, ini_year, end_year):
    nrun = mod_data.run.size
    values = np.zeros((nrun,))
    for run in range(nrun):
        y = mod_data.sel(run=run).sel(time=slice(f'{ini_year}', 
                                                 f'{end_year}'))
        values[run] = np.quantile(y, p)
    return values

# v -> p
def cdf_from_mod_ens(mod_data, v, ini_year, end_year):
    nrun = mod_data.run.size
    probs = np.zeros((nrun,))
    for run in range(nrun):
        print(f'{run+1}/{nrun}')
        y = mod_data.sel(run=run).sel(time=slice(f'{ini_year}', 
                                                 f'{end_year}'))
        ans = 0
        for i in range(100):
            pool = np.random.choice(y, size=(100,), replace=True)
            ans += stats.percentileofscore(pool, v, kind='rank')/100
        probs[run] = ans/100
    return probs

# correct data
shape = mod_lens2.shape
data = np.ravel(mod_lens2.values)
corrected_data = transfer_fun(data)
corrected_data_matrix = corrected_data.reshape(shape)
mod_lens_corrected = xr.DataArray(corrected_data_matrix, 
                                  coords=mod_lens2.coords)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 12

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

_, axs = plt.subplots(2, 2, figsize=(11, 10), 
                      gridspec_kw={'height_ratios': [2, 1], 
                                   'width_ratios': [2, 1]})

probs_mod = np.arange(1, 25, 1)
probs_obs = np.arange(2, 24, 2)

# intensity vs frequency
plt.sca(axs[0, 0])
for init, end, color, name in zip([1921, 1971, 2021], [1970, 2020, 2070], 
                                  ['dodgerblue', 'grey', 'firebrick'], 
                                  ['Past', 'Present', 'Future (SSP3-7.0)']):
    # modeled data
    avg = np.zeros((probs_mod.size,))
    ciup = np.zeros((probs_mod.size,))   
    cilo = np.zeros((probs_mod.size,))

    for i, prob in enumerate(probs_mod):
        print(f'{i+1}/{probs_mod.size}')
        p = (prob-1)/(100-1)
        values = invcdf_from_mod_ens(mod_lens_corrected, p, init, end)
        defs = 100*(1-values/obs_qn_mean.values)
        avg[i] = defs.mean()
        ciup[i] = np.percentile(defs, 75)
        cilo[i] = np.percentile(defs, 25)
        
        if name == 'Present' and prob == 5:
            print(f'{name} [{init}-{end}]: {values.mean()}')
            ac_threshold = values.mean()

    plt.fill_between(probs_mod, cilo, ciup, color=color, alpha=0.1)
    label=f'{name} [{init}-{end}]'
    plt.plot(probs_mod, avg, color=color, linewidth=3, label=label)

plt.title('Intensity vs. frequency')
plt.xlim(-0.5, 25)
plt.ylim(20, 90)
plt.ylabel('Precipitation deficit [wrt. 1971-2020] (%)')
plt.xlabel('Frequency (%)')
plt.axvline(5, color='fuchsia', linestyle='--', label='5% frequency isoline')
plt.legend()

# HD frequency
plt.sca(axs[1, 0])
k = 0
for init, end, color, name in zip([1921, 1971, 2021], [1970, 2020, 2070], 
                                  ['dodgerblue', 'grey', 'firebrick'], 
                                  ['Past', 'Present', 'Future']):
    probs = cdf_from_mod_ens(mod_lens_corrected, ac_threshold, init, end)*100
    plt.boxplot(probs, positions=[k], widths=0.4, patch_artist=True, 
                boxprops=dict(facecolor=color, color=color, alpha=0.1), 
                vert=False, showmeans=True, meanline=True, 
                meanprops=dict(color=color, linewidth=2, linestyle='solid'), 
                medianprops=dict(color=color, linewidth=1, linestyle='--'))               
    k = k+1
plt.xlim(-0.5, 25)
plt.ylim(-1, 3)  
plt.yticks([0, 1, 2], ['Past', 'Present', 'Future'])
plt.title('HD frequency')
plt.xlabel('Frequency (%)')

# HD intensity
plt.sca(axs[0, 1])
k = 0
for init, end, color, name in zip([1921, 1971, 2021], [1970, 2020, 2070], 
                                  ['dodgerblue', 'grey', 'firebrick'], 
                                  ['Past', 'Present', 'Future']):
    p = (5-1)/(100-1)
    values = invcdf_from_mod_ens(mod_lens_corrected, p, init, end)
    defs = 100*(1-values/obs_qn_mean.values)
    plt.boxplot(defs, positions=[k], widths=0.4, patch_artist=True, 
                boxprops=dict(facecolor=color, color=color, alpha=0.1), 
                showmeans=True, meanline=True, 
                meanprops=dict(color=color, linewidth=2, linestyle='solid'),
                medianprops=dict(color=color, linewidth=1, linestyle='--'))           
    k = k+1
plt.xlim(-1,3)
plt.ylim(20, 90)
plt.xticks([0, 1, 2], ['Past', 'Present', 'Future'])
plt.title('HD intensity threshold')
plt.ylabel('Precipitation deficit [wrt. 1971-2020] (%)')

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/extreme-drought/'
filename = 'HD_prob_deficit_corrected.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)

