import re
import textwrap
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Access Control & Privilege Analysis",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# HTML RENDERING GUARD
#
# Streamlit renders markdown, and markdown ENDS a raw HTML block at the
# first blank line. Any following line indented 4+ spaces then becomes a
# fenced code block -- which is why hand-indented HTML shows up on screen
# as literal source. render_html() strips indentation and blank lines so
# the browser always receives one clean HTML block.
# ============================================================

def render_html(html, target=None):
    """Collapse HTML to a safe single block, then render it."""
    cleaned = textwrap.dedent(html).strip()
    cleaned = "\n".join(
        line.strip() for line in cleaned.splitlines() if line.strip()
    )
    cleaned = re.sub(r">\s+<", "><", cleaned)
    (target or st).markdown(cleaned, unsafe_allow_html=True)


def inject_css(css):
    """
    Inject a stylesheet safely.

    Same trap as render_html: markdown ends an HTML block at the first blank
    line, so blank lines between CSS rule groups cause every following rule to
    be printed on the page as text. Stripping blank lines and indentation keeps
    the <style> element intact.
    """
    body = "\n".join(
        line.strip() for line in css.splitlines() if line.strip()
    )
    st.markdown(body, unsafe_allow_html=True)


def stretch(**kwargs):
    """Width kwarg that works on both old and new Streamlit versions."""
    return kwargs


# Streamlit renamed use_container_width -> width="stretch". Detect once.
try:
    _ST_MAJOR = int(st.__version__.split(".")[0])
    _ST_MINOR = int(st.__version__.split(".")[1])
    _NEW_WIDTH_API = (_ST_MAJOR, _ST_MINOR) >= (1, 49)
except Exception:
    _NEW_WIDTH_API = False

WIDTH_KW = {"width": "stretch"} if _NEW_WIDTH_API else {"use_container_width": True}


# ============================================================
# THEME
# ============================================================

THEMES = {
    "Light": {
        "bg": "#f4f7fb",
        "surface": "#ffffff",
        "surface_2": "#f8fafc",
        "sidebar": "#ffffff",
        "border": "#e2e8f0",
        "text": "#0f172a",
        "muted": "#54657d",
        "primary": "#4f46e5",
        "secondary": "#7c3aed",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "grid": "#eef2f7",
        "shadow": "0 2px 14px rgba(15, 23, 42, 0.06)",
        "shadow_hover": "0 10px 28px rgba(79, 70, 229, 0.16)",
        "card": "linear-gradient(160deg, #ffffff 0%, #fafbfe 100%)",
        "hero": "linear-gradient(135deg, #eef2ff 0%, #ffffff 52%, #f5f3ff 100%)",
        "glow": "radial-gradient(1000px 340px at 10% -35%, rgba(79,70,229,0.08), transparent 60%)",
        "plot_bg": "#ffffff",
    },
    "Dark": {
        "bg": "#0a1120",
        "surface": "#131f33",
        "surface_2": "#1a293f",
        "sidebar": "#0d1626",
        "border": "#2b4260",
        "text": "#f2f7fd",
        "muted": "#b3c6dd",
        "primary": "#9aa5ff",
        "secondary": "#c4a9ff",
        "success": "#4ade80",
        "warning": "#fcd34d",
        "danger": "#fb8b8b",
        "grid": "#243a56",
        "shadow": "0 4px 22px rgba(0, 0, 0, 0.45)",
        "shadow_hover": "0 10px 30px rgba(129, 140, 248, 0.18)",
        "card": "linear-gradient(160deg, #101b2d 0%, #14213604 100%)",
        "hero": "linear-gradient(135deg, #131f36 0%, #101b2d 55%, #17162e 100%)",
        "glow": "radial-gradient(1000px 340px at 10% -35%, rgba(129,140,248,0.13), transparent 60%)",
        "plot_bg": "rgba(0,0,0,0)",
    },
}
THEMES["Dark"]["card"] = "linear-gradient(160deg, #131f33 0%, #17263d 100%)"
THEMES["Light"]["scheme"] = "light"
THEMES["Dark"]["scheme"] = "dark"

if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Light"


# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(filename):
    file_path = OUTPUT_DIR / filename

    if file_path.exists():
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


@st.cache_data
def load_raw_csv(filename):
    file_path = DATA_DIR / filename

    if file_path.exists():
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


# ============================================================
# LOAD ANALYSIS RESULTS
# ============================================================

excessive_permissions = load_csv("excessive_permissions.csv")
excessive_roles = load_csv("excessive_roles.csv")
high_privilege_roles = load_csv("high_privilege_roles.csv")
role_privilege_distribution = load_csv("role_privilege_distribution.csv")
user_permission_distribution = load_csv("user_permission_distribution.csv")
user_role_distribution = load_csv("user_role_distribution.csv")


# ============================================================
# LOAD RAW DATA
# ============================================================

users = load_raw_csv("users.csv")
roles = load_raw_csv("roles.csv")
permissions = load_raw_csv("permissions.csv")
resources = load_raw_csv("resources.csv")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_record_count(dataframe):
    if dataframe is None or dataframe.empty:
        return 0

    return len(dataframe)


def get_column(dataframe, possible_columns):
    if dataframe is None or dataframe.empty:
        return None

    for column in possible_columns:
        if column in dataframe.columns:
            return column

    return None


