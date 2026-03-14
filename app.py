"""
Heart Disease Analysis — Streamlit + Gemini Application
Run:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="CardioInsight AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1c2333;
    --border:    #30363d;
    --red:       #e05252;
    --red-glow:  rgba(224,82,82,0.18);
    --blue:      #4c9be8;
    --blue-glow: rgba(76,155,232,0.15);
    --green:     #3fb950;
    --amber:     #d29922;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --font-serif: 'DM Serif Display', Georgia, serif;
    --font-sans:  'DM Sans', system-ui, sans-serif;
    --font-mono:  'JetBrains Mono', monospace;
  }

  html, body, [data-testid="stAppViewContainer"],
  [data-testid="stMain"], section.main { background: var(--bg) !important; }

  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }

  * { font-family: var(--font-sans); color: var(--text); }

  h1 { font-family: var(--font-serif) !important; }
  h2, h3 { font-family: var(--font-sans) !important; font-weight: 600 !important; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
  }
  [data-testid="stMetricValue"] { font-family: var(--font-mono) !important; font-size: 2rem !important; }
  [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.08em; }

  /* Tabs */
  [data-testid="stTabs"] button {
    font-family: var(--font-sans) !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
  }
  [data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom-color: var(--blue) !important;
    background: transparent !important;
  }

  /* Select / Input */
  [data-baseweb="select"] > div,
  [data-baseweb="input"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
  }

  /* Buttons */
  [data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--blue), #7b68ee) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
  }
  [data-testid="stButton"] > button:hover { opacity: 0.88 !important; }

  /* Expanders / Containers */
  [data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
  }

  /* Chat messages */
  [data-testid="stChatMessage"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* Divider */
  hr { border-color: var(--border) !important; }

  /* Plotly charts background */
  .js-plotly-plot .plotly { background: transparent !important; }

  /* Sidebar nav links */
  .nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 14px; border-radius: 8px;
    margin-bottom: 4px; cursor: pointer;
    font-size: 0.9rem; font-weight: 500;
    transition: background 0.15s;
    text-decoration: none; color: var(--muted);
  }
  .nav-item:hover { background: var(--surface2); color: var(--text); }
  .nav-item.active { background: var(--blue-glow); color: var(--blue); }

  .kpi-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
  }
  .kpi-card .kpi-value { font-family: var(--font-mono); font-size: 2.2rem; font-weight: 600; }
  .kpi-card .kpi-label { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
  .kpi-card .kpi-sub { font-size: 0.85rem; color: var(--muted); margin-top: 2px; }

  .section-header {
    display: flex; align-items: center; gap: 12px;
    margin: 24px 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }
  .section-header .icon { font-size: 1.4rem; }
  .section-header h2 { margin: 0; font-size: 1.3rem; }

  .insight-box {
    background: var(--surface2);
    border-left: 3px solid var(--blue);
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.9rem;
    line-height: 1.6;
  }
  .insight-box.warning { border-left-color: var(--amber); }
  .insight-box.danger  { border-left-color: var(--red); }
  .insight-box.success { border-left-color: var(--green); }

  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .badge-red   { background: var(--red-glow);  color: var(--red); }
  .badge-blue  { background: var(--blue-glow); color: var(--blue); }
  .badge-green { background: rgba(63,185,80,0.15); color: var(--green); }

  /* Sidebar logo */
  .sidebar-logo {
    padding: 8px 0 20px;
    text-align: center;
  }
  .sidebar-logo .logo-text {
    font-family: var(--font-serif);
    font-size: 1.6rem;
    background: linear-gradient(135deg, var(--red), #ff8c69);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .sidebar-logo .logo-sub { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.15em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ─── Import pages ─────────────────────────────────────────────────────────────
import page.overview as overview
import page.clinical as clinical
import page.policy as policy
import page.personal as personal
import page.gemini_chat as gemini_chat
import page.story as story

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="logo-text">🫀 CardioInsight</div>
      <div class="logo-sub">AI-Powered Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigate",
        options=[
            "🏠  Overview",
            "🩺  Clinical Analysis",
            "🏛️  Policy Dashboard",
            "👤  Personal Monitor",
            "📖  Data Story",
            "🤖  Gemini AI Assistant",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("""
    <div style="padding: 12px; background: #161b22; border-radius: 10px; border: 1px solid #30363d; font-size: 0.78rem; color: #8b949e; line-height: 1.6;">
      <b style="color:#e6edf3">Data Source</b><br>
      UCI Heart Disease Dataset<br>
      303 patient records · 14 features<br><br>
      <b style="color:#e6edf3">Tools</b><br>
      Python · Streamlit · Plotly<br>
      Google Gemini AI
    </div>
    """, unsafe_allow_html=True)

# ─── Router ───────────────────────────────────────────────────────────────────
if   "Overview"    in page: overview.render()
elif "Clinical"    in page: clinical.render()
elif "Policy"      in page: policy.render()
elif "Personal"    in page: personal.render()
elif "Story"       in page: story.render()
elif "Gemini"      in page: gemini_chat.render()
