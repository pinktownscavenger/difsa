import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import skew, kurtosis

def generate_summary(df: pd.DataFrame) -> dict:
    """Generate summary statistics for the dataset."""
    summary = {}

    # Identify binary columns (1/0 values)
    binary_columns = [col for col in df.columns if set(df[col].dropna().unique()).issubset({0, 1})]

    # Identify columns that are likely to be serial numbers
    serial_like_columns = [
        col for col in df.select_dtypes(include=[np.number]).columns
        if df[col].nunique() == len(df[col]) and (df[col].dropna().diff().dropna() == 1).all()
    ]

    # Filter out serial and binary columns for summary statistics
    summary_columns = [col for col in df.columns if col not in serial_like_columns + binary_columns]

    # Only consider numeric columns for these additional stats
    numeric_columns = df[summary_columns].select_dtypes(include=[np.number]).columns
    summary_stats = df[numeric_columns].describe().T  # Transpose for a table-like view

    # Add additional stats to the summary
    summary_stats["unique"] = df[numeric_columns].nunique()
    summary_stats["mode"] = df[numeric_columns].mode().iloc[0]
    summary_stats["skewness"] = df[numeric_columns].apply(lambda x: skew(x.dropna()))
    summary_stats["kurtosis"] = df[numeric_columns].apply(lambda x: kurtosis(x.dropna()))
    summary_stats["IQR"] = df[numeric_columns].apply(lambda x: x.quantile(0.75) - x.quantile(0.25))

    return {
        "columns": df.columns.tolist(),
        "column_types": df.dtypes.to_dict(),
        "binary_columns": binary_columns,
        "summary_stats": summary_stats.to_dict(),
    }

def plot_distributions(df: pd.DataFrame):
    """Plot data distributions for numerical features."""
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        st.pyplot(plt)
        plt.close()