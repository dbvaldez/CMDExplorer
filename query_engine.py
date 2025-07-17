from astroquery.gaia import Gaia
import pandas as pd

Gaia.MAIN_GAIA_SERVER = "https://gea.esac.esa.int"
Gaia.verbose = True

def query_region(ra, dec, radius_deg, row_limit=5000):
    query = f"""
    SELECT TOP {row_limit} source_id, ra, dec, parallax,
           phot_g_mean_mag, bp_mean_mag, rp_mean_mag
    FROM gaiadr3.gaia_source
    WHERE CONTAINS(POINT('ICRS', ra, dec),
                   CIRCLE('ICRS', {ra}, {dec}, {radius_deg})) = 1
    """
    try:
        job = Gaia.launch_job(query)
        return job.get_results().to_pandas()
    except Exception as e:
        print(f"Query failed: {e}")
        return pd.DataFrame()
