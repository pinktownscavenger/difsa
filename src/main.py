import sys
from ingestion import load_data, validate_data
from exploration import generate_summary, plot_distributions

def main(file_path):
    print("Loading dataset...")
    try:
        df = load_data(file_path)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    print("\nValidating dataset...")
    validation_results = validate_data(df)
    print(f"Missing Values: {validation_results['missing_values']}")
    print(f"Duplicates: {validation_results['duplicates']}")

    print("\nGenerating dataset summary...")
    summary = generate_summary(df)
    print("Columns:", summary["columns"])
    print("Column Types:", summary["column_types"])
    print("Basic Stats:", summary["basic_stats"])

    print("\nVisualizing data distributions...")
    plot_distributions(df)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)