def show_dataframe(dataframe, height=420):
    if dataframe is not None and not dataframe.empty:
        st.dataframe(dataframe, height=height, **WIDTH_KW)
    else:
        st.info("No data is available for this dataset.")


def download_button(dataframe, label, filename, key=None):
    """Every table on the dashboard is exportable."""
    if dataframe is None or dataframe.empty:
        return
    st.download_button(
        label=label,
        data=dataframe.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        key=key,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render_html(
        """
        <div class="brand">
        <div class="brand-icon">🔐</div>
        <div>
        <div class="brand-name">ACCESS CONTROL</div>
        <div class="brand-sub">Security Analytics Platform</div>
        </div>
        </div>
        """
    )

    render_html("<div class='rule'></div>")
    render_html("<div class='side-label'>Appearance</div>")

    theme_choice = st.selectbox(
        "Theme",
        options=["Light", "Dark"],
        index=0 if st.session_state.theme_choice == "Light" else 1,
        label_visibility="collapsed",
    )
    st.session_state.theme_choice = theme_choice

    render_html("<div class='side-label'>Navigation</div>")

    page = st.radio(
        "Navigation",
        [
            "Dashboard Overview",
            "User Analysis",
            "Role Analysis",
            "Security Findings",
            "Data Explorer",
        ],
        label_visibility="collapsed",
    )

    render_html("<div class='rule'></div>")
    render_html("<div class='side-label'>Project Information</div>")

    render_html(
        """
        <div class="side-card">
        <div class="side-row"><span>Project</span><b>Access Control / Privilege Analysis</b></div>
        <div class="side-row"><span>Database</span><b>SQLite</b></div>
        <div class="side-row"><span>Analysis</span><b>RBAC &amp; Privilege Review</b></div>
        </div>
        """
    )

    _findings_total = (
        get_record_count(excessive_permissions)
        + get_record_count(excessive_roles)
        + get_record_count(high_privilege_roles)
    )
    _status = "success" if _findings_total == 0 else "warn"

    render_html(
        f"""
        <div class="side-card status-{_status}">
        <div class="status-line"><span class="dot"></span>{_findings_total} OPEN FINDINGS</div>
        <div class="status-sub">{get_record_count(users)} users &middot; {get_record_count(roles)} roles</div>
        </div>
        """
    )


# ============================================================
# THEME COLOR TOKENS
# ============================================================

T = THEMES[st.session_state.theme_choice]

PRIMARY_COLOR = T["primary"]
SECONDARY_COLOR = T["secondary"]
SUCCESS_COLOR = T["success"]
WARNING_COLOR = T["warning"]
DANGER_COLOR = T["danger"]
DARK_COLOR = T["text"]
TEXT_COLOR = T["text"]
MUTED_COLOR = T["muted"]
BORDER_COLOR = T["border"]
CARD_BACKGROUND = T["surface"]
PAGE_BACKGROUND = T["bg"]


# ============================================================
# CUSTOM STYLING
# ============================================================

inject_css(
    f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {{
    font-family: Inter, "Segoe UI", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.stApp {{ background: {T["bg"]}; color: {T["text"]}; }}
[data-testid="stAppViewContainer"] {{ background: {T["glow"]}, {T["bg"]}; }}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1520px; }}

::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {T["border"]}; border-radius: 10px; }}
::-webkit-scrollbar-thumb:hover {{ background: {T["muted"]}; }}

section[data-testid="stSidebar"] {{
    background: {T["sidebar"]};
    border-right: 1px solid {T["border"]};
}}
section[data-testid="stSidebar"] .block-container {{ padding-top: 1.7rem; }}

.brand {{ display: flex; align-items: center; gap: .8rem; padding: .2rem 0 1.2rem 0; }}
.brand-icon {{ font-size: 1.7rem; line-height: 1; filter: drop-shadow(0 0 10px {T["primary"]}55); }}
.brand-name {{ font-size: 1rem; font-weight: 900; letter-spacing: .07em; color: {T["text"]}; }}
.brand-sub {{ font-size: .78rem; color: {T["muted"]}; margin-top: .18rem; }}

.rule {{ height: 1px; background: linear-gradient(90deg, {T["border"]}, transparent); margin: .9rem 0 1.1rem; }}
.side-label {{
    color: {T["muted"]}; font-size: .68rem; font-weight: 800;
    letter-spacing: .13em; text-transform: uppercase; margin: 1.1rem 0 .55rem;
}}
.side-card {{
    background: {T["card"]}; border: 1px solid {T["border"]};
    border-radius: 13px; padding: .9rem 1rem; box-shadow: {T["shadow"]};
}}
.side-row {{ display: flex; flex-direction: column; gap: .12rem; padding: .48rem 0; border-top: 1px solid {T["border"]}80; }}
.side-row:first-child {{ border-top: none; padding-top: 0; }}
.side-row span {{ font-size: .66rem; font-weight: 800; letter-spacing: .09em; text-transform: uppercase; color: {T["muted"]}; }}
.side-row b {{ font-size: .85rem; font-weight: 600; color: {T["text"]}; line-height: 1.35; }}

