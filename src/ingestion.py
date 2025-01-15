import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a file."""
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl")
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format!")
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {e}")

def validate_data(df: pd.DataFrame) -> dict:
    """Validate dataset and return summary of issues."""
    return {
        "missing_values": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum(),
        "shape": df.shape,
    }