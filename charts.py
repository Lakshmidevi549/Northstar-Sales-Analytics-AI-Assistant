import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


sns.set_theme(
    style="whitegrid",
    palette="deep"
)


def histogram(df, column, bins):

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    sns.histplot(
        df[column].dropna(),
        bins=bins,
        kde=True,
        color="#2563eb",
        ax=ax
    )

    ax.set_title(
        f"Distribution of {column}",
        fontsize=17,
        fontweight="bold"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    fig.tight_layout()

    return fig


def boxplot(df, column):

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    sns.boxplot(
        x=df[column],
        color="#60a5fa",
        ax=ax
    )

    ax.set_title(
        f"Outlier Analysis — {column}",
        fontsize=17,
        fontweight="bold"
    )

    ax.set_xlabel(column)

    fig.tight_layout()

    return fig


def countplot(df, column):

    values = (
        df[column]
        .value_counts()
        .head(20)
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    sns.barplot(
        x=values.index.astype(str),
        y=values.values,
        color="#2563eb",
        ax=ax
    )

    ax.set_title(
        f"Category Frequency — {column}",
        fontsize=17,
        fontweight="bold"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    ax.tick_params(
        axis="x",
        rotation=45
    )

    fig.tight_layout()

    return fig


def scatterplot(df, x, y):

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    sns.scatterplot(
        data=df,
        x=x,
        y=y,
        alpha=0.65,
        color="#2563eb",
        ax=ax
    )

    ax.set_title(
        f"{y} vs {x}",
        fontsize=17,
        fontweight="bold"
    )

    fig.tight_layout()

    return fig


def lineplot(df, column):

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        df[column].values,
        color="#2563eb",
        linewidth=2
    )

    ax.set_title(
        f"Trend — {column}",
        fontsize=17,
        fontweight="bold"
    )

    ax.set_xlabel("Record")
    ax.set_ylabel(column)

    fig.tight_layout()

    return fig


def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include="number"
    )

    corr = numeric_df.corr()

    fig, ax = plt.subplots(
        figsize=(11, 8)
    )

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        linewidths=0.5,
        ax=ax
    )

    ax.set_title(
        "Feature Correlation Matrix",
        fontsize=17,
        fontweight="bold"
    )

    fig.tight_layout()

    return fig
