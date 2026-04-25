from pathlib import Path
import pandas as pd


def extract_csv(path: str | Path) -> pd.DataFrame:
    """Read raw service request data from a CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find input file: {csv_path}")
    return pd.read_csv(csv_path)
