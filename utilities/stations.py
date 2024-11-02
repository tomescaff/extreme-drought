import pandas as pd
import xarray as xr 

def yearly_precip_QN_1866_2022():
    bd = '/home/tcarrasco/result/data/QN/'
    fn = 'SANTIAGO_QN_1866_2020_RENE_ext_2022.csv'
    df = pd.read_csv(bd+fn, delimiter=",", decimal=".", index_col=None, header=0, parse_dates=['FECHA'])
    months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    df_sum = df[months].sum(axis=1)
    coords = {'time': df['FECHA']}
    da = xr.DataArray(df_sum, coords=coords) 
    return da 