"""pages/story.py — Data Story with 7 narrative scenes"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_utils import load_data
from utils.charts import (bar_age_group, scatter_chol_hr, heatmap_cp_disease,
                           bubble_risk, treemap_thal, boxplot_chol_age, histogram_hr)

SURFACE = "#161b22"; BORDER = "#30363d"; TEXT = "#e6edf3"; MUTED = "#8b949e"
RED = "#e05252"; BLUE = "#4c9be8"; GREEN = "#3fb950"; AMBER = "#d29922"


def render():
    df = load_data()

    st.markdown("""
    <div style="padding:20px 0 8px;">
      <h1 style="font-family:'DM Serif Display',serif; font-size:2.4rem; margin:0; font-style:italic;">
        "The Heart Disease Journey"
      </h1>
      <p style="color:#8b949e; margin-top:6px; font-size:1rem;">
        A 7-scene data story — from raw numbers to life-saving insights.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Scene selector
    scenes = [
        "🎬 Scene 1 · Setting the Stage",
        "👥 Scene 2 · Who Is at Risk?",
        "⚠️  Scene 3 · The Warning Signs",
        "🏃 Scene 4 · Lifestyle Factors",
        "🗺️  Scene 5 · Population Patterns",
        "💊 Scene 6 · What Can Be Done?",
        "🎯 Scene 7 · Your Action Plan",
    ]

    col_nav, col_main = st.columns([1, 3])

    with col_nav:
        st.markdown("<br>", unsafe_allow_html=True)
        scene_idx = st.radio("Story Scenes", scenes, label_visibility="collapsed")

    with col_main:
        idx = scenes.index(scene_idx)

        if idx == 0:
            _scene_1(df)
        elif idx == 1:
            _scene_2(df)
        elif idx == 2:
            _scene_3(df)
        elif idx == 3:
            _scene_4(df)
        elif idx == 4:
            _scene_5(df)
        elif idx == 5:
            _scene_6(df)
        else:
            _scene_7(df)

    # Navigation buttons at bottom
    st.markdown("<br>", unsafe_allow_html=True)
    b1, _, b2 = st.columns([1, 5, 1])
    if idx > 0:
        with b1:
            if st.button("← Previous"):
                st.session_state["_story_scene"] = idx - 1
    if idx < 6:
        with b2:
            if st.button("Next →"):
                st.session_state["_story_scene"] = idx + 1


def _scene_header(icon, scene, title, body):
    st.markdown(f"""
    <div style="background:{SURFACE}; border:1px solid {BORDER}; border-radius:14px;
                padding:22px 28px; margin-bottom:20px;">
      <div style="font-size:0.72rem; color:{MUTED}; text-transform:uppercase; letter-spacing:0.12em;">
        {scene}
      </div>
      <h2 style="margin:6px 0 10px; font-family:'DM Serif Display',serif; font-size:1.9rem;">
        {icon} {title}
      </h2>
      <p style="color:{MUTED}; font-size:0.95rem; line-height:1.7; max-width:680px; margin:0;">
        {body}
      </p>
    </div>
    """, unsafe_allow_html=True)


