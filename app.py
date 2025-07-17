import streamlit as st
import plotly.express as px
from utils import query_region, preprocess

st.set_page_config(page_title="CMDExplorer", layout="wide")
st.title("Color-Magnitude Diagram Explorer")
st.markdown("Explore stellar populations by region using live Gaia data.")

# Region selector
ra = st.number_input("RA (deg)", value=56.75)
dec = st.number_input("Dec (deg)", value=24.12)
radius = st.slider("Search Radius (°)", 0.1, 5.0, 1.0)

if st.button("Fetch Data"):
    with st.spinner("Querying Gaia Archive..."):
        df = preprocess(query_region(ra, dec, radius))
        st.success(f"{len(df):,} stars loaded!")

        # Filters
        mag_min, mag_max = st.slider("Absolute Magnitude", -5.0, 15.0, (-5.0, 15.0))
        color_min, color_max = st.slider("BP-RP Color", -0.5, 3.0, (-0.5, 3.0))

        filtered_df = df[df['abs_mag'].between(mag_min, mag_max) &
                         df['bp_rp'].between(color_min, color_max)]

        fig = px.scatter(
            filtered_df, x="bp_rp", y="abs_mag",
            hover_data=["source_id", "ra", "dec", "parallax"],
            title="Gaia CMD",
            labels={"bp_rp": "BP-RP Color", "abs_mag": "Absolute Magnitude"},
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
