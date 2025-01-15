import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_summary(df: pd.DataFrame) -> dict:
    """Generate summary statistics for the dataset."""
    return {
        "columns": df.columns.tolist(),
        "column_types": df.dtypes.to_dict(),
        "basic_stats": df.describe().to_dict(),
    }

def plot_distributions(df: pd.DataFrame):
    """Plot data distributions for numerical features."""
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns
    for col in numeric_cols:
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        plt.show()