def _scene_1(df):
    total = len(df)
    pos   = int(df["target"].sum())
    prev  = round(pos / total * 100, 1)
    avg_age = round(df["age"].mean(), 1)

    _scene_header("🫀", "Scene 1 of 7", "Setting the Stage",
        f"Heart disease is not abstract — it affects <b style='color:{RED}'>{pos} of {total}</b> "
        f"patients in this dataset, a prevalence of <b style='color:{RED}'>{prev}%</b>. "
        "Worldwide, 17.9 million people die from cardiovascular disease every year. "
        "This story follows the data to understand why — and what can be done.")

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, color in [
        (c1, f"{pos}", "Positive Cases", RED),
        (c2, f"{prev}%", "Prevalence",  RED),
        (c3, f"{avg_age}", "Average Age",  AMBER),
        (c4, f"{round(df[df['target']==1]['sex'].mean()*100)}%", "Male (Positive)", BLUE),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary donut
    fig = go.Figure(go.Pie(
        values=[pos, total - pos], labels=["Heart Disease", "Healthy"],
        hole=0.7, marker_colors=[RED, BLUE],
        marker=dict(line=dict(color=SURFACE, width=3))
    ))
    fig.update_layout(paper_bgcolor=SURFACE, height=300,
                      margin=dict(l=20, r=20, t=20, b=20),
                      font=dict(color=TEXT),
                      annotations=[dict(text=f"<b>{prev}%</b><br>Prevalence",
                                        font_size=16, font_color=RED, showarrow=False)])
    st.plotly_chart(fig, use_container_width=True)


def _scene_2(df):
    _scene_header("👥", "Scene 2 of 7", "Who Is at Risk?",
        "The data reveals a clear demographic fingerprint: middle-aged men carry a "
        "disproportionate share of risk. But the story is more nuanced — "
        "women's risk surges after 55, often masked by different symptom presentations.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(bar_age_group(df), use_container_width=True)
    with col_b:
        # Gender x Age prevalence
        g = df.groupby(["age_group", "gender"])["target"].mean().reset_index()
        g["prevalence"] = (g["target"] * 100).round(1)
        fig = px.bar(g, x="age_group", y="prevalence", color="gender",
                     barmode="group", color_discrete_map={"Male": BLUE, "Female": "#c788e5"},
                     labels={"age_group": "Age Group", "prevalence": "Prevalence (%)", "gender": ""},
                     text="prevalence")
        fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig.update_layout(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE, height=380,
                          font=dict(color=MUTED, size=11), margin=dict(l=20,r=20,t=44,b=20),
                          title=dict(text="Prevalence by Gender & Age", font=dict(size=15, color=TEXT)),
                          xaxis=dict(gridcolor=BORDER), yaxis=dict(gridcolor=BORDER),
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

    male_prev = round(df[df["sex"]==1]["target"].mean()*100, 1)
    fem_prev  = round(df[df["sex"]==0]["target"].mean()*100, 1)
    st.markdown(f"""
    <div class="insight-box danger">
      <b style="color:#e6edf3">Gender Divergence</b> — Male prevalence is <b style="color:{RED}">{male_prev}%</b>
      vs Female <b style="color:#c788e5">{fem_prev}%</b> overall. However, post-menopausal women in the 55–70
      range show rapidly converging risk — a clinical window often missed in standard screening protocols.
    </div>
    """, unsafe_allow_html=True)


def _scene_3(df):
    _scene_header("⚠️", "Scene 3 of 7", "The Warning Signs",
        "Not all chest pain is created equal. The data tells a counter-intuitive story: "
        "the patients presenting as asymptomatic are the most at risk. "
        "Meanwhile, cholesterol and heart rate form a revealing two-axis danger zone.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(heatmap_cp_disease(df), use_container_width=True)
    with col_b:
        st.plotly_chart(scatter_chol_hr(df), use_container_width=True)

    asym_prev = round(df[df["cp"]==3]["target"].mean()*100, 1)
    st.markdown(f"""
    <div class="insight-box danger">
      <b style="color:#e6edf3">⚡ The Silent Killer</b> — Asymptomatic chest pain (Type 3) carries a
      <b style="color:{RED}">{asym_prev}%</b> disease prevalence. These patients present no classic
      warning symptoms yet harbour the highest risk. Routine screening beyond symptom-based triage
      is critical for this subgroup.
    </div>
    """, unsafe_allow_html=True)


def _scene_4(df):
    _scene_header("🏃", "Scene 4 of 7", "Lifestyle Factors",
        "The data exposes lifestyle as a powerful modifiable variable. "
        "Exercise-induced angina, elevated blood pressure, and cholesterol interact in "
        "compounding ways — and the risk score bubble chart makes this devastatingly clear.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(bubble_risk(df), use_container_width=True)
    with col_b:
        from utils.charts import line_age_bp
        st.plotly_chart(line_age_bp(df), use_container_width=True)

    exang_prev = round(df[df["exang"]==1]["target"].mean()*100, 1)
    st.markdown(f"""
    <div class="insight-box warning">
      <b style="color:#e6edf3">🏋️ Exercise Angina Signal</b> — Patients with exercise-induced angina
      show <b style="color:{AMBER}">{exang_prev}%</b> disease prevalence. Combined with rising BP trends
      post-age 50, this strongly implicates sedentary lifestyle as a major, addressable risk driver.
    </div>
    """, unsafe_allow_html=True)


def _scene_5(df):
    _scene_header("🗺️", "Scene 5 of 7", "Population Patterns",
        "Zooming out to the population level, we see structural patterns in thalassemia type "
        "distribution and how risk compounds across cohorts. "
        "These insights underpin evidence-based public health policy.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(treemap_thal(df), use_container_width=True)
    with col_b:
        from utils.charts import prevalence_bar
        st.plotly_chart(prevalence_bar(df), use_container_width=True)

    thal2_prev = round(df[df["thal"]==2]["target"].mean()*100, 1)
    st.markdown(f"""
    <div class="insight-box">
      <b style="color:#e6edf3">🧬 Thalassemia Type 2 (Reversible Defect)</b> — Shows the highest
      disease association at <b style="color:{BLUE}">{thal2_prev}%</b> prevalence. This genetic marker
      should be integrated into population-level screening models and incorporated into primary
      care risk stratification tools.
    </div>
    """, unsafe_allow_html=True)


def _scene_6(df):
    _scene_header("💊", "Scene 6 of 7", "What Can Be Done?",
        "Prevention is not just possible — the data shows exactly where to intervene. "
        "Cholesterol distribution, heart rate patterns, and risk stratification "
        "all point to actionable clinical and lifestyle targets.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(boxplot_chol_age(df), use_container_width=True)
    with col_b:
        st.plotly_chart(histogram_hr(df), use_container_width=True)

    st.markdown(f"""
    <div class="insight-box success">
      <b style="color:#e6edf3">✅ The Intervention Window</b> — The 40–60 age group shows the widest
      interquartile range in cholesterol (highest variability = highest modifiability). This is
      the optimal window for dietary intervention, statin therapy consideration, and structured
      fitness programmes. Addressing cholesterol in this decade of life yields the greatest
      population-level cardiovascular benefit.
    </div>
    """, unsafe_allow_html=True)


def _scene_7(df):
    _scene_header("🎯", "Scene 7 of 7", "Your Action Plan",
        "The story ends where it matters most — with you. The data has shown us the patterns. "
        "Now it's time to translate insights into action. "
        "Navigate to the Personal Monitor to build your individual risk profile.")

    # Final summary scorecard
    stats = {
        "Highest Risk Age Group":     "50–60 years",
        "Strongest Single Predictor": "Asymptomatic Chest Pain (Type 3)",
        "Most Modifiable Factor":     "Cholesterol in 40–60 cohort",
        "Gender Watch Window":        "Post-menopausal women (55–70)",
        "Population Intervention":    "Sedentary lifestyle & tobacco control",
        "Genetic Screening Priority": "Thalassemia Type 2 (Reversible Defect)",
    }

    for key, val in stats.items():
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:12px 18px; background:{SURFACE}; border:1px solid {BORDER};
                    border-radius:8px; margin-bottom:8px;">
          <span style="color:{MUTED}; font-size:0.88rem;">{key}</span>
          <span style="color:{TEXT}; font-weight:600; font-size:0.9rem;">{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #1a2a3a, #2a1a3a);
                border:1px solid {BORDER}; border-radius:14px;
                padding:28px 32px; text-align:center;">
      <div style="font-family:'DM Serif Display',serif; font-size:1.8rem; color:{TEXT}; margin-bottom:12px;">
        Ready to check your own risk?
      </div>
      <p style="color:{MUTED}; max-width:500px; margin:0 auto 16px;">
        Head to the <b style="color:{BLUE}">Personal Monitor</b> page, enter your metrics,
        and get a tailored action plan — or ask the <b style="color:{RED}">Gemini AI Assistant</b>
        any question about your results.
      </p>
      <div style="font-size:2rem;">🫀 🤖 📊</div>
    </div>
    """, unsafe_allow_html=True)
