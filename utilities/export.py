"""Module for exporting data to various formats."""

import lens
import pandas as pd

def export_lens1_cchile_gridpoints_as_csv():
    """Export the LENS1 yearly precipitation data from 1920 to 2100 over
    the Chilean territory from 30 to 37ºS using selected gridpoints to a
    CSV file.
    """
    basedir = '/home/tcarrasco/result/data/LENS1/pr/csv/'
    filename = 'lens1_cchile_mmyear.csv'
    filepath = basedir + filename
    da = lens.lens1_cchile_gridpoints()
    columns = da.run.values
    index = da.time.dt.year
    data = da.values
    df = pd.DataFrame(data, index=index, columns=columns)
    df.to_csv(filepath, float_format='%.1f')


def export_lens2_cchile_gridpoints_as_csv():
    """Export the LENS2 yearly precipitation data from 1850 to 2100 over
    the Chilean territory from 30 to 37ºS using selected gridpoints to a
    CSV file.
    """
    basedir = '/home/tcarrasco/result/data/LENS2/pr/csv/'
    filename = 'lens2_cchile_mmyear.csv'
    filepath = basedir + filename
    da = lens.lens2_cchile_gridpoints()
    columns = da.run.values
    index = da.time.dt.year
    data = da.values
    df = pd.DataFrame(data, index=index, columns=columns)
    df.to_csv(filepath, float_format='%.1f')
    
    
if __name__ == '__main__':
    export_lens1_cchile_gridpoints_as_csv()
    export_lens2_cchile_gridpoints_as_csv()