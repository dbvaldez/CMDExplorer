import numpy as np
import pandas as pd
from astroquery.gaia import Gaia

def query_region(ra, dec, radius_deg):
    query = f"""
    SELECT source_id, ra, dec, parallax, phot_g_mean_mag,
           bp_mean_mag, rp_mean_mag
    FROM gaiadr3.gaia_source
    WHERE CONTAINS(POINT('ICRS', ra, dec),
                   CIRCLE('ICRS', {ra}, {dec}, {radius_deg})) = 1
    """
    job = Gaia.launch_job(query)
    return job.get_results().to_pandas()

def preprocess(df):
    df['bp_rp'] = df['bp_mean_mag'] - df['rp_mean_mag']
    df['abs_mag'] = df['phot_g_mean_mag'] - 5 * (np.log10(1000 / df['parallax']) - 1)
    return df
