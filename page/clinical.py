"""pages/clinical.py — Clinical Risk Analysis (Dr. Sharma scenario)"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_utils import load_data, filter_df
from utils.charts import (bar_age_group, donut_gender, scatter_chol_hr,
                           heatmap_cp_disease, boxplot_chol_age, histogram_hr)


def render():
    df = load_data()

    st.markdown("""
    <div style="padding: 20px 0 8px;">
      <h1 style="font-family:'DM Serif Display',serif; font-size:2.2rem; margin:0;">
        🩺 Clinical Risk Analysis
      </h1>
      <p style="color:#8b949e; margin-top:6px;">
        Designed for clinicians — segment patients by demographics, symptoms, and lab values.
        Mirrors <b style="color:#e6edf3">Dr. Sharma's</b> workflow for identifying high-risk groups.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar Filters ────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔬 Clinical Filters")
        age_range = st.slider("Age Range", 20, 80, (29, 77))
        gender    = st.selectbox("Gender", ["All", "Male", "Female"])
        disease   = st.selectbox("Disease Status", ["All", "Heart Disease", "Healthy"])
        chol_cat  = st.selectbox("Cholesterol", ["All", "Normal", "Borderline", "High"])

    filtered = filter_df(df, age_range, gender, disease, chol_cat)

    # ── Summary strip ─────────────────────────────────────────────────────────
    total = len(filtered)
    pos   = int(filtered["target"].sum())
    neg   = total - pos
    prev  = round(pos / total * 100, 1) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, color in [
        (c1, total, "Filtered Patients", "#4c9be8"),
        (c2, pos,   "Disease Positive",  "#e05252"),
        (c3, neg,   "Healthy",           "#3fb950"),
        (c4, f"{prev}%", "Prevalence",   "#d29922"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tab layout ────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📊 Demographics", "🔬 Lab Values", "📈 Distributions"])

    with tab1:
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.plotly_chart(bar_age_group(filtered), use_container_width=True)
        with col_b:
            st.plotly_chart(donut_gender(filtered), use_container_width=True)

        st.plotly_chart(heatmap_cp_disease(filtered), use_container_width=True)

    with tab2:
        st.plotly_chart(scatter_chol_hr(filtered), use_container_width=True)
        st.plotly_chart(boxplot_chol_age(filtered), use_container_width=True)

    with tab3:
        st.plotly_chart(histogram_hr(filtered), use_container_width=True)

        # Risk factor breakdown table
        st.markdown("""
        <div class="section-header">
          <span class="icon">📋</span><h2>Risk Factor Breakdown</h2>
        </div>
        """, unsafe_allow_html=True)

        risk_table = filtered.groupby("disease_label").agg(
            Count=("age", "count"),
            Avg_Age=("age", lambda x: round(x.mean(), 1)),
            Avg_Cholesterol=("chol", lambda x: round(x.mean(), 1)),
            Avg_BP=("trestbps", lambda x: round(x.mean(), 1)),
            Avg_MaxHR=("thalach", lambda x: round(x.mean(), 1)),
            Pct_Smoker_Equivalent=("exang", lambda x: round(x.mean() * 100, 1)),
        ).reset_index()
        risk_table.columns = ["Status", "Count", "Avg Age", "Avg Cholesterol", "Avg BP", "Avg Max HR", "% Exang Angina"]
        st.dataframe(risk_table, use_container_width=True, hide_index=True)

    # ── Clinical Insight Panel ─────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <span class="icon">🔍</span><h2>Clinical Decision Support</h2>
    </div>
    """, unsafe_allow_html=True)

    if total > 0:
        high_risk_pct = round(filtered[
            (filtered["chol"] > 240) & (filtered["trestbps"] > 140)
        ]["target"].mean() * 100, 1)

        asym_pct = round(filtered[filtered["cp"] == 3]["target"].mean() * 100, 1) if len(filtered[filtered["cp"]==3]) else 0

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="insight-box danger">
              <b style="color:#e6edf3">⚠️ High-Risk Compound Indicator</b><br>
              <span style="color:#8b949e">Patients with Cholesterol >240 AND BP >140 in the current filter
              show a <b style="color:#e05252">{high_risk_pct}%</b> disease prevalence —
              {round(high_risk_pct / max(prev, 0.1), 1)}× the filtered average.
              Priority screening recommended for this sub-group.</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="insight-box warning">
              <b style="color:#e6edf3">🫀 Asymptomatic Chest Pain Alert</b><br>
              <span style="color:#8b949e">Of patients with <b>asymptomatic chest pain (Type 3)</b>,
              <b style="color:#d29922">{asym_pct}%</b> have confirmed heart disease.
              This silent presentation is the most clinically dangerous
              and frequently under-triaged pattern in the dataset.</span>
            </div>
            """, unsafe_allow_html=True)
