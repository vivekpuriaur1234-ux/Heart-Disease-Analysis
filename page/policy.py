"""pages/policy.py — Population Health & Policy Dashboard (Ramesh scenario)"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_utils import load_data, filter_df
from utils.charts import (line_age_bp, treemap_thal, dual_axis_bp_oldpeak,
                           bubble_risk, prevalence_bar, correlation_heatmap)

SURFACE = "#161b22"; BORDER = "#30363d"; TEXT = "#e6edf3"; MUTED = "#8b949e"
RED = "#e05252"; BLUE = "#4c9be8"; GREEN = "#3fb950"; AMBER = "#d29922"


def render():
    df = load_data()

    st.markdown("""
    <div style="padding: 20px 0 8px;">
      <h1 style="font-family:'DM Serif Display',serif; font-size:2.2rem; margin:0;">
        🏛️ Population Health & Policy
      </h1>
      <p style="color:#8b949e; margin-top:6px;">
        Evidence-based policy intelligence for public health decision-makers.
        Built for <b style="color:#e6edf3">Ramesh</b>'s government health department scenario.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🏛️ Policy Filters")
        age_range = st.slider("Age Range", 20, 80, (29, 77), key="policy_age")
        chol_cat  = st.selectbox("Cholesterol Category", ["All", "Normal", "Borderline", "High"], key="policy_chol")
        exang     = st.selectbox("Exercise-Induced Angina", ["All", "Yes", "No"], key="policy_exang")

    filtered = filter_df(df, age_range, "All", "All", chol_cat)
    if exang == "Yes":
        filtered = filtered[filtered["exang"] == 1]
    elif exang == "No":
        filtered = filtered[filtered["exang"] == 0]

    # ── Headline stats ────────────────────────────────────────────────────────
    total    = len(filtered)
    prev     = round(filtered["target"].mean() * 100, 1) if total else 0
    high_bp  = round((filtered["trestbps"] > 140).mean() * 100, 1) if total else 0
    high_ch  = round((filtered["chol"] > 240).mean() * 100, 1) if total else 0
    sedent   = round(filtered["exang"].mean() * 100, 1) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, color, sub in [
        (c1, f"{prev}%",    "Disease Prevalence", RED,   f"of {total} patients"),
        (c2, f"{high_bp}%", "Hypertension Rate",  AMBER, "BP > 140 mmHg"),
        (c3, f"{high_ch}%", "High Cholesterol",   AMBER, "Chol > 240 mg/dL"),
        (c4, f"{sedent}%",  "Exertional Angina",  BLUE,  "exercise-induced"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-label">{lbl}</div>
              <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺️ Population Patterns", "🔗 Risk Correlations"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(line_age_bp(filtered), use_container_width=True)
        with col_b:
            st.plotly_chart(prevalence_bar(filtered), use_container_width=True)
        st.plotly_chart(dual_axis_bp_oldpeak(filtered), use_container_width=True)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            st.plotly_chart(treemap_thal(filtered), use_container_width=True)
        with col_d:
            st.plotly_chart(bubble_risk(filtered), use_container_width=True)

        # Population breakdown table
        st.markdown("#### Population Breakdown by Age Group")
        pop = filtered.groupby("age_group").agg(
            Total=("age", "count"),
            Disease=("target", "sum"),
            Healthy=("target", lambda x: (x == 0).sum()),
            Prevalence=("target", lambda x: f"{round(x.mean()*100,1)}%"),
            Avg_Chol=("chol", lambda x: round(x.mean(),1)),
            Avg_BP=("trestbps", lambda x: round(x.mean(),1)),
        ).reset_index()
        pop.columns = ["Age Group", "Total", "Disease", "Healthy", "Prevalence", "Avg Cholesterol", "Avg BP"]
        st.dataframe(pop, use_container_width=True, hide_index=True)

    with tab3:
        st.plotly_chart(correlation_heatmap(filtered), use_container_width=True)

        # Lifestyle factor impact
        st.markdown("#### Lifestyle Factor Impact on Disease Rate")
        factors = {
            "Fasting Blood Sugar > 120": filtered.groupby("fbs")["target"].mean().get(1, 0),
            "Exercise-Induced Angina":   filtered.groupby("exang")["target"].mean().get(1, 0),
            "High Cholesterol (>240)":   filtered[filtered["chol"]>240]["target"].mean(),
            "Hypertension (BP>140)":     filtered[filtered["trestbps"]>140]["target"].mean(),
            "Asymptomatic Chest Pain":   filtered[filtered["cp"]==3]["target"].mean(),
        }
        factor_df = pd.DataFrame(list(factors.items()), columns=["Factor", "Disease Rate"])
        factor_df["Disease Rate"] = (factor_df["Disease Rate"] * 100).round(1)
        factor_df = factor_df.sort_values("Disease Rate", ascending=True)
        fig = px.bar(factor_df, x="Disease Rate", y="Factor", orientation="h",
                     color="Disease Rate",
                     color_continuous_scale=[[0, BLUE], [0.5, AMBER], [1, RED]],
                     text="Disease Rate", labels={"Disease Rate": "Disease Rate (%)"})
        fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig.update_layout(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
                          font=dict(color=MUTED, size=11), height=300,
                          margin=dict(l=20, r=40, t=20, b=20),
                          yaxis=dict(color=TEXT), xaxis=dict(color=MUTED, gridcolor=BORDER))
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Policy Recommendations ─────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <span class="icon">📋</span><h2>Evidence-Based Policy Recommendations</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    recs = [
        ("danger",  "🚬 Tobacco Control",
         f"Exercise-induced angina affects {sedent}% of this cohort, strongly correlated with smoking. Recommend stricter tobacco regulations and subsidized cessation programs in high-prevalence age groups."),
        ("warning", "🏃 Workplace Fitness",
         f"Sedentary indicators peak in the 50–60 bracket where prevalence reaches {round(filtered[filtered['age_group']=='50-60']['target'].mean()*100,1) if len(filtered[filtered['age_group']=='50-60'])>0 else 'N/A'}%. Mandate fitness facilities in workplaces targeting this demographic."),
        ("",        "🥗 Diet Subsidies",
         f"{high_ch}% of patients have high cholesterol (>240 mg/dL). Policy should prioritize subsidies for fresh produce and heart-healthy foods in lower-income urban zones with high disease prevalence."),
    ]
    for col, (cls, title, text) in zip([col1, col2, col3], recs):
        with col:
            st.markdown(f"""
            <div class="insight-box {cls}">
              <b style="color:#e6edf3">{title}</b><br>
              <span style="color:#8b949e">{text}</span>
            </div>
            """, unsafe_allow_html=True)
