"""CONCEPT: data layer (no AI here).
Load the SMARD CSV and make it queryable with SQL."""
import duckdb
import pandas as pd


def load_smard_csv(path) -> pd.DataFrame:
    """SMARD exports use ';' separators, German numbers ("1.234,56") and '-' for missing values."""
    df = pd.read_csv(path, sep=";", decimal=",", thousands=".", na_values=["-"])
    df = df.rename(columns={df.columns[0]: "ts"})
    df["ts"] = pd.to_datetime(df["ts"], dayfirst=True)
    df = df.drop(columns=[c for c in df.columns[1:] if c.lower().startswith("datum")])  # 'Datum bis'
    # "Deutschland/Luxemburg [€/MWh] Originalauflösungen" -> "deutschland_luxemburg"
    df.columns = ["ts"] + [c.split("[")[0].strip().lower().replace(" ", "_").replace("/", "_")
                           for c in df.columns[1:]]
    return df


def make_database(df: pd.DataFrame) -> duckdb.DuckDBPyConnection:
    """An in-memory DuckDB database. The DataFrame becomes the SQL table 'data'."""
    con = duckdb.connect()
    con.register("data", df)
    return con
