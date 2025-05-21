import pandas as pd
import os
import streamlit as st

def get_data_path(filename):
    """Tries to find the data file in common relative locations."""
    path_option1 = os.path.join('data', filename)  # If running from project root
    path_option2 = os.path.join('../data', filename)  # If running from app/
    if os.path.exists(path_option1):
        return path_option1
    elif os.path.exists(path_option2):
        return path_option2
    else:
        return None

@st.cache_data(ttl=3600)
def load_cleaned_data(country_name_full):
    """
    Loads a single cleaned dataset for a given country.
    """
    file_map = {
        'Benin (Malanville)': 'benin_clean.csv',
        'Sierra Leone (Bumbuna)': 'sierra_leone_clean.csv',
        'Togo (Dapaong QC)': 'togo_clean.csv'
    }
    
    filename_short = file_map.get(country_name_full)
    if not filename_short:
        st.error(f"No file mapping found for country: {country_name_full}")
        return pd.DataFrame()

    file_path = get_data_path(filename_short)
    
    if file_path and os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if 'Timestamp' in df.columns:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df['Country'] = country_name_full
            st.write(f"Loaded {filename_short} with {len(df)} rows and columns: {', '.join(df.columns)}")
            return df
        except Exception as e:
            st.error(f"Error loading {filename_short}: {e}")
            return pd.DataFrame()
    else:
        st.error(f"File not found: {filename_short} in data/. Please ensure it exists in the data/ directory.")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_all_cleaned_data(countries_to_load):
    """Loads and concatenates cleaned data for selected countries."""
    all_dfs = []
    for country_name in countries_to_load:
        df = load_cleaned_data(country_name)
        if not df.empty:
            all_dfs.append(df)
    
    if not all_dfs:
        st.error("No data loaded for any selected countries.")
        return pd.DataFrame()
    combined_df = pd.concat(all_dfs, ignore_index=True)
    st.write(f"Combined data with {len(combined_df)} rows.")
    return combined_df