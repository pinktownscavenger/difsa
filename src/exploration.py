import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import skew, kurtosis

def extract_boolean_columns(df: pd.DataFrame) -> dict:
    """Identify binary columns (1/0 values) and return min/max values."""
    boolean_columns = {
        col: {
            "min": int(df[col].min()),
            "max": int(df[col].max())
        }
        for col in df.columns if set(df[col].dropna().unique()).issubset({0, 1})
    }
    return boolean_columns

def extract_sequential_columns(df: pd.DataFrame) -> dict:
    """Identify columns that contain unique sequential-like identifiers."""
    sequential_columns = {
        col: {
            "total": df[col].count(),
            "unique": df[col].nunique()
        }
        for col in df.select_dtypes(include=[np.number]).columns
        if df[col].nunique() == len(df[col])  # Check if all values are unique
    }
    return sequential_columns

def filter_df(df, sequential_columns, boolean_columns):
    sequential_cols = list(sequential_columns.keys())
    boolean_cols = list(boolean_columns.keys())

    summary_columns = [col for col in df.columns if col not in sequential_cols + boolean_cols]
    return summary_columns

def format_and_addi_stats(df,summary_columns):
    if not summary_columns:
        return "No valid numeric columns for summary statistics."
    
    numeric_columns = df[summary_columns].select_dtypes(include=[np.number]).columns

    if numeric_columns.empty:
        return "No numeric columns available after filtering."
    
    summary_stats = df[numeric_columns].describe().T  # Transpose for a table-like view
    summary_stats = summary_stats.drop(labels=['25%', '50%', '75%'], axis=1)

    summary_stats["unique"] = df[numeric_columns].nunique()
    summary_stats["mode"] = df[numeric_columns].mode().iloc[0]
    summary_stats["skewness"] = df[numeric_columns].apply(lambda x: skew(x.dropna()))
    summary_stats["kurtosis"] = df[numeric_columns].apply(lambda x: kurtosis(x.dropna()))
    summary_stats["IQR"] = df[numeric_columns].apply(lambda x: x.quantile(0.75) - x.quantile(0.25))

    return summary_stats

def generate_summary(df: pd.DataFrame) -> dict:
    """Generate summary statistics for the dataset."""
    summary = {}

    boolean_columns = extract_boolean_columns(df)
    sequential_columns = extract_sequential_columns(df)

    summary_columns = filter_df(df,sequential_columns,boolean_columns)
    summary_stats = format_and_addi_stats(df,summary_columns)

    return {
        "boolean_columns": boolean_columns,
        "sequential_columns": sequential_columns,
        "summary_stats": summary_stats
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