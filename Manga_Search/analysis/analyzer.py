import pandas as pd

def analyze_tags(df: pd.DataFrame, top_n=10):
    tags_series = df["Tags"].dropna().str.split(", ")
    all_tags = [tag for sublist in tags_series for tag in sublist if tag != "N/A"]
    return pd.Series(all_tags).value_counts().head(top_n)

def analyze_authors(df: pd.DataFrame, top_n=10):
    return df["Tác giả"].value_counts().head(top_n)

def analyze_status(df: pd.DataFrame):
    return df["Trạng thái"].value_counts()