.status-line {{ display: flex; align-items: center; gap: .5rem; font-size: .8rem; font-weight: 800; letter-spacing: .05em; }}
.status-warn .status-line {{ color: {T["warning"]}; }}
.status-success .status-line {{ color: {T["success"]}; }}
.status-sub {{ color: {T["muted"]}; font-size: .78rem; margin-top: .4rem; }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: currentColor; animation: pulse 2.2s infinite; }}
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 currentColor; opacity: 1; }}
    70% {{ box-shadow: 0 0 0 8px transparent; opacity: .75; }}
    100% {{ box-shadow: 0 0 0 0 transparent; opacity: 1; }}
}}

.hero {{
    background: {T["hero"]}; border: 1px solid {T["border"]};
    border-radius: 20px; padding: 1.7rem 2rem; margin-bottom: 1.5rem;
    box-shadow: {T["shadow"]};
}}
.hero-title {{
    display: flex; align-items: center; gap: .65rem;
    font-size: clamp(1.5rem, 2.6vw, 2.35rem); font-weight: 800;
    letter-spacing: -.03em; color: {T["text"]}; margin: 0;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.hero-sub {{ font-size: .98rem; color: {T["muted"]}; margin-top: .55rem; line-height: 1.6; max-width: 900px; }}

.section-title {{
    display: flex; align-items: center; gap: .65rem;
    font-size: 1.28rem; font-weight: 800; color: {T["text"]};
    letter-spacing: -.015em; margin: 1.9rem 0 .4rem;
}}
.section-title::before {{
    content: ""; width: 3px; height: 1.05em; border-radius: 3px; flex-shrink: 0;
    background: linear-gradient(180deg, {T["primary"]}, {T["secondary"]});
}}
.section-description {{ color: {T["muted"]}; font-size: .92rem; margin: 0 0 1.1rem 1.3rem; }}

div[data-testid="stMetric"] {{
    background: {T["card"]}; border: 1px solid {T["border"]};
    padding: 1.05rem 1.2rem; border-radius: 15px;
    box-shadow: {T["shadow"]}; min-height: 112px;
    position: relative; overflow: hidden;
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}}
div[data-testid="stMetric"]::before {{
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, {T["primary"]}, {T["secondary"]});
}}
div[data-testid="stMetric"]:hover {{
    transform: translateY(-3px); border-color: {T["primary"]}66; box-shadow: {T["shadow_hover"]};
}}
div[data-testid="stMetricLabel"] {{
    color: {T["muted"]} !important; font-size: .7rem !important;
    font-weight: 800 !important; letter-spacing: .1em; text-transform: uppercase;
}}
div[data-testid="stMetricValue"] {{
    color: {T["text"]} !important; font-size: 1.95rem !important;
    font-weight: 800 !important; letter-spacing: -.03em; font-variant-numeric: tabular-nums;
}}

div[data-testid="stDataFrame"] {{
    border: 1px solid {T["border"]}; border-radius: 12px;
    overflow: hidden; box-shadow: {T["shadow"]};
}}
.js-plotly-plot {{
    border: 1px solid {T["border"]}; border-radius: 15px;
    overflow: hidden; box-shadow: {T["shadow"]}; background: {T["surface"]};
}}

button[data-baseweb="tab"] {{ font-size: .93rem; font-weight: 700; color: {T["muted"]}; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {T["primary"]}; }}
div[data-baseweb="tab-highlight"] {{ background: {T["primary"]}; }}

div.stButton > button, div.stDownloadButton > button {{
    border-radius: 10px; font-weight: 600;
    border: 1px solid {T["border"]}; background: {T["surface_2"]}; color: {T["text"]};
    padding: .48rem 1.1rem; transition: all .18s ease;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover {{
    border-color: {T["primary"]}; color: {T["primary"]};
    transform: translateY(-1px); box-shadow: {T["shadow_hover"]};
}}
div[data-baseweb="select"] > div, .stTextInput input {{
    background: {T["surface"]}; border-color: {T["border"]};
    border-radius: 10px; color: {T["text"]};
}}
.stTextInput input:focus {{ border-color: {T["primary"]}; box-shadow: 0 0 0 2px {T["primary"]}25; }}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label {{
    border-radius: 8px; padding: .34rem .5rem; transition: background .15s ease;
}}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {{ background: {T["surface_2"]}; }}

.insight {{
    background: {T["card"]}; border: 1px solid {T["border"]};
    border-left: 3px solid {T["primary"]}; border-radius: 13px;
    padding: 1rem 1.2rem; margin-bottom: .8rem; box-shadow: {T["shadow"]};
}}
.insight-title {{ font-size: .93rem; font-weight: 700; color: {T["text"]}; margin-bottom: .35rem; }}
.insight-text {{ font-size: .88rem; color: {T["muted"]}; line-height: 1.6; }}
.insight-text b {{ color: {T["text"]}; }}
.insight.danger {{ border-left-color: {T["danger"]}; }}
.insight.warning {{ border-left-color: {T["warning"]}; }}
.insight.secondary {{ border-left-color: {T["secondary"]}; }}

.footer-box {{
    margin-top: 2.2rem; padding: 1.1rem 1.4rem;
    background: {T["card"]}; border: 1px solid {T["border"]};
    border-radius: 14px; color: {T["muted"]}; text-align: center; font-size: .85rem;
}}
.footer-box b {{ color: {T["text"]}; }}

@media (max-width: 1100px) {{
    .hero-title {{ white-space: normal; font-size: clamp(1.35rem, 4.2vw, 1.9rem); }}
}}
/* ============================================================
   STREAMLIT INTERNAL TEXT OVERRIDES
   Streamlit's own base theme (config.toml) colours its widget
   labels, captions and tick marks. Those elements out-specify
   plain CSS, so in a runtime-switched dark theme they stay
   near-black and become unreadable. Force them here.
   ============================================================ */
.stApp {{ color-scheme: {T["scheme"]}; }}
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] div,
.stTextInput label, .stSelectbox label, .stSlider label,
.stRadio label, .stCheckbox label, .stMultiSelect label {{
    color: {T["muted"]} !important;
    font-weight: 600 !important;
}}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
.stMarkdown p, .stMarkdown li {{ color: {T["text"]}; }}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label p,
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label div,
.stRadio [role="radiogroup"] label p {{
    color: {T["text"]} !important;
    font-weight: 500 !important;
}}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
.stCaption, .stCaption p {{ color: {T["muted"]} !important; }}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div {{ color: {T["muted"]} !important; }}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] div {{ color: {T["text"]} !important; }}
[data-testid="stMetricDelta"], [data-testid="stMetricDelta"] div {{ color: {T["muted"]} !important; }}
[data-testid="stTickBarMin"], [data-testid="stTickBarMax"],
[data-testid="stThumbValue"] {{ color: {T["muted"]} !important; }}
[data-baseweb="slider"] [role="slider"] {{ background: {T["primary"]} !important; }}
.stTextInput input, .stTextInput input:focus {{ color: {T["text"]} !important; }}
.stTextInput input::placeholder {{ color: {T["muted"]} !important; opacity: .8; }}
div[data-baseweb="select"] *, div[data-baseweb="select"] div {{ color: {T["text"]} !important; }}
div[data-baseweb="popover"] li, div[data-baseweb="menu"] li {{
    background: {T["surface"]} !important; color: {T["text"]} !important;
}}
div[data-baseweb="popover"] li:hover, div[data-baseweb="menu"] li:hover {{
    background: {T["surface_2"]} !important;
}}
button[data-baseweb="tab"] p, button[data-baseweb="tab"] div {{ color: {T["muted"]} !important; }}
button[data-baseweb="tab"][aria-selected="true"] p,
button[data-baseweb="tab"][aria-selected="true"] div {{
    color: {T["primary"]} !important; font-weight: 700 !important;
}}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p,
details summary, details summary p {{ color: {T["text"]} !important; }}
[data-testid="stExpander"] details {{
    background: {T["card"]}; border: 1px solid {T["border"]}; border-radius: 12px;
}}
[data-testid="stAlert"] {{
    background: {T["surface_2"]} !important; border: 1px solid {T["border"]};
    border-radius: 12px; color: {T["text"]} !important;
}}
[data-testid="stAlert"] p, [data-testid="stAlert"] div {{ color: {T["text"]} !important; }}
[data-testid="stHeader"] button, [data-testid="stHeader"] svg,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg {{ color: {T["text"]} !important; fill: {T["text"]} !important; }}
h1, h2, h3, h4, h5, h6 {{ color: {T["text"]} !important; }}
div.stButton > button p, div.stDownloadButton > button p {{ color: inherit !important; }}
</style>
"""
)


# ============================================================
# CHART STYLING
# ============================================================

def _supports(builder):
    try:
        builder()
        return True
    except Exception:
        return False


_ROUNDED = _supports(lambda: go.Bar(x=["a"], y=[1], marker=dict(cornerradius=6)))
BAR_MARKER = dict(cornerradius=6) if _ROUNDED else {}

SEQ_BLUE = [T["primary"], T["secondary"]]


def apply_chart_style(
    fig,
    height=420,
    show_legend=False,
    xaxis_title=None,
    yaxis_title=None,
):
    """
    Apply one consistent Plotly layout.

    IMPORTANT:
    Only one xaxis and one yaxis dictionary are passed here.
    This prevents the duplicate 'yaxis' update_layout error.
    """
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=T["plot_bg"],
        margin=dict(l=30, r=30, t=62, b=60),
        font=dict(
            family='Inter, "Segoe UI", Arial, sans-serif',
            color=T["muted"],
            size=12,
        ),
        title=dict(font=dict(size=15, color=T["text"]), x=0.015, y=0.96),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=T["muted"], size=11),
        ),
        hoverlabel=dict(
            bgcolor=T["surface_2"],
            bordercolor=T["border"],
            font=dict(color=T["text"], size=12),
        ),
        coloraxis_showscale=False,
        xaxis=dict(
            title=xaxis_title,
            showgrid=False,
            linecolor=T["border"],
            tickfont=dict(color=T["muted"], size=11),
        ),
        yaxis=dict(
            title=yaxis_title,
            showgrid=True,
            gridcolor=T["grid"],
            zeroline=False,
            linecolor=T["border"],
            tickfont=dict(color=T["muted"], size=11),
        ),
    )
    return fig


def ranked_bar(
    data,
    label_col,
    value_col,
    title,
    top_n=15,
    color=None,
    x_title="Count",
    y_title=None,
    height=430,
):
    """
    Horizontal ranked bar chart.

    Horizontal beats vertical here because role and user names are long --
    vertical bars force 45-degree rotated labels that are hard to read.
    """
    color = color or T["primary"]
    chart_data = (
        data.sort_values(value_col, ascending=False)
        .head(top_n)
        .sort_values(value_col, ascending=True)
    )

    fig = px.bar(
        chart_data,
        x=value_col,
        y=label_col,
        orientation="h",
        title=title,
        color=value_col,
        color_continuous_scale=[[0, color + "55"], [1, color]],
        text=value_col,
    )
    fig.update_traces(
        marker_line_width=0,
        marker=BAR_MARKER,
        texttemplate="%{text:,}",
        textposition="outside",
        textfont=dict(size=11, color=T["muted"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>" + x_title + ": %{x:,}<extra></extra>",
    )
    apply_chart_style(fig, height=height, xaxis_title=x_title, yaxis_title=y_title)
    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            linecolor=T["border"],
            tickfont=dict(color=T["text"], size=11),
            title=y_title,
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=T["grid"],
            zeroline=False,
            linecolor=T["border"],
            tickfont=dict(color=T["muted"], size=11),
            title=x_title,
        ),
        margin=dict(l=10, r=60, t=62, b=45),
    )
    return fig


def insight(title, text, tone=""):
    render_html(
        f"""
        <div class="insight {tone}">
        <div class="insight-title">{title}</div>
        <div class="insight-text">{text}</div>
        </div>
        """
    )


def section(title, description=None):
    render_html(f'<div class="section-title">{title}</div>')
    if description:
        render_html(f'<div class="section-description">{description}</div>')


# ============================================================
# MAIN HEADER
# ============================================================

render_html(
    """
    <div class="hero">
    <div class="hero-title"><span>🔐</span><span>Access Control &amp; Privilege Analysis</span></div>
    <div class="hero-sub">Interactive security analysis of users, roles, permissions, resources, and potentially excessive privilege assignments</div>
    </div>
    """
)


# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

if page == "Dashboard Overview":

    section(
        "📊 Security Overview",
        "A high-level view of the access control environment and identified security risks.",
    )

    total_users = get_record_count(users)
    total_roles = get_record_count(roles)
    total_permissions = get_record_count(permissions)
    total_resources = get_record_count(resources)
    total_excessive_permissions = get_record_count(excessive_permissions)
    total_excessive_roles = get_record_count(excessive_roles)
    total_high_privilege_roles = get_record_count(high_privilege_roles)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Users", f"{total_users:,}")
    with col2:
        st.metric("Total Roles", f"{total_roles:,}")
    with col3:
        st.metric("Total Permissions", f"{total_permissions:,}")
    with col4:
        st.metric("Total Resources", f"{total_resources:,}")

    # --------------------------------------------------------
    # SECURITY FINDINGS
    # --------------------------------------------------------

    section("🚨 Security Findings")

    finding_col1, finding_col2, finding_col3, finding_col4 = st.columns(4)

    total_findings = (
        total_excessive_permissions
        + total_excessive_roles
        + total_high_privilege_roles
    )

    affected_pct = (
        f"{(total_excessive_permissions / total_users * 100):.1f}% of users"
        if total_users
        else None
    )

    with finding_col1:
        st.metric(
            "Excessive Permissions",
            f"{total_excessive_permissions:,}",
            delta=affected_pct,
            delta_color="off",
        )
    with finding_col2:
        st.metric("Excessive Roles", f"{total_excessive_roles:,}")
    with finding_col3:
        st.metric("High-Privilege Roles", f"{total_high_privilege_roles:,}")
    with finding_col4:
        st.metric("Total Open Findings", f"{total_findings:,}")

    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    section("📈 Privilege Concentration")

    top_n = st.slider(
        "Number of top entries to display in the charts below",
        min_value=5,
        max_value=25,
        value=12,
        step=1,
    )

    left_column, right_column = st.columns(2)

    with left_column:
        if not role_privilege_distribution.empty:
            role_column = get_column(
                role_privilege_distribution, ["role_name", "role", "name"]
            )
            privilege_column = get_column(
                role_privilege_distribution,
                ["permission_count", "privilege_count", "permissions", "count"],
            )

            if role_column and privilege_column:
                fig = ranked_bar(
                    role_privilege_distribution,
                    role_column,
                    privilege_column,
                    "🛡️ Top Roles by Permission Count",
                    top_n=top_n,
                    color=T["primary"],
                    x_title="Permissions",
                )
                st.plotly_chart(fig, **WIDTH_KW)
            else:
                show_dataframe(role_privilege_distribution)
        else:
            st.info("Role privilege distribution data was not found.")

    with right_column:
        if not user_permission_distribution.empty:
            user_column = get_column(
                user_permission_distribution, ["username", "user_name", "user"]
            )
            permission_column = get_column(
                user_permission_distribution,
                ["permission_count", "permissions", "privilege_count", "count"],
            )

            if user_column and permission_column:
                fig = ranked_bar(
                    user_permission_distribution,
                    user_column,
                    permission_column,
                    "👤 Users with the Most Permissions",
                    top_n=top_n,
                    color=T["secondary"],
                    x_title="Permissions",
                )
                st.plotly_chart(fig, **WIDTH_KW)
            else:
                show_dataframe(user_permission_distribution)
        else:
            st.info("User permission distribution data was not found.")

    # --------------------------------------------------------
    # ANALYSIS SUMMARY
    # --------------------------------------------------------

    section("🎯 Analysis Summary")

    summary_data = pd.DataFrame(
        {
            "Security Category": [
                "Excessive Permissions",
                "Excessive Roles",
                "High-Privilege Roles",
            ],
            "Findings": [
                total_excessive_permissions,
                total_excessive_roles,
                total_high_privilege_roles,
            ],
        }
    )

    summary_left, summary_right = st.columns([1, 1.4])

    with summary_left:
        fig = px.pie(
            summary_data,
            names="Security Category",
            values="Findings",
            hole=0.62,
            title="Findings Distribution",
            color="Security Category",
            color_discrete_map={
                "Excessive Permissions": DANGER_COLOR,
                "Excessive Roles": WARNING_COLOR,
                "High-Privilege Roles": SECONDARY_COLOR,
            },
        )
        fig.update_traces(
            textinfo="percent",
            textfont=dict(size=13, color="#ffffff"),
            marker=dict(line=dict(color=T["surface"], width=3)),
            hovertemplate=(
                "<b>%{label}</b><br>Findings: %{value}<br>"
                "Percentage: %{percent}<extra></extra>"
            ),
        )
        fig.add_annotation(
            text=f"<b>{total_findings:,}</b><br>"
            "<span style='font-size:11px'>findings</span>",
            x=0.5,
            y=0.5,
            font=dict(size=24, color=T["text"]),
            showarrow=False,
        )
        fig.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=60),
            font=dict(
                family='Inter, "Segoe UI", Arial, sans-serif', color=T["muted"]
            ),
            title=dict(font=dict(size=15, color=T["text"]), x=0.015),
            legend=dict(
                orientation="h",
                y=-0.12,
                x=0.5,
                xanchor="center",
                font=dict(color=T["muted"], size=11),
            ),
            hoverlabel=dict(
                bgcolor=T["surface_2"],
                bordercolor=T["border"],
                font=dict(color=T["text"]),
            ),
        )
        st.plotly_chart(fig, **WIDTH_KW)

    with summary_right:
        render_html('<div class="section-title">Security Risk Summary</div>')

        insight(
            "🔴 Excessive permissions",
            f"<b>{total_excessive_permissions:,}</b> findings. Users holding "
            "significantly more permissions than their peer group. These are the "
            "highest-value remediation targets because each one is a standing "
            "breach of least privilege.",
            "danger",
        )
        insight(
            "🟠 Excessive roles",
            f"<b>{total_excessive_roles:,}</b> findings. Accounts assigned an "
            "unusually high number of roles, typically the result of role "
            "accumulation across internal transfers.",
            "warning",
        )
        insight(
            "🟣 High-privilege roles",
            f"<b>{total_high_privilege_roles:,}</b> roles containing elevated or "
            "sensitive capabilities. Remediating a single over-scoped role clears "
            "the finding for every user who holds it.",
            "secondary",
        )


# ============================================================
# USER ANALYSIS
# ============================================================

elif page == "User Analysis":

    section(
        "👤 User Access Analysis",
        "Explore permission assignments and role distribution across users.",
    )

    tab_perm, tab_role = st.tabs(
        ["🔑 Permission Distribution", "👥 Role Distribution"]
    )

    with tab_perm:
        if not user_permission_distribution.empty:
            user_column = get_column(
                user_permission_distribution, ["username", "user_name", "user"]
            )
            permission_column = get_column(
                user_permission_distribution,
                ["permission_count", "permissions", "privilege_count", "count"],
            )

            filter_col1, filter_col2 = st.columns([2, 1])

            with filter_col1:
                search_term = st.text_input(
                    "Search for a user", placeholder="Enter username..."
                )

            filtered_data = user_permission_distribution.copy()

            if permission_column:
                perm_max = int(filtered_data[permission_column].max())
                perm_min = int(filtered_data[permission_column].min())
                with filter_col2:
                    if perm_max > perm_min:
                        threshold = st.slider(
                            "Minimum permission count",
                            min_value=perm_min,
                            max_value=perm_max,
                            value=perm_min,
                        )
                        filtered_data = filtered_data[
                            filtered_data[permission_column] >= threshold
                        ]

            if user_column and search_term:
                filtered_data = filtered_data[
                    filtered_data[user_column]
                    .astype(str)
                    .str.contains(search_term, case=False, na=False)
                ]

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric("Users Displayed", f"{len(filtered_data):,}")
            with metric_col2:
                if permission_column and not filtered_data.empty:
                    st.metric(
                        "Highest Permission Count",
                        f"{int(filtered_data[permission_column].max()):,}",
                    )
                else:
                    st.metric("Highest Permission Count", 0)
            with metric_col3:
                if permission_column and not filtered_data.empty:
                    st.metric(
                        "Median Permission Count",
                        f"{filtered_data[permission_column].median():.0f}",
                    )
                else:
                    st.metric("Median Permission Count", 0)

            if user_column and permission_column and not filtered_data.empty:
                fig = ranked_bar(
                    filtered_data,
                    user_column,
                    permission_column,
                    "Permission Count by User",
                    top_n=20,
                    color=T["primary"],
                    x_title="Permissions",
                    height=520,
                )
                st.plotly_chart(fig, **WIDTH_KW)

            show_dataframe(filtered_data, height=380)
            download_button(
                filtered_data,
                "⬇️ Download filtered users",
                "user_permission_distribution.csv",
                key="dl_user_perm",
            )
        else:
            st.warning("User permission analysis data was not found.")

    with tab_role:
        if not user_role_distribution.empty:
            user_column = get_column(
                user_role_distribution, ["username", "user_name", "user"]
            )
            role_count_column = get_column(
                user_role_distribution, ["role_count", "roles", "count"]
            )

            if user_column and role_count_column:
                m1, m2 = st.columns(2)
                with m1:
                    st.metric("Users Analyzed", f"{len(user_role_distribution):,}")
                with m2:
                    st.metric(
                        "Most Roles Held",
                        f"{int(user_role_distribution[role_count_column].max()):,}",
                    )

                fig = ranked_bar(
                    user_role_distribution,
                    user_column,
                    role_count_column,
                    "Roles Assigned to Users",
                    top_n=20,
                    color=T["secondary"],
                    x_title="Roles",
                    height=520,
                )
                st.plotly_chart(fig, **WIDTH_KW)

            show_dataframe(user_role_distribution, height=380)
            download_button(
                user_role_distribution,
                "⬇️ Download role distribution",
                "user_role_distribution.csv",
                key="dl_user_role",
            )
        else:
            st.info("User role distribution data was not found.")


# ============================================================
# ROLE ANALYSIS
# ============================================================

elif page == "Role Analysis":

    section(
        "🛡️ Role & Privilege Analysis",
        "Review roles, permission concentration, and high-privilege assignments.",
    )

    if not role_privilege_distribution.empty:
        role_column = get_column(
            role_privilege_distribution, ["role_name", "role", "name"]
        )
        privilege_column = get_column(
            role_privilege_distribution,
            ["permission_count", "privilege_count", "permissions", "count"],
        )

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Roles Analyzed", f"{len(role_privilege_distribution):,}")
        with metric_col2:
            if privilege_column:
                st.metric(
                    "Highest Privilege Count",
                    f"{int(role_privilege_distribution[privilege_column].max()):,}",
                )
            else:
                st.metric("Highest Privilege Count", 0)
        with metric_col3:
            if privilege_column:
                st.metric(
                    "Median Privilege Count",
                    f"{role_privilege_distribution[privilege_column].median():.0f}",
                )
            else:
                st.metric("Median Privilege Count", 0)

        if role_column and privilege_column:
            chart_col, dist_col = st.columns([1.5, 1])

            with chart_col:
                fig = ranked_bar(
                    role_privilege_distribution,
                    role_column,
                    privilege_column,
                    "Privilege Distribution Across Roles",
                    top_n=20,
                    color=T["secondary"],
                    x_title="Permissions",
                    height=520,
                )
                st.plotly_chart(fig, **WIDTH_KW)

            with dist_col:
                fig = px.histogram(
                    role_privilege_distribution,
                    x=privilege_column,
                    nbins=18,
                    title="Permission Count Spread",
                    color_discrete_sequence=[T["primary"]],
                )
                fig.update_traces(
                    marker_line_width=0,
                    marker=BAR_MARKER,
                    opacity=0.92,
                    hovertemplate="%{x} permissions<br>%{y} roles<extra></extra>",
                )
                apply_chart_style(
                    fig,
                    height=520,
                    xaxis_title="Permissions per role",
                    yaxis_title="Number of roles",
                )
                fig.update_layout(bargap=0.08)
                st.plotly_chart(fig, **WIDTH_KW)

        show_dataframe(role_privilege_distribution, height=380)
        download_button(
            role_privilege_distribution,
            "⬇️ Download role distribution",
            "role_privilege_distribution.csv",
            key="dl_role_dist",
        )
    else:
        st.warning("Role privilege distribution data was not found.")

    section("🚨 High-Privilege Roles")

    if not high_privilege_roles.empty:
        st.metric("High-Privilege Roles Identified", f"{len(high_privilege_roles):,}")
        show_dataframe(high_privilege_roles, height=420)
        download_button(
            high_privilege_roles,
            "⬇️ Download high-privilege roles",
            "high_privilege_roles.csv",
            key="dl_high_priv",
        )
    else:
        st.success("No high-privilege role findings were detected.")


# ============================================================
# SECURITY FINDINGS
# ============================================================

elif page == "Security Findings":

    section(
        "🚨 Security Findings",
        "Review potential excessive privileges, excessive role assignments, "
        "and elevated roles requiring additional security review.",
    )

    f1, f2, f3 = st.columns(3)
    with f1:
        st.metric("Excessive Permissions", f"{get_record_count(excessive_permissions):,}")
    with f2:
        st.metric("Excessive Roles", f"{get_record_count(excessive_roles):,}")
    with f3:
        st.metric("High-Privilege Roles", f"{get_record_count(high_privilege_roles):,}")

    tab1, tab2, tab3 = st.tabs(
        [
            "🔴 Excessive Permissions",
            "🟠 Excessive Roles",
            "🟣 High-Privilege Roles",
        ]
    )

    finding_tabs = [
        (
            tab1,
            excessive_permissions,
            "Users with Potentially Excessive Permissions",
            "excessive_permissions.csv",
            "dl_ep",
        ),
        (
            tab2,
            excessive_roles,
            "Users with Potentially Excessive Role Assignments",
            "excessive_roles.csv",
            "dl_er",
        ),
        (
            tab3,
            high_privilege_roles,
            "High-Privilege Roles",
            "high_privilege_roles.csv",
            "dl_hp",
        ),
    ]

    for tab, dataset, heading, filename, key in finding_tabs:
        with tab:
            render_html(f'<div class="section-title">{heading}</div>')

            if not dataset.empty:
                search = st.text_input(
                    "Filter these findings",
                    placeholder="Enter a keyword...",
                    key=f"search_{key}",
                )

                display = dataset.copy()

                if search:
                    mask = (
                        display.astype(str)
                        .apply(
                            lambda column: column.str.contains(
                                search, case=False, na=False
                            )
                        )
                        .any(axis=1)
                    )
                    display = display[mask]

                st.caption(f"Showing {len(display):,} of {len(dataset):,} findings.")
                show_dataframe(display, height=480)
                download_button(display, "⬇️ Download findings", filename, key=key)
            else:
                st.success("No findings were detected in this category.")


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    section(
        "🔎 Data Explorer",
        "Explore the source data and analysis results used throughout the dashboard.",
    )

    available_datasets = {
        "Users": users,
        "Roles": roles,
        "Permissions": permissions,
        "Resources": resources,
        "Excessive Permissions": excessive_permissions,
        "Excessive Roles": excessive_roles,
        "High-Privilege Roles": high_privilege_roles,
        "Role Privilege Distribution": role_privilege_distribution,
        "User Permission Distribution": user_permission_distribution,
        "User Role Distribution": user_role_distribution,
    }

    selected_dataset = st.selectbox(
        "Select a dataset", list(available_datasets.keys())
    )

    selected_data = available_datasets[selected_dataset]

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Records", f"{get_record_count(selected_data):,}")
    with metric_col2:
        cols = len(selected_data.columns) if not selected_data.empty else 0
        st.metric("Columns", f"{cols:,}")
    with metric_col3:
        missing = (
            int(selected_data.isna().sum().sum()) if not selected_data.empty else 0
        )
        st.metric("Missing Values", f"{missing:,}")

    if selected_data is not None and not selected_data.empty:

        search_data = st.text_input(
            "Search within selected dataset", placeholder="Enter a keyword..."
        )

        display_data = selected_data.copy()

        if search_data:
            mask = (
                display_data.astype(str)
                .apply(
                    lambda column: column.str.contains(
                        search_data, case=False, na=False
                    )
                )
                .any(axis=1)
            )
            display_data = display_data[mask]

        st.caption(
            f"Displaying {len(display_data):,} of {len(selected_data):,} records."
        )

        show_dataframe(display_data, height=500)

        download_button(
            display_data,
            "⬇️ Download Filtered CSV",
            selected_dataset.lower().replace(" ", "_") + ".csv",
            key="dl_explorer",
        )

        with st.expander("Column profile"):
            profile = pd.DataFrame(
                {
                    "Column": selected_data.columns,
                    "Type": [str(d) for d in selected_data.dtypes],
                    "Missing": selected_data.isna().sum().values,
                    "Unique": selected_data.nunique(dropna=True).values,
                }
            )
            st.dataframe(profile, hide_index=True, **WIDTH_KW)
    else:
        st.info("No data is available for this dataset.")


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer-box">
    🔐 <b>Access Control &amp; Privilege Analysis</b>
    &nbsp;&nbsp;|&nbsp;&nbsp; RBAC Security Analytics
    &nbsp;&nbsp;|&nbsp;&nbsp; Least Privilege Review
    </div>
    """
)
# ============================================================
# SQL DATABASE ANALYSIS
# ============================================================

