"""LENS data access functions.

This module provides functions to access LENS posprocessed data. It  
contains the following functions:

    * lens1_cchile_gridpoints: Access the LENS1 precipitation data from 1920
        to 2100. 
        
    * lens1_cchile_gridpoints_cr: Access the LENS1 precipitation data from 
        the control run.
    
    * lens2_cchile_gridpoints: Access the LENS2 precipitation data from 1850
        to 2100.
        
    * lens1_annual_gmst_ensmean: Access the LENS1 40-member ensemble-mean 
        annual GMST data from 1920 to 2100.
    
    * lens2_annual_gmst_ensmean: Access the LENS2 100-member ensemble-mean
        annual GMST data from 1850 to 2100.
"""

import xarray as xr
import pandas as pd
import numpy as np

def lens1_cchile_gridpoints():
    """Access the LENS1 yearly precipitation data from 1920 to 2100 over
    the Chilean territory from 30 to 37ºS using selected gridpoints.

    Returns
    -------
    xr.DataArray
        LENS1 yearly precipitation data from 1920 to 2100. [time x run]
    """
    basedir = '/home/tcarrasco/result/data/LENS1/pr/final/'
    filename = 'CESM1_LENS_pr_mon_1920_2100_chile_1deg_40m.nc'
    filepath = basedir + filename
    ds = xr.open_dataset(filepath)
    da = ds['pr'].sel(lat=slice(-37, -30), lon=288.75).mean(['lat']).squeeze()
    da = da*1e-3*3600*24*1000  # da in monthly mean precip flux in mm/day
    dr = pd.date_range('1920', '2100', freq='1D')
    one_per_day = xr.DataArray(np.ones((dr.size,)), coords=[dr], dims=['time']) # type: ignore
    days_per_month = one_per_day.resample(time='1MS').sum(skipna=False)
    da_mm_month = da*days_per_month  # mm/month
    da_mm_year = da_mm_month.resample(time='1YS').sum(skipna=False)  # mm/year
    return da_mm_year


def lens1_cchile_gridpoints_cr():
    """Access the LENS1 yearly precipitation data from the control run over
    the Chilean territory from 30 to 37ºS using selected gridpoints.

    Returns
    -------
    xr.DataArray
        LENS1 yearly precipitation data from 401 to 2200. [time x run]
    """
    basedir = '/home/tcarrasco/result/data/LENS1/pr/final/'
    filename = 'CESM1_LENS_pr_year_0400_2200_global_1deg_cr.nc'
    filepath = basedir + filename
    ds = xr.open_dataset(filepath)
    da = ds['PRECC']
    da = da.sel(lat=slice(-37, -30), lon=288.75).mean(['lat']).squeeze()
    # da is yearly mean precip flux in m/s
    da_mm_year = da*3600*24*1000*365 # m/s -> mm/year 
    return da_mm_year


def lens2_cchile_gridpoints():
    """Access the LENS2 yearly precipitation data from 1850 to 2100 over
    the Chilean territory from 30 to 37ºS using selected gridpoints.

    Returns
    -------
    xr.DataArray
        LENS2 yearly precipitation data from 1850 to 2100. [time x run]
    """
    basedir = '/home/tcarrasco/result/data/LENS2/pr/final/'
    filename = 'CESM2_LENS_pr_mon_1850_2100_chile_1deg_100m_NOAA.nc'
    filepath = basedir + filename
    ds = xr.open_dataset(filepath)
    da = ds['pr'].sel(lat=slice(-37, -30), lon=288.75).mean(['lat']).squeeze()
    da = da*1e-3*3600*24*1000  # da in monthly mean precip flux in mm/day
    dr = pd.date_range('1850', '2100', freq='1D')
    one_per_day = xr.DataArray(np.ones((dr.size,)), coords=[dr], dims=['time']) # type: ignore
    days_per_month = one_per_day.resample(time='1MS').sum(skipna=False)
    da_mm_month = da*days_per_month  # mm/month
    da_mm_year = da_mm_month.resample(time='1YS').sum(skipna=False)  # mm/year
    return da_mm_year


def lens1_annual_gmst_ensmean():
    """Access the LENS1 40-member ensemble-mean annual GMST data from 1920
    to 2100.
    
    Returns
    -------
    xr.DataArray
        LENS1 40-member ensemble-mean annual GMST data from 1920 to 2100.
    """
    basedir = '/home/tcarrasco/result/data/GMST/'
    filename = 'tas_CESM1-CAM5_LENS_ensmean_spamean_yearmean.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tas'] - 273.15
    return da


def lens2_annual_gmst_ensmean():
    """Access the LENS2 100-member ensemble-mean annual GMST data from 1850
    to 2100.
    
    Returns
    -------
    xr.DataArray
        LENS2 100-member ensemble-mean annual GMST data from 1850 to 2100.
    """
    basedir = '/home/tcarrasco/result/data/GMST/'
    filename = 'tas_CESM2_LENS_ensmean_spamean_yearmean.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tas'] - 273.15
    return da