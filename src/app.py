import streamlit as st
import pandas as pd
from ingestion import validate_data
from exploration import generate_summary, plot_distributions

st.title("DIFSA: Data Insight and Feature Selection Assistant")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel, JSON):", type=["csv", "xlsx", "json"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file format!")
            st.stop()
        
        st.success(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        # Show the dataset
        st.subheader("Preview of Dataset")
        st.dataframe(df.head())
        
        # Validate dataset
        st.subheader("Validation Results")
        validation_results = validate_data(df)
        st.write(f"Missing Values: {validation_results['missing_values']}")
        st.write(f"Duplicates: {validation_results['duplicates']}")

        # Summary statistics
        st.subheader("Dataset Summary")
        summary = generate_summary(df)
        st.json(summary["basic_stats"])

        # Visualizations
        st.subheader("Data Visualizations")
        st.write("Numeric feature distributions:")
        plot_distributions(df)
    
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
