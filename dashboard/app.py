

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FinSight | Data Quality Engine",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_PATH = BASE_DIR / "data" / "reports" / "quality_report.json"
CLEAN_DATA_PATH = BASE_DIR / "data" / "processed" / "clean_transactions.csv"


# ============================================================
# 3. CUSTOM CSS (dark fintech theme)
# ============================================================

st.markdown(
    """
    <style>

         /* =========================================================
       GLOBAL BRIGHT TEXT OVERRIDE
       Har chota light-gray text ko bright white kar deta hai
       ========================================================= */

    /* ---------- Captions ("Transaction Data Quality Engine", footer, etc.) ---------- */
    .stCaption,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: #E8F0F7 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }

    /* ---------- Markdown paragraphs / body text ---------- */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] label {
        color: #DCE8F2 !important;
        opacity: 1 !important;
    }

    /* ---------- Sidebar text (module list, captions) ---------- */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] * {
        color: #DCE8F2 !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: #B8C9D6 !important;
        opacity: 1 !important;
    }

    /* ---------- Text inputs, placeholders ---------- */
    input::placeholder,
    textarea::placeholder {
        color: #8FA6B8 !important;
        opacity: 1 !important;
    }

    /* ---------- Selectbox, slider labels ---------- */
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] {
        color: #DCE8F2 !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }

    /* ---------- Slider tick labels (50, 85, 100) ---------- */
    div[data-testid="stSlider"] [data-testid="stTickBar"] * ,
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
        color: #B8C9D6 !important;
        opacity: 1 !important;
    }

    /* ---------- DataFrame header (column names) ---------- */
    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="columnheader"] * {
        color: #FFFFFF !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    /* ---------- Expander / details text ---------- */
    details summary,
    details summary * {
        color: #E8F0F7 !important;
        opacity: 1 !important;
    }

    /* ---------- Tabs ke unselected tab ka text ---------- */
    button[data-baseweb="tab"],
    button[data-baseweb="tab"] * {
        color: #B8C9D6 !important;
        opacity: 1 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] * {
        color: #5BE6C0 !important;
        opacity: 1 !important;
    }
    

     header[data-testid="stHeader"] {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* ---------- App background ---------- */
    .stApp { background-color: #07111F; color: #E8F0F7; }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 10% 0%, rgba(0,150,255,0.10), transparent 28%),
            radial-gradient(circle at 90% 5%, rgba(0,255,180,0.06), transparent 25%),
            #07111F;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: #06101B;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    /* ---------- Headings ---------- */
    h1 { color: #FFFFFF !important; font-weight: 800 !important; letter-spacing: -1px; }
    h2 { color: #EAF4F8 !important; font-weight: 750 !important; }
    h3 { color: #B8C9D6 !important; }

    /* ---------- Metric cards ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #10263A, #091827);
        border: 1px solid rgba(100,190,255,0.12);
        border-radius: 18px;
        padding: 22px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
        min-height: 130px;
    }

    div[data-testid="stMetricLabel"] {
        color: #FFFF00 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 30px !important;
        font-weight: 800 !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(80,180,255,0.18);
        background: #10283C;
        color: #EAF7FC;
        font-weight: 650;
    }

    .stButton > button:hover { border-color: #57DDB7; color: #57DDB7; }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        background: #0E2D42;
        color: #EAF7FC;
        border: 1px solid rgba(85,220,180,0.20);
        font-weight: 700;
    }

    .stDownloadButton > button:hover { background: #123A52; border-color: #5BE6C0; }

    /* ---------- Tabs ---------- */
    button[data-baseweb="tab"] { color: #7895A8; font-weight: 650; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #5BE6C0; }

    /* ---------- DataFrame ---------- */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        overflow: hidden;
    }

    /* ---------- Inputs ---------- */
    div[data-baseweb="input"]  { background-color: #0B1C2C; border-radius: 10px; }
    div[data-baseweb="select"] { background-color: #0B1C2C; border-radius: 10px; }

    /* ---------- Alerts / dividers / captions ---------- */
    div[data-testid="stAlert"] { border-radius: 12px; }
    hr { border-color: rgba(255,255,255,0.07); }
    .stCaption { color: #B8C9D6 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. DATA LOADING
# ============================================================

@st.cache_data
def load_report():
    """Load the JSON quality report, or None if missing."""
    if not REPORT_PATH.exists():
        return None
    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_clean_data():
    """Load the cleaned transaction CSV, or None if missing."""
    if not CLEAN_DATA_PATH.exists():
        return None
    return pd.read_csv(CLEAN_DATA_PATH)


# ============================================================
# 5. SAFE ACCESS HELPERS
# ============================================================

def get_report_value(report_data, keys, default=None):
    """Safely retrieve a nested value from the quality report."""
    current = report_data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def get_report_section(report_data, section_name, default=None):
    """Safely return a top-level section of the report."""
    if not isinstance(report_data, dict):
        return default
    return report_data.get(section_name, default)


def safe_int(value, default=0):
    """Coerce to int, tolerating None / NaN / bad values."""
    try:
        if value is None or pd.isna(value):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    """Coerce to float, tolerating None / NaN / bad values."""
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


# ============================================================
# 6. LOAD + VALIDATE INPUTS
# ============================================================

report = load_report()
clean_df = load_clean_data()


def _missing_inputs_error(message: str):
    """Render the standard 'run main.py first' error block."""
    st.error(message)
    st.info("Run this command first:")
    st.code("python main.py", language="bash")
    st.stop()


if report is None or not isinstance(report, dict):
    _missing_inputs_error("❌ Quality report not found or invalid.")

if clean_df is None or not isinstance(clean_df, pd.DataFrame):
    _missing_inputs_error("❌ Clean transaction dataset not found or invalid.")


# ============================================================
# 7. EXTRACT METRICS FROM REPORT
# ============================================================

dataset_info = get_report_section(report, "dataset", {})

original_rows = safe_int(get_report_value(dataset_info, ["original_rows"], 0))
clean_rows    = safe_int(get_report_value(dataset_info, ["clean_rows"], 0))
removed_rows  = safe_int(get_report_value(dataset_info, ["removed_rows"], 0))

duplicates         = safe_int(get_report_value(report, ["duplicates", "duplicate_count"], 0))
negative_amounts   = safe_int(get_report_value(report, ["invalid_amounts", "negative_amounts"], 0))
zero_amounts       = safe_int(get_report_value(report, ["invalid_amounts", "zero_amounts"], 0))
outlier_count      = safe_int(get_report_value(report, ["outliers", "outlier_count"], 0))
outlier_percentage = safe_float(
    get_report_value(report, ["outliers", "outlier_percentage"], 0.0)
)
invalid_types = safe_int(
    get_report_value(report, ["transaction_types", "invalid_transaction_type_count"], 0)
)


# ---------- Missing values table (SAFE) ----------
# The report may return:
#   - a list of dicts  -> normal case
#   - an empty list    -> no missing values
#   - a dict           -> alternate schema
#   - None             -> missing key
# We normalize everything into a DataFrame with a guaranteed
# "missing_count" column so downstream code never crashes.

def _build_missing_df(report_data) -> pd.DataFrame:
    raw = report_data.get("missing_values", []) if isinstance(report_data, dict) else []

    # Normalize to a list of records
    if isinstance(raw, dict):
        # e.g. {"amount": 3, "customer_id": 1}
        records = [{"column": k, "missing_count": v} for k, v in raw.items()]
    elif isinstance(raw, list):
        records = [r for r in raw if isinstance(r, dict)]
    else:
        records = []

    df = pd.DataFrame(records)

    # Guarantee the columns we depend on
    if "missing_count" not in df.columns:
        df["missing_count"] = pd.Series(dtype="int64")
    if "column" not in df.columns:
        # Fall back to index if no column name is present
        df["column"] = [f"column_{i}" for i in range(len(df))]

    # Coerce counts to numeric
    if not df.empty:
        df["missing_count"] = (
            pd.to_numeric(df["missing_count"], errors="coerce")
            .fillna(0)
            .astype(int)
        )

    return df


missing_df = _build_missing_df(report)
missing_total = int(missing_df["missing_count"].sum()) if not missing_df.empty else 0


# ============================================================
# 8. QUALITY SCORE
# ============================================================

total_issues = (
    missing_total
    + duplicates
    + negative_amounts
    + zero_amounts
    + invalid_types
)

if original_rows > 0:
    issue_rate = total_issues / original_rows
    quality_score = max(0, min(100, round(100 - issue_rate * 100, 1)))
else:
    quality_score = 0.0


def quality_status_for(score: float) -> str:
    if score >= 95: return "Excellent"
    if score >= 85: return "Good"
    if score >= 70: return "Needs Attention"
    return "Critical"


quality_status = quality_status_for(quality_score)


# ============================================================
# 9. SIDEBAR
# ============================================================

with st.sidebar:
    st.title("💳 FinSight")
    st.caption("Transaction Data Quality Engine")
    st.divider()

    st.subheader("System Status")
    st.success("● Pipeline Operational")
    st.divider()

    st.subheader("Quality Threshold")
    threshold = st.slider(
        "Minimum acceptable score",
        min_value=50, max_value=100, value=85, step=1,
    )
    if quality_score >= threshold:
        st.success(f"Score: {quality_score}%")
    else:
        st.warning(f"Score: {quality_score}%")

    st.divider()
    st.subheader("Engine Modules")
    for module in [
        "Schema Validation",
        "Missing Value Analysis",
        "Duplicate Detection",
        "Business Rule Validation",
        "Outlier Detection",
        "Automated Cleaning",
        "Quality Reporting",
        "Dashboard Monitoring",
    ]:
        # Hex code #EAF4F8 (soft white/blueish) ya #FFFFFF (pure white) use karein
        st.markdown(f"<span style='color: #EAF4F5;'>✓ {module}</span>", unsafe_allow_html=True)

    st.divider()
    st.caption("FinSight v1.0")


# ============================================================
# 10. HERO
# ============================================================

st.title("💳 FinTech Transaction Intelligence")
st.subheader("Data Quality Command Center")
st.write(
    "Monitor, validate and analyze the quality of financial "
    "transaction data from ingestion to analysis-ready output."
)
st.divider()


# ============================================================
# 11. PIPELINE OVERVIEW (top KPIs)
# ============================================================

st.subheader("📊 Pipeline Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total Transactions", f"{original_rows:,}",
        help="Total records received from the raw dataset.",
    )
with k2:
    st.metric(
        "Clean Transactions", f"{clean_rows:,}",
        help="Records remaining after cleaning.",
    )
with k3:
    st.metric(
        "Removed Records", f"{removed_rows:,}",
        help="Records removed during automated cleaning.",
    )
with k4:
    st.metric("Quality Score", f"{quality_score}%", quality_status)


# ============================================================
# 12. DATA HEALTH (metric + gauge)
# ============================================================

st.divider()
st.subheader("🩺 Data Health")

health_col1, health_col2 = st.columns([1, 2])

with health_col1:
    st.metric("Overall Quality", f"{quality_score}%", quality_status)

    if quality_score >= 95:
        st.success("Dataset health is excellent.")
    elif quality_score >= 85:
        st.success("Dataset is in good condition.")
    elif quality_score >= 70:
        st.warning("Dataset requires attention.")
    else:
        st.error("Dataset quality is critical.")

with health_col2:
    quality_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=quality_score,
            title={"text": "Data Quality Score"},
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#55E6BE"},
                "steps": [
                    {"range": [0, 70],   "color": "#321821"},
                    {"range": [70, 85],  "color": "#332C18"},
                    {"range": [85, 100], "color": "#123129"},
                ],
            },
        )
    )
    quality_gauge.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E8F0F7"},
    )
    st.plotly_chart(quality_gauge, width="stretch")


# ============================================================
# 13. QUALITY ISSUES CHART
# ============================================================

st.divider()
st.subheader("🚨 Data Quality Issues")

issue_df = pd.DataFrame(
    {
        "Issue": [
            "Missing Values",
            "Duplicates",
            "Negative Amounts",
            "Zero Amounts",
            "Invalid Types",
            "Outliers",
        ],
        "Count": [
            missing_total,
            duplicates,
            negative_amounts,
            zero_amounts,
            invalid_types,
            outlier_count,
        ],
    }
)

fig = px.bar(issue_df, x="Issue", y="Count", text="Count")
fig.update_traces(marker_color="#3EA6FF", textposition="outside")
fig.update_layout(
    height=400,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"color": "#DCE8F2"},
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis={"title": None, "gridcolor": "rgba(255,255,255,0.04)"},
    yaxis={"title": "Number of Records", "gridcolor": "rgba(255,255,255,0.05)"},
)
st.plotly_chart(fig, width="stretch")


# ============================================================
# 14. QUALITY BREAKDOWN
# ============================================================

st.divider()
st.subheader("🔍 Quality Breakdown")

b1, b2, b3, b4 = st.columns(4)

with b1:
    st.metric("Missing Values", f"{missing_total:,}")
with b2:
    st.metric("Duplicates", f"{duplicates:,}")
with b3:
    st.metric("Invalid Amounts", f"{negative_amounts + zero_amounts:,}")
with b4:
    st.metric("Outliers", f"{outlier_count:,}", f"{outlier_percentage}%")


# ============================================================
# 15. DETAIL TABS
# ============================================================

st.divider()

tab_missing, tab_outliers, tab_transactions, tab_validation = st.tabs(
    [
        "📋 Missing Values",
        "📈 Outliers",
        "💳 Transactions",
        "🔎 Validation",
    ]
)


# ---------- 15a. Missing Values tab ----------

with tab_missing:
    st.subheader("Missing Value Analysis")
    st.write("Columns are ranked by the number of missing values.")

    if missing_df.empty:
        st.info("✅ No missing values found in the dataset.")
    else:
        display_missing = missing_df.copy().sort_values(
            "missing_count", ascending=False
        )
        st.dataframe(display_missing, width="stretch", height=400)


# ---------- 15b. Outliers tab ----------

with tab_outliers:
    st.subheader("Transaction Amount Analysis")

    outliers_report = report.get("outliers", {}) if isinstance(report, dict) else {}
    lower_bound = outliers_report.get("lower_bound", 0.0)
    upper_bound = outliers_report.get("upper_bound", 0.0)

    o1, o2, o3 = st.columns(3)
    with o1:
        st.metric("Lower Bound", f"{lower_bound:,.2f}")
    with o2:
        st.metric("Upper Bound", f"{upper_bound:,.2f}")
    with o3:
        st.metric("Outliers", f"{outlier_count:,}")

    st.info(
        "An outlier is not automatically fraud. "
        "A high-value transaction can be legitimate."
    )

    if "amount" in clean_df.columns:
        amount_df = (
            clean_df[["amount"]]
            .dropna()
            .head(300)
            .reset_index(drop=True)
        )
        amount_chart = px.line(amount_df, y="amount", title="Transaction Amount Trend")
        amount_chart.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#DCE8F2"},
        )
        st.plotly_chart(amount_chart, width="stretch")


# ---------- 15c. Transactions tab ----------

with tab_transactions:
    st.subheader("Clean Transaction Explorer")
    st.write(f"{len(clean_df):,} analysis-ready records available.")

    search = st.text_input(
        "🔎 Search",
        placeholder="Search customer, merchant, transaction type...",
    )

    transaction_type_filter = st.selectbox(
        "Transaction Type",
        options=["All"]
        + (
            sorted(
                clean_df["transaction_type"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
            if "transaction_type" in clean_df.columns
            else []
        ),
    )

    filtered_df = clean_df.copy()

    # Search across all columns (string match, case-insensitive)
    if search:
        mask = (
            filtered_df.astype(str)
            .apply(lambda col: col.str.contains(search, case=False, na=False))
            .any(axis=1)
        )
        filtered_df = filtered_df[mask]

    # Transaction type filter
    if transaction_type_filter != "All" and "transaction_type" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["transaction_type"].astype(str) == transaction_type_filter
        ]

    st.caption(
        f"Showing {min(len(filtered_df), 100):,} "
        f"of {len(filtered_df):,} matching records."
    )
    st.dataframe(filtered_df.head(100), width="stretch", height=500)


# ---------- 15d. Validation tab ----------

with tab_validation:
    st.subheader("Validation Results")

    schema_section            = get_report_section(report, "schema", {})
    data_types_section        = get_report_section(report, "data_types", {})
    transaction_types_section = get_report_section(report, "transaction_types", {})

    schema_valid      = bool(get_report_value(schema_section, ["schema_valid"], False))
    amount_numeric    = bool(get_report_value(data_types_section, ["amount_numeric"], False))
    date_valid        = bool(get_report_value(data_types_section, ["date_valid"], False))
    transaction_valid = bool(get_report_value(transaction_types_section, ["valid"], False))

    validation_df = pd.DataFrame(
        {
            "Validation": [
                "Schema Structure",
                "Amount Numeric",
                "Date Valid",
                "Transaction Types",
            ],
            "Status": [
                "PASS" if schema_valid      else "FAIL",
                "PASS" if amount_numeric    else "FAIL",
                "PASS" if date_valid        else "FAIL",
                "PASS" if transaction_valid else "FAIL",
            ],
        }
    )

    st.dataframe(validation_df, width="stretch", hide_index=True)

    st.subheader("Schema Details")
    st.json(schema_section)


# ============================================================
# 16. EXPORT
# ============================================================

st.divider()
st.subheader("📥 Export")

download1, download2 = st.columns(2)

with download1:
    st.download_button(
        label="⬇️ Download Clean Dataset",
        data=clean_df.to_csv(index=False),
        file_name="clean_transactions.csv",
        mime="text/csv",
        width="stretch",
    )

with download2:
    st.download_button(
        label="⬇️ Download Quality Report",
        data=json.dumps(report, indent=4, default=str),
        file_name="quality_report.json",
        mime="application/json",
        width="stretch",
    )


# ============================================================
# 17. FOOTER
# ============================================================

st.divider()
st.caption("💳 FinSight Data Quality Engine • Python • Pandas • Plotly • Streamlit")