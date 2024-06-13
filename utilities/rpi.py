"""RPI data access functions.

This module provides functions to access RPI data from the RPI time
series developed by Juan Pablo Boisier and René Garreaud. It contains
the following functions:

    * rpi_timeseries: Access the RPI time series from 1850 to 2022.
"""

import xarray as xr
import pandas as pd


def rpi_timeseries():
    """Access the RPI time series from 1850 to 2022.

    Returns
    -------
    xr.DataArray
        RPI time series from 1850 to 2022.
        QN from 1866 to 2022.
        RPI1 from 1920 to 2021.
        RPI2 from 1960 to 2021.
    """
    basedir = '/home/tcarrasco/result/data/RPI/'
    filename = 'tseries_QN_RPIs_3037_1850_2022_Rene.txt'
    filepath = basedir + filename
    df = pd.read_csv(filepath, sep='\s+', header=None)  # type: ignore
    dr = pd.date_range(start='1850-01-01', end='2022-12-31', freq='1YS')
    da_qn = xr.DataArray(df.iloc[:, 0].values, coords=[dr], dims=['time'])
    da_rpi1 = xr.DataArray(df.iloc[:, 1].values, coords=[dr], dims=['time'])
    da_rpi2 = xr.DataArray(df.iloc[:, 2].values, coords=[dr], dims=['time'])
    ds = xr.Dataset({'qn': da_qn, 'rpi1': da_rpi1, 'rpi2': da_rpi2})
    return ds
