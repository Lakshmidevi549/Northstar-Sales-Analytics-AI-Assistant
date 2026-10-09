import streamlit as st

from data_utils import (
    get_missing_summary,
    get_duplicate_count,
    get_data_quality_score
)


def show_data_analysis():

    df = st.session_state.df

    st.title("🔍 Data Analysis")

    if df is None:

        st.warning(
            "Upload a dataset from the sidebar first."
        )

        return

    tabs = st.tabs(
        [
            "📋 Overview",
            "🧬 Columns",
            "⚠️ Missing Values",
            "♻️ Duplicates",
            "📊 Statistics"
        ]
    )

    # ========================================================
    # OVERVIEW
    # ========================================================

    with tabs[0]:

        st.subheader("Dataset Overview")

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        st.write(
            f"Shape: **{df.shape[0]:,} rows × "
            f"{df.shape[1]:,} columns**"
        )

    # ========================================================
    # COLUMNS
    # ========================================================

    with tabs[1]:

        st.subheader("Column Information")

        info = df.dtypes.astype(str)

        table = []

        for column in df.columns:

            table.append(
                {
                    "Column": column,
                    "Data Type": str(
                        df[column].dtype
                    ),
                    "Non-Null": int(
                        df[column].notna().sum()
                    ),
                    "Missing": int(
                        df[column].isna().sum()
                    ),
                    "Unique": int(
                        df[column].nunique()
                    )
                }
            )

        st.dataframe(
            table,
            use_container_width=True
        )

    # ========================================================
    # MISSING
    # ========================================================

    with tabs[2]:

        st.subheader(
            "Missing Value Analysis"
        )

        missing = get_missing_summary(df)

        missing = missing[
            missing["Missing Values"] > 0
        ]

        if missing.empty:

            st.success(
                "🎉 No missing values found!"
            )

        else:

            st.dataframe(
                missing,
                use_container_width=True
            )

            st.bar_chart(
                missing.set_index(
                    "Column"
                )["Missing %"]
            )

    # ========================================================
    # DUPLICATES
    # ========================================================

    with tabs[3]:

        duplicate_count = (
            get_duplicate_count(df)
        )

        st.subheader(
            "Duplicate Row Analysis"
        )

        if duplicate_count == 0:

            st.success(
                "No duplicate rows found."
            )

        else:

            st.warning(
                f"{duplicate_count:,} duplicate rows found."
            )

    # ========================================================
    # STATISTICS
    # ========================================================

    with tabs[4]:

        st.subheader(
            "Statistical Summary"
        )

        st.dataframe(
            df.describe(
                include="all"
            ).T,
            use_container_width=True
        )
