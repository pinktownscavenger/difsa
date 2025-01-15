import pytest
from src.ingestion import load_data, validate_data

def test_load_data():
    df = load_data("data/sample.csv")
    assert not df.empty

def test_validate_data():
    df = load_data("data/sample.csv")
    validation = validate_data(df)
    assert validation["missing_values"] >= 0