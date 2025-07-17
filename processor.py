import numpy as np

def preprocess(df):
    df['bp_rp'] = df['bp_mean_mag'] - df['rp_mean_mag']
    df['abs_mag'] = df['phot_g_mean_mag'] - 5 * (np.log10(1000 / df['parallax']) - 1)
    return df

def filter_cmd(df, color_range, mag_range):
    return df[(df['bp_rp'].between(*color_range)) &
              (df['abs_mag'].between(*mag_range))]
