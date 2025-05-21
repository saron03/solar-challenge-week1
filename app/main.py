import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_all_cleaned_data

# --- Page Configuration ---
st.set_page_config(
    page_title="MoonLight Solar Analysis Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Data ---
AVAILABLE_COUNTRIES = ['Benin (Malanville)', 'Sierra Leone (Bumbuna)', 'Togo (Dapaong QC)']

st.sidebar.title("🌍 Country & Data Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=AVAILABLE_COUNTRIES,
    default=AVAILABLE_COUNTRIES
)

if not selected_countries:
    st.warning("Please select at least one country from the sidebar to view data.")
    st.stop()

combined_df = load_all_cleaned_data(selected_countries)

# Debug data loading
if combined_df.empty:
    st.error("Failed to load data for the selected countries. Check if CSV files (benin_clean.csv, sierra_leone.csv, togo_clean.csv) exist in 'data/' and have columns like Timestamp, GHI, DNI, etc.")
    st.stop()
else:
    st.write(f"Data loaded successfully with {len(combined_df)} rows.")
    st.write("Columns in dataset: " + ", ".join(combined_df.columns))

# Filter for daytime data
daytime_df = combined_df[combined_df['GHI'] > 10].copy()
if daytime_df.empty and not combined_df.empty:
    st.warning("No data points with GHI > 10 W/m² found. Using all data for plots.")
    daytime_df_for_plots = combined_df.copy()
else:
    daytime_df_for_plots = daytime_df

# --- Main Dashboard Title ---
st.title("☀️ MoonLight Energy Solutions - Solar Investment Dashboard")
st.markdown("Comparative analysis of solar potential across selected regions.")

# --- Section 1: Irradiance Comparison ---
st.header("📊 Solar Irradiance Comparison (Daytime GHI > 10 W/m²)")
if not daytime_df_for_plots.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("GHI Distribution")
        if 'GHI' in daytime_df_for_plots.columns:
            fig_ghi_box = px.box(daytime_df_for_plots, x='Country', y='GHI', color='Country',
                                 title="Global Horizontal Irradiance (GHI)", labels={'GHI': 'GHI (W/m²)'},
                                 points=False)
            fig_ghi_box.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_ghi_box, use_container_width=True)
        else:
            st.write("GHI column not found in data.")

    with col2:
        st.subheader("DNI Distribution")
        if 'DNI' in daytime_df_for_plots.columns:
            fig_dni_box = px.box(daytime_df_for_plots, x='Country', y='DNI', color='Country',
                                 title="Direct Normal Irradiance (DNI)", labels={'DNI': 'DNI (W/m²)'},
                                 points=False)
            fig_dni_box.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_dni_box, use_container_width=True)
        else:
            st.write("DNI column not found in data.")

else:
    st.write("No data available for irradiance comparison.")

# --- Section 2: Top Regions Table ---
st.header("🏆 Top Regions Summary (Daytime Averages)")
if not daytime_df_for_plots.empty:
    metrics_for_summary = ['GHI', 'DNI', 'DHI', 'Tamb', 'TModA']
    available_metrics = [m for m in metrics_for_summary if m in daytime_df_for_plots.columns]

    if available_metrics:
        agg_dict = {metric: ['mean', 'median', 'std'] for metric in available_metrics}
        summary_table_multi_index = daytime_df_for_plots.groupby('Country').agg(agg_dict)
        
        if not summary_table_multi_index.empty:
            summary_table = summary_table_multi_index.copy()
            summary_table.columns = ['_'.join(col).strip() for col in summary_table.columns.values]
            summary_table = summary_table.reset_index()
            
            st.markdown("Mean, Median, and Standard Deviation of key metrics during daytime (GHI > 10 W/m²).")
            numeric_columns = summary_table.select_dtypes(include=['float', 'int']).columns
            formatted_table = summary_table.copy()
            for col in numeric_columns:
                formatted_table[col] = formatted_table[col].apply(lambda x: f"{x:.2f}")
            
            sort_metric = 'GHI_mean'
            if sort_metric in summary_table.columns:
                st.dataframe(formatted_table.sort_values(by=sort_metric, ascending=False))
            else:
                st.dataframe(formatted_table)
        else:
            st.write("Summary table could not be generated.")
    else:
        st.write("No suitable metrics available for the summary table.")
else:
    st.write("No data available to generate the summary table.")

# --- Section 3: Time Series Viewer ---
st.header("🕰️ Time Series Viewer")
if not combined_df.empty and 'Timestamp' in combined_df.columns:
    selected_metric_ts = st.selectbox(
        "Select Metric for Time Series:",
        options=[col for col in combined_df.columns if pd.api.types.is_numeric_dtype(combined_df[col]) and col not in ['Country', 'Cleaning'] and not col.endswith('_zscore')],
        index=0
    )

    if selected_metric_ts and selected_metric_ts in combined_df.columns:
        df_to_plot_ts = combined_df[['Timestamp', 'Country', selected_metric_ts]].copy()
        fig_ts = px.line(df_to_plot_ts, x='Timestamp', y=selected_metric_ts, color='Country',
                         title=f"{selected_metric_ts} Over Time",
                         labels={selected_metric_ts: f'{selected_metric_ts} (Units)'})
        st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.write(f"Metric '{selected_metric_ts}' not available for time series plot.")
else:
    st.write("Timestamp column or data not available for time series viewer.")

# --- Footer ---
st.markdown("---")
st.markdown("Dashboard developed for MoonLight Energy Solutions")