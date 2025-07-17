import streamlit as st
import plotly.express as px
from query_engine import query_region
from processor import preprocess, filter_cmd
from config import targets

st.set_page_config(page_title="CMDExplorer", layout="wide")
st.title("Plug-and-Play CMD Explorer")

target = st.selectbox("Choose Region", options=list(targets.keys()))
params = targets[target]

if st.button("Load Stars"):
    with st.spinner("Fetching Gaia stars..."):
        df_raw = query_region(params['ra'], params['dec'], params['radius'])
        if df_raw.empty:
            st.error("No stars found. Try another region or smaller radius.")
        else:
            df = preprocess(df_raw)
            st.success(f"{len(df):,} stars loaded.")

            color_range = st.slider("BP-RP Color Range", -0.5, 3.0, (-0.5, 3.0))
            mag_range = st.slider("Absolute Magnitude Range", -5.0, 15.0, (-5.0, 15.0))
            df_filtered = filter_cmd(df, color_range, mag_range)

            fig = px.scatter(df_filtered, x='bp_rp', y='abs_mag',
                             hover_data=["source_id", "ra", "dec"],
                             labels={'bp_rp': 'Color (BP-RP)', 'abs_mag': 'Absolute Magnitude'},
                             title=f"{target} CMD")
            fig.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
