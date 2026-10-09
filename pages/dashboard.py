import streamlit as st

from data_utils import get_dataset_summary


def show_dashboard(df):

    st.title("🏠 Dashboard")

    st.caption(
        "High-level overview of your dataset."
    )

    # ============================================================
    # CHECK DATASET
    # ============================================================

    if df is None or df.empty:

        st.warning(
            "📂 Please upload a dataset from the sidebar."
        )

        return

    # ============================================================
    # DATASET SUMMARY
    # ============================================================

    summary = get_dataset_summary(df)

    # ============================================================
    # KPI CARDS
    # ============================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            label="Total Rows",
            value=f"{summary['rows']:,}"
        )

    with c2:

        st.metric(
            label="Total Columns",
            value=f"{summary['columns']:,}"
        )

    with c3:

        st.metric(
            label="Missing Values",
            value=f"{summary['missing_values']:,}"
        )

    with c4:

        st.metric(
            label="Data Quality",
            value=f"{summary['quality_score']}%"
        )

    st.divider()

    # ============================================================
    # DATASET PREVIEW
    # ============================================================

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.divider()

    # ============================================================
    # COLUMN TYPES
    # ============================================================

    st.subheader("🧬 Column Types")

    c1, c2 = st.columns(2)

    # ============================================================
    # NUMERIC COLUMNS
    # ============================================================

    with c1:

        st.markdown("### 🔢 Numeric Columns")

        numeric_columns = summary.get(
            "numeric_columns",
            []
        )

        if numeric_columns:

            for col in numeric_columns:

                st.write(f"• {col}")

        else:

            st.info("No numeric columns found.")

    # ============================================================
    # CATEGORICAL COLUMNS
    # ============================================================

    with c2:

        st.markdown("### 🔤 Categorical Columns")

        categorical_columns = summary.get(
            "categorical_columns",
            []
        )

        if categorical_columns:

            for col in categorical_columns:

                st.write(f"• {col}")

        else:

            st.info("No categorical columns found.")