import sqlite3
from pathlib import Path

st.divider()

st.markdown("## 🗄️ SQL Database Analysis")
st.caption("Live SQL queries from the Access Control SQLite database")

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "access_control.db"

try:
    conn = sqlite3.connect(DB_PATH)

    # SQL database statistics
    sql_users = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM users",
        conn
    ).iloc[0]["total"]

    sql_roles = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM roles",
        conn
    ).iloc[0]["total"]

    sql_permissions = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM permissions",
        conn
    ).iloc[0]["total"]

    sql_resources = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM resources",
        conn
    ).iloc[0]["total"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("SQL Users", sql_users)

    with col2:
        st.metric("SQL Roles", sql_roles)

    with col3:
        st.metric("SQL Permissions", sql_permissions)

    with col4:
        st.metric("SQL Resources", sql_resources)

    st.markdown("### 🔍 Top Roles by Permission Count")

    top_roles_sql = pd.read_sql_query(
        """
        SELECT
            role_id,
            COUNT(permission_id) AS permission_count
        FROM role_permissions
        GROUP BY role_id
        ORDER BY permission_count DESC
        LIMIT 10
        """,
        conn
    )

    st.dataframe(top_roles_sql, use_container_width=True)

    st.success(
        "SQL database connected successfully — "
        "using SELECT, COUNT, GROUP BY, and ORDER BY queries."
    )

    conn.close()

except Exception as e:
    st.error(f"SQL database connection error: {e}")