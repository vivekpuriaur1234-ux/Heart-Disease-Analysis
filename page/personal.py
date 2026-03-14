"""pages/personal.py — Personal Health Monitor (Anita scenario)"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_utils import load_data

SURFACE = "#161b22"; SURFACE2 = "#1c2333"; BORDER = "#30363d"
TEXT = "#e6edf3"; MUTED = "#8b949e"
RED = "#e05252"; BLUE = "#4c9be8"; GREEN = "#3fb950"; AMBER = "#d29922"

BENCHMARKS = {
    "chol":     {"label": "Cholesterol",     "unit": "mg/dL",  "safe": 200, "warning": 240, "critical": 300},
    "trestbps": {"label": "Resting BP",       "unit": "mmHg",   "safe": 120, "warning": 140, "critical": 180},
    "thalach":  {"label": "Max Heart Rate",   "unit": "bpm",    "safe": 150, "warning": 130, "critical": 110},
    "oldpeak":  {"label": "ST Depression",    "unit": "",       "safe": 1.0, "warning": 2.0, "critical": 3.5},
}


def gauge(value, title, safe, warning, critical, unit="", reverse=False):
    """Build a Plotly gauge indicator."""
    if reverse:
        color = GREEN if value >= safe else (AMBER if value >= warning else RED)
    else:
        color = GREEN if value <= safe else (AMBER if value <= warning else RED)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": f"{title}<br><span style='font-size:0.75em;color:{MUTED}'>{unit}</span>",
               "font": {"size": 13, "color": TEXT}},
        number={"font": {"color": color, "size": 26, "family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0, critical * 1.4], "tickcolor": MUTED, "tickfont": {"color": MUTED, "size": 10}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": SURFACE2,
            "bordercolor": BORDER,
            "steps": [
                {"range": [0, safe],     "color": "rgba(63,185,80,0.15)"},
                {"range": [safe, warning], "color": "rgba(210,153,34,0.15)"},
                {"range": [warning, critical * 1.4], "color": "rgba(224,82,82,0.15)"},
            ],
            "threshold": {"line": {"color": RED, "width": 2}, "thickness": 0.7, "value": warning},
        },
    ))
    fig.update_layout(paper_bgcolor=SURFACE, height=220,
                      margin=dict(l=30, r=30, t=60, b=10),
                      font=dict(color=TEXT))
    return fig


def risk_radar(user_vals: dict, pop_avg: dict) -> go.Figure:
    cats = ["Age Factor", "Cholesterol", "Blood Pressure", "Heart Rate", "ST Depression", "Vessels"]
    user  = [user_vals.get(c, 0.5) for c in cats]
    avg   = [pop_avg.get(c, 0.5)   for c in cats]
    fig = go.Figure()
    for vals, name, color in [(avg, "Population Avg", BLUE), (user, "Your Profile", RED)]:
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", name=name,
            line=dict(color=color, width=2),
            fillcolor=color.replace(")", ",0.15)").replace("rgb(", "rgba(")
                      if "rgb" in color else color + "26",
        ))
    fig.update_layout(
        polar=dict(
            bgcolor=SURFACE2,
            radialaxis=dict(visible=True, range=[0, 1], color=MUTED, gridcolor=BORDER),
            angularaxis=dict(color=TEXT, gridcolor=BORDER),
        ),
        paper_bgcolor=SURFACE, height=340,
        margin=dict(l=40, r=40, t=30, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
        font=dict(color=TEXT),
    )
    return fig


def render():
    df = load_data()

    st.markdown("""
    <div style="padding: 20px 0 8px;">
      <h1 style="font-family:'DM Serif Display',serif; font-size:2.2rem; margin:0;">
        👤 Personal Health Monitor
      </h1>
      <p style="color:#8b949e; margin-top:6px;">
        Enter your health metrics below and see how your risk profile compares
        to clinical benchmarks. Inspired by <b style="color:#e6edf3">Anita</b>'s self-monitoring scenario.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Panel ───────────────────────────────────────────────────────────
    with st.expander("📝 Enter Your Health Metrics", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            age       = st.number_input("Age (years)",         20, 90, 45)
            sex_str   = st.selectbox("Sex", ["Female", "Male"])
            cp_str    = st.selectbox("Chest Pain Type",
                                     ["Asymptomatic", "Typical Angina", "Atypical Angina", "Non-Anginal Pain"])
        with col2:
            chol      = st.number_input("Cholesterol (mg/dL)", 100, 600, 220)
            trestbps  = st.number_input("Resting BP (mmHg)",   80, 250, 130)
            fbs_str   = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No", "Yes"])
        with col3:
            thalach   = st.number_input("Max Heart Rate (bpm)", 60, 220, 155)
            oldpeak   = st.number_input("ST Depression (oldpeak)", 0.0, 8.0, 1.0, step=0.1)
            exang_str = st.selectbox("Exercise-Induced Angina", ["No", "Yes"])
            ca        = st.slider("Major Vessels (0–3)", 0, 3, 0)

    # ── Derived values ────────────────────────────────────────────────────────
    sex   = 1 if sex_str == "Male" else 0
    fbs   = 1 if fbs_str == "Yes" else 0
    exang = 1 if exang_str == "Yes" else 0
    cp_map_rev = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal Pain": 2, "Asymptomatic": 3}
    cp = cp_map_rev[cp_str]

    risk_score = round(
        (chol / 240) + (trestbps / 140) + exang * 0.8 + ca * 0.3 +
        max(0, (220 - age - thalach) / 50), 2
    )

    risk_level = "LOW"   if risk_score < 2.5 else \
                 "MEDIUM" if risk_score < 4.0 else "HIGH"
    risk_color = GREEN if risk_level == "LOW" else (AMBER if risk_level == "MEDIUM" else RED)

    # ── Risk Score Hero ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:{SURFACE2}; border:1px solid {BORDER}; border-radius:16px;
                padding:24px 32px; margin:20px 0; display:flex; align-items:center; gap:32px;">
      <div>
        <div style="font-size:0.72rem; color:{MUTED}; text-transform:uppercase; letter-spacing:0.1em;">
          Composite Risk Score
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:3.5rem; font-weight:700; color:{risk_color}; line-height:1;">
          {risk_score}
        </div>
        <div style="margin-top:8px;">
          <span class="badge badge-{'red' if risk_level=='HIGH' else ('blue' if risk_level=='LOW' else '')}"
                style="font-size:0.85rem; padding:4px 14px;">
            {risk_level} RISK
          </span>
        </div>
      </div>
      <div style="flex:1; color:{MUTED}; font-size:0.9rem; line-height:1.7;">
        Your risk score is computed from cholesterol, blood pressure, exercise angina,
        coronary vessels, and heart rate reserve relative to your age. A score below 2.5
        is considered low risk; 2.5–4.0 moderate; above 4.0 requires clinical follow-up.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Gauge Row ─────────────────────────────────────────────────────────────
    st.markdown("#### 📊 Your Metrics vs. Clinical Thresholds")
    g1, g2, g3, g4 = st.columns(4)
    with g1: st.plotly_chart(gauge(chol,     "Cholesterol",   200, 240, 350, "mg/dL"),  use_container_width=True)
    with g2: st.plotly_chart(gauge(trestbps, "Resting BP",    120, 140, 200, "mmHg"),   use_container_width=True)
    with g3: st.plotly_chart(gauge(thalach,  "Max Heart Rate",150, 130, 100, "bpm", reverse=True), use_container_width=True)
    with g4: st.plotly_chart(gauge(oldpeak,  "ST Depression", 1.0, 2.0, 4.0, ""),       use_container_width=True)

    # ── Radar vs Population ───────────────────────────────────────────────────
    pop_avg_age_factor = float(df["age"].mean() / 77)
    pop_avg = {
        "Age Factor":      pop_avg_age_factor,
        "Cholesterol":     float(df["chol"].mean() / 400),
        "Blood Pressure":  float(df["trestbps"].mean() / 200),
        "Heart Rate":      1 - float(df["thalach"].mean() / 210),
        "ST Depression":   float(df["oldpeak"].mean() / 6),
        "Vessels":         float(df["ca"].mean() / 3),
    }
    user_vals = {
        "Age Factor":      age / 77,
        "Cholesterol":     min(chol / 400, 1),
        "Blood Pressure":  min(trestbps / 200, 1),
        "Heart Rate":      1 - min(thalach / 210, 1),
        "ST Depression":   min(oldpeak / 6, 1),
        "Vessels":         ca / 3,
    }

    col_rad, col_sim = st.columns([1, 1])
    with col_rad:
        st.markdown("#### 🕸️ Risk Radar vs Population Average")
        st.plotly_chart(risk_radar(user_vals, pop_avg), use_container_width=True)

    with col_sim:
        st.markdown("#### 👥 Similar Patient Outcomes")
        # Find similar patients
        similar = df[
            (df["age"].between(age - 8, age + 8)) &
            (df["sex"] == sex) &
            (df["chol"].between(chol - 50, chol + 50))
        ]
        if len(similar) >= 5:
            sim_prev = round(similar["target"].mean() * 100, 1)
            sim_count = len(similar)
            fig_sim = px.histogram(similar, x="risk_score", color="disease_label",
                                   nbins=15, barmode="overlay", opacity=0.75,
                                   color_discrete_map={"Heart Disease": RED, "Healthy": BLUE},
                                   labels={"risk_score": "Risk Score", "disease_label": ""})
            fig_sim.add_vline(x=risk_score, line_dash="solid", line_color="#d29922",
                              annotation_text=f"You ({risk_score})", annotation_font_color="#d29922")
            fig_sim.update_layout(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
                                  font=dict(color=MUTED, size=11), height=260,
                                  margin=dict(l=20, r=20, t=20, b=20),
                                  xaxis=dict(gridcolor=BORDER), yaxis=dict(gridcolor=BORDER),
                                  legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_sim, use_container_width=True)
            st.markdown(f"""
            <div style="color:{MUTED}; font-size:0.85rem; text-align:center;">
              Among <b style="color:{TEXT}">{sim_count}</b> similar patients
              (age ±8, same sex, chol ±50), <b style="color:{RED}">{sim_prev}%</b>
              have heart disease.
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Not enough similar patients found for comparison. Adjust your inputs.")

    # ── Action Plan ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <span class="icon">🎯</span><h2>Personalised Action Plan</h2>
    </div>
    """, unsafe_allow_html=True)

    actions = []
    if chol > 240:
        actions.append(("danger", "🥗 Reduce Dietary Fats", f"Your cholesterol ({chol} mg/dL) exceeds the high-risk threshold of 240 mg/dL. Target a Mediterranean diet: reduce saturated fats, increase fibre, omega-3 rich fish."))
    if trestbps > 130:
        actions.append(("warning", "🧂 Lower Sodium Intake", f"Resting BP of {trestbps} mmHg is elevated. Reduce sodium to <2,300 mg/day. Aerobic exercise 150 min/week can lower BP by 5–8 mmHg."))
    if exang == 1:
        actions.append(("danger", "🏥 Cardiology Referral", "Exercise-induced angina is a significant warning sign. Consult a cardiologist for stress-test evaluation and medication review within 30 days."))
    if thalach < 140:
        actions.append(("warning", "🏃 Improve Cardiovascular Fitness", f"Max heart rate of {thalach} bpm is below target for your age. Gradual aerobic conditioning (walking, cycling) 3–5× per week."))
    if not actions:
        actions.append(("success", "✅ Maintain Current Lifestyle", f"Your indicators are within healthy ranges. Continue regular check-ups (annual BP and cholesterol screening) and maintain your current activity level."))

    cols_act = st.columns(min(len(actions), 3))
    for col, (cls, title, text) in zip(cols_act, actions[:3]):
        with col:
            st.markdown(f"""
            <div class="insight-box {cls}">
              <b style="color:#e6edf3">{title}</b><br>
              <span style="color:#8b949e">{text}</span>
            </div>
            """, unsafe_allow_html=True)
