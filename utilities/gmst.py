"""Global Mean Surface Temperature (GMST) data processing utilities.

This module provides functions to load and process GMST data from
different sources. It contains the following functions:

    * annual_global_gistemp: Load the annual GMST data from the GISTEMP 
        dataset from 1880 to 2022.
    
    * annual_global_gistemp_lowess_from_csv: Load the annual GMST data 
        from the GISTEMP dataset from 1880 to 2022 with a 5-year lowess 
        smoothing computed by the GISS-NASA team.
        
    * annual_global_gistemp_lowess_from_statsmodel: Load the annual GMST
        data from the GISTEMP dataset from 1880 to 2022 with a 5-year
        lowess smoothing computed by the statsmodels library.
        
    * annual_global_hadcrut: Load the annual GMST data from the HadCRUT
        dataset from 1850 to 2022.
        
    * annual_global_hadcrut_lowess_from_statsmodel: Load the annual GMST
        data from the HadCRUT dataset from 1850 to 2022 with a 5-year
        lowess smoothing computed by the statsmodels library.
"""

from os.path import join
import pandas as pd
import xarray as xr
import statsmodels.api as sm


def annual_global_gistemp():
    """Load the annual GMST data from the GISTEMP dataset from 1880 to 
    2022.

    Returns
    -------
    xr.DataArray
        Annual GMST data from 1880 to 2022.
    """
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'GISTEMP_year_smooth_2022.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, skiprows=1, parse_dates={'time': ['Year']})
    df = df.set_index('time')
    return df['No_Smoothing'].to_xarray().astype(float)


def annual_global_gistemp_lowess_from_csv():
    """Load the annual GMST data from the GISTEMP dataset from 1880 to
    2022 with a 5-year lowess smoothing computed by the GISS-NASA team.
    
    Returns
    -------
    xr.DataArray
        Annual GMST data from 1880 to 2022 with a 5-year lowess smoothing.
    """
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'GISTEMP_year_smooth_2022.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, skiprows=1, parse_dates={'time': ['Year']})
    df = df.set_index('time')
    return df['Lowess(5)'].to_xarray().astype(float)


def annual_global_gistemp_lowess_from_statsmodel():
    """Load the annual GMST data from the GISTEMP dataset from 1880 to
    2022 with a 5-year lowess smoothing computed by the statsmodels library.
    
    Returns
    -------
    xr.DataArray
        Annual GMST data from 1880 to 2022 with a 5-year lowess smoothing.
    """
    gmst = annual_global_gistemp()
    n = gmst.size
    smooth_gmst = sm.nonparametric.lowess(
        gmst.values, gmst.time.dt.year, frac=10./n)
    da = xr.DataArray(smooth_gmst[:, 1], coords=[gmst.time], dims=['time'])
    return da


def annual_global_hadcrut():
    """Load the annual GMST data from the HadCRUT dataset from 1850 to
    2022.
    
    Returns
    -------
    xr.DataArray
        Annual GMST data from 1850 to 2022.
    """
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'HadCRUT.5.0.1.0.analysis.summary_series.global.annual.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, parse_dates={'time': ['Time']})
    df.rename(columns={'Time': 'time',
                       'Anomaly (deg C)': 'anom',
                       'Lower confidence limit (2.5%)': 'lower',
                       'Upper confidence limit (97.5%)': 'upper'},
              inplace=True)
    df = df.set_index('time')
    ds = df.to_xarray().astype(float)
    ds = ds - ds.sel(time=slice('1850', '1900')).mean('time')
    ds = ds.sel(time=slice('1850', '2022'))
    return ds


def annual_global_hadcrut_lowess_from_statsmodel():
    """Load the annual GMST data from the HadCRUT dataset from 1850 to
    2022 with a 5-year lowess smoothing computed by the statsmodels library.
    
    Returns
    -------
    xr.DataArray
        Annual GMST data from 1850 to 2022 with a 5-year lowess smoothing.
    """
    gmst = annual_global_hadcrut()['anom']
    n = gmst.size
    smooth_gmst = sm.nonparametric.lowess(
        gmst.values, gmst.time.dt.year, frac=10./n)
    da = xr.DataArray(smooth_gmst[:, 1], coords=[gmst.time], dims=['time'])
    return da