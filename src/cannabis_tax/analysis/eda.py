"""EDA helpers for the notebook workflow."""

from __future__ import annotations

import math
from typing import Iterable

import pandas as pd


def missing_summary(df: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Return a simple missingness summary."""
    selected = list(columns) if columns is not None else list(df.columns)
    summary = pd.DataFrame(
        {
            "variable": selected,
            "non_null": [int(df[col].notna().sum()) for col in selected],
            "missing": [int(df[col].isna().sum()) for col in selected],
            "missing_pct": [df[col].isna().mean() for col in selected],
        }
    )
    return summary.sort_values(["missing_pct", "variable"], ascending=[False, True]).reset_index(
        drop=True
    )


def numeric_summary(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Describe numeric variables in a notebook-friendly format."""
    numeric_df = df.loc[:, list(columns)].apply(pd.to_numeric, errors="coerce")
    return numeric_df.describe().T


def categorical_summary(
    df: pd.DataFrame,
    columns: Iterable[str],
    top_n: int = 10,
) -> pd.DataFrame:
    """Return top categories for each selected variable."""
    frames = []
    for col in columns:
        counts = (
            df[col]
            .astype("string")
            .fillna("<NA>")
            .value_counts(dropna=False)
            .head(top_n)
            .rename_axis("category")
            .reset_index(name="count")
        )
        counts.insert(0, "variable", col)
        frames.append(counts)
    if not frames:
        return pd.DataFrame(columns=["variable", "category", "count"])
    return pd.concat(frames, ignore_index=True)


def plot_histograms(
    df: pd.DataFrame,
    columns: Iterable[str],
    bins: int = 20,
    figsize: tuple[int, int] | None = None,
):
    """Plot histograms for selected numeric columns."""
    import matplotlib.pyplot as plt

    selected = list(columns)
    n_cols = 2
    n_rows = math.ceil(len(selected) / n_cols)
    if figsize is None:
        figsize = (12, max(4, 4 * n_rows))

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for axis, column in zip(axes, selected):
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        axis.hist(series, bins=bins, color="#4C78A8", edgecolor="white")
        axis.set_title(column)
        axis.set_xlabel(column)
        axis.set_ylabel("Frecuencia")

    for axis in axes[len(selected) :]:
        axis.remove()

    fig.tight_layout()
    return fig


def plot_target_rate_by_category(
    df: pd.DataFrame,
    target: str,
    category: str,
    min_count: int = 10,
):
    """Plot the average target rate by category."""
    import matplotlib.pyplot as plt

    plot_df = (
        df[[target, category]]
        .dropna()
        .groupby(category)
        .agg(rate=(target, "mean"), count=(target, "size"))
        .query("count >= @min_count")
        .sort_values("rate", ascending=False)
    )

    ax = plot_df["rate"].plot(kind="bar", color="#2A9D8F", figsize=(8, 4))
    ax.set_title(f"Tasa promedio de {target} por {category}")
    ax.set_ylabel("Promedio")
    ax.set_xlabel(category)
    plt.tight_layout()
    return ax
