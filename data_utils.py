import pandas as pd
import numpy as np


def get_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def get_categorical_columns(df):

    return df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()


def get_datetime_columns(df):

    return df.select_dtypes(
        include=["datetime"]
    ).columns.tolist()


def get_missing_summary(df):

    missing = df.isnull().sum()

    result = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
        "Missing %": (
            missing.values / len(df) * 100
        ).round(2)
    })

    return result.sort_values(
        "Missing Values",
        ascending=False
    )


def get_duplicate_count(df):

    return int(df.duplicated().sum())


def get_data_quality_score(df):

    if df.empty:
        return 0

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    duplicate_cells = (
        duplicate_rows * df.shape[1]
    )

    problems = (
        missing_cells + duplicate_cells
    )

    score = 100 - (
        problems / total_cells * 100
    )

    return max(
        0,
        round(score)
    )


def get_dataset_summary(df):

    numeric = get_numeric_columns(df)
    categorical = get_categorical_columns(df)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_columns": numeric,
        "categorical_columns": categorical,
        "missing_values": int(
            df.isnull().sum().sum()
        ),
        "duplicate_rows": get_duplicate_count(df),
        "quality_score": get_data_quality_score(df)
    }
