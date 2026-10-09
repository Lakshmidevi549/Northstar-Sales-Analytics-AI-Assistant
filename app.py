import streamlit as st
import pandas as pd

from config import APP_NAME, APP_ICON


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "df": None,
    "file_name": None,
    "chat_history": [],
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background: #f5f7fb;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0f172a 0%,
            #172554 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15);
    }

    /* -------------------------------------------------------
       HERO
    ------------------------------------------------------- */

    .hero {
        padding: 10px 0 25px 0;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #dbeafe;
        color: #1d4ed8;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 42px;
        line-height: 1.1;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 17px;
        margin-top: 8px;
    }

    /* -------------------------------------------------------
       CARDS
    ------------------------------------------------------- */

    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        min-height: 115px;
    }

    .metric-title {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .metric-value {
        color: #0f172a;
        font-size: 29px;
        font-weight: 800;
        margin-top: 5px;
    }

    .metric-description {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    /* -------------------------------------------------------
       SECTION
    ------------------------------------------------------- */

    .section-title {
        color: #0f172a;
        font-size: 24px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 42px;
    }

    /* -------------------------------------------------------
       DATAFRAME
    ------------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* -------------------------------------------------------
       CHAT
    ------------------------------------------------------- */

    div[data-testid="stChatMessage"] {
        border-radius: 14px;
    }

    /* -------------------------------------------------------
       SIDEBAR BRAND
    ------------------------------------------------------- */

    .sidebar-brand {
        padding: 8px 0 12px 0;
    }

    .sidebar-brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
    }

    .sidebar-brand-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 3px;
    }

    .sidebar-label {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
    }

    .dataset-info {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px;
        margin-top: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">
                📊 AI EDA Studio
            </div>
            <div class="sidebar-brand-subtitle">
                Intelligent Exploratory Data Analysis
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # --------------------------------------------------------
    # DATASET UPLOAD
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-label">DATASET</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel dataset.",
    )

    if uploaded_file is not None:

        # Avoid unnecessarily reloading the same file
        if st.session_state.file_name != uploaded_file.name:

            try:

                if uploaded_file.name.lower().endswith(
                    (".xlsx", ".xls")
                ):
                    df = pd.read_excel(uploaded_file)

                else:
                    # Try common encodings
                    try:
                        df = pd.read_csv(
                            uploaded_file,
                            encoding="utf-8",
                        )
                    except UnicodeDecodeError:
                        uploaded_file.seek(0)

                        df = pd.read_csv(
                            uploaded_file,
                            encoding="latin-1",
                        )

                st.session_state.df = df
                st.session_state.file_name = uploaded_file.name
                st.session_state.chat_history = []

                st.success(
                    f"Loaded: {uploaded_file.name}"
                )

            except Exception as e:

                st.error(
                    f"Could not load dataset: {e}"
                )

    # --------------------------------------------------------
    # DEMO DATASET
    # --------------------------------------------------------

    if st.button(
        "✨ Try Demo Dataset",
        use_container_width=True,
    ):

        demo_df = pd.DataFrame(
            {
                "Customer_ID": range(1, 101),
                "Age": [
                    22 + (i * 7) % 45
                    for i in range(100)
                ],
                "Income": [
                    25000 + (i * 1375) % 90000
                    for i in range(100)
                ],
                "Spending_Score": [
                    20 + (i * 11) % 80
                    for i in range(100)
                ],
                "City": [
                    ["Delhi", "Mumbai", "Bangalore", "Chennai"][
                        i % 4
                    ]
                    for i in range(100)
                ],
                "Membership": [
                    ["Basic", "Silver", "Gold"][i % 3]
                    for i in range(100)
                ],
            }
        )

        # Add realistic data-quality problems
        demo_df.loc[5, "Income"] = None
        demo_df.loc[18, "Age"] = None
        demo_df.loc[30, "City"] = None

        # Duplicate rows for demonstration
        demo_df.loc[98] = demo_df.loc[20]
        demo_df.loc[99] = demo_df.loc[40]

        st.session_state.df = demo_df
        st.session_state.file_name = "demo_customer_dataset.csv"
        st.session_state.chat_history = []

        st.success("Demo dataset loaded!")

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    if st.session_state.df is not None:

        if st.button(
            "🗑️ Reset Workspace",
            use_container_width=True,
        ):

            st.session_state.df = None
            st.session_state.file_name = None
            st.session_state.chat_history = []

            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-label">NAVIGATION</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔍 Data Analysis",
            "📈 Visualization",
            "🤖 AI Analyst",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    # --------------------------------------------------------
    # DATASET STATUS
    # --------------------------------------------------------

    if st.session_state.df is not None:

        df = st.session_state.df

        st.markdown(
            '<div class="sidebar-label">CURRENT DATASET</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="dataset-info">
                <div style="font-weight:700;">
                    📄 {st.session_state.file_name}
                </div>

                <div style="
                    color:#cbd5e1;
                    font-size:12px;
                    margin-top:8px;
                ">
                    Rows: {len(df):,}
                    <br>
                    Columns: {len(df.columns):,}
                    <br>
                    Missing: {int(df.isna().sum().sum()):,}
                    <br>
                    Duplicates: {int(df.duplicated().sum()):,}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "Upload a dataset or try the demo dataset to begin."
        )

    st.divider()

    st.caption(
        "AI EDA Studio • Data Analysis Project"
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "🏠 Dashboard":

    from pages.dashboard import show_dashboard

    show_dashboard()


elif page == "🔍 Data Analysis":

    from pages.data_analysis import show_data_analysis

    show_data_analysis()


elif page == "📈 Visualization":

    from pages.visualization import show_visualization

    show_visualization()


elif page == "🤖 AI Analyst":

    from pages.ai_analyst import show_ai_analyst

    show_ai_analyst()