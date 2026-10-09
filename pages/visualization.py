import streamlit as st
import matplotlib.pyplot as plt

from data_utils import (
    get_numeric_columns,
    get_categorical_columns
)

from charts import (
    histogram,
    boxplot,
    countplot,
    scatterplot,
    lineplot,
    correlation_heatmap
)


def show_visualization():

    df = st.session_state.df

    st.title("📈 Visualization Studio")

    if df is None:

        st.warning(
            "Upload a dataset from the sidebar first."
        )

        return

    numeric_columns = get_numeric_columns(df)

    categorical_columns = get_categorical_columns(df)

    chart_type = st.selectbox(
        "Choose a visualization",
        [
            "Histogram",
            "Boxplot",
            "Countplot",
            "Scatter Plot",
            "Line Chart",
            "Correlation Heatmap"
        ]
    )

    st.divider()

    # ========================================================
    # HISTOGRAM
    # ========================================================

    if chart_type == "Histogram":

        st.subheader(
            "📊 Distribution Analysis"
        )

        if not numeric_columns:

            st.error(
                "No numeric columns found."
            )

            return

        column = st.selectbox(
            "Numeric column",
            numeric_columns
        )

        bins = st.slider(
            "Bins",
            5,
            100,
            25
        )

        if st.button(
            "Generate Chart",
            type="primary"
        ):

            fig = histogram(
                df,
                column,
                bins
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

    # ========================================================
    # BOXPLOT
    # ========================================================

    elif chart_type == "Boxplot":

        st.subheader(
            "📦 Outlier Analysis"
        )

        if not numeric_columns:

            st.error(
                "No numeric columns found."
            )

            return

        column = st.selectbox(
            "Numeric column",
            numeric_columns
        )

        if st.button(
            "Generate Chart",
            type="primary"
        ):

            fig = boxplot(
                df,
                column
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

    # ========================================================
    # COUNTPLOT
    # ========================================================

    elif chart_type == "Countplot":

        st.subheader(
            "🔢 Category Distribution"
        )

        if not categorical_columns:

            st.error(
                "No categorical columns found."
            )

            return

        column = st.selectbox(
            "Categorical column",
            categorical_columns
        )

        if st.button(
            "Generate Chart",
            type="primary"
        ):

            fig = countplot(
                df,
                column
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

    # ========================================================
    # SCATTER
    # ========================================================

    elif chart_type == "Scatter Plot":

        st.subheader(
            "🔵 Relationship Analysis"
        )

        if len(numeric_columns) < 2:

            st.error(
                "At least two numeric columns are required."
            )

            return

        c1, c2 = st.columns(2)

        with c1:

            x = st.selectbox(
                "X-axis",
                numeric_columns,
                key="scatter_x"
            )

        with c2:

            y = st.selectbox(
                "Y-axis",
                numeric_columns,
                key="scatter_y"
            )

        if st.button(
            "Generate Chart",
            type="primary"
        ):

            fig = scatterplot(
                df,
                x,
                y
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

    # ========================================================
    # LINE
    # ========================================================

    elif chart_type == "Line Chart":

        st.subheader(
            "📈 Trend Analysis"
        )

        if not numeric_columns:

            st.error(
                "No numeric columns found."
            )

            return

        column = st.selectbox(
            "Numeric column",
            numeric_columns
        )

        if st.button(
            "Generate Chart",
            type="primary"
        ):

            fig = lineplot(
                df,
                column
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

    # ========================================================
    # CORRELATION
    # ========================================================

    elif chart_type == "Correlation Heatmap":

        st.subheader(
            "🔥 Feature Correlation"
        )

        if len(numeric_columns) < 2:

            st.error(
                "At least two numeric columns are required."
            )

            return

        st.caption(
            "The heatmap automatically uses all numeric columns."
        )

        if st.button(
            "Generate Heatmap",
            type="primary"
        ):

            fig = correlation_heatmap(
                df
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)
