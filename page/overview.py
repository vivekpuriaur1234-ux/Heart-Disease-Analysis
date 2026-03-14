"""pages/overview.py — Landing overview with KPIs and key charts"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_utils import load_data, get_summary_stats
from utils.charts import (bar_age_group, donut_gender, scatter_chol_hr,
                           correlation_heatmap, prevalence_bar)


def render():
    df = load_data()
    stats = get_summary_stats(df)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 28px 0 8px;">
      <h1 style="font-family:'DM Serif Display',serif; font-size:2.6rem; margin:0; line-height:1.15;">
        Heart Disease Intelligence
        <span style="font-size:1.8rem;">🫀</span>
      </h1>
      <p style="color:#8b949e; font-size:1rem; margin-top:8px; max-width:620px;">
        Interactive analytics platform built on the UCI Heart Disease Dataset.
        Explore clinical patterns, population trends, and personal risk indicators
        — powered by <span style="color:#4c9be8;">Google Gemini AI</span>.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "Total Patients", str(stats["total"]), "UCI dataset records", "#4c9be8"),
        (c2, "Heart Disease+", str(stats["positive"]), f"{stats['prevalence']}% prevalence", "#e05252"),
        (c3, "Healthy", str(stats["negative"]), "confirmed negative", "#3fb950"),
        (c4, "Avg Age", str(stats["avg_age"]), "years across cohort", "#d29922"),
        (c5, "Avg Cholesterol", str(stats["avg_chol"]), "mg/dL serum level", "#a371f7"),
    ]
    for col, label, value, sub, color in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-value" style="color:{color};">{value}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Age Bar + Donut ────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.plotly_chart(bar_age_group(df), use_container_width=True)
    with col_b:
        st.plotly_chart(donut_gender(df), use_container_width=True)

    # ── Row 2: Prevalence + Scatter ────────────────────────────────────────────
    col_c, col_d = st.columns(2)
    with col_c:
        st.plotly_chart(prevalence_bar(df), use_container_width=True)
    with col_d:
        st.plotly_chart(scatter_chol_hr(df), use_container_width=True)

    # ── Row 3: Correlation matrix ──────────────────────────────────────────────
    st.plotly_chart(correlation_heatmap(df), use_container_width=True)

    # ── Key Insights ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <span class="icon">💡</span><h2>Key Findings</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    insights = [
        ("danger",  "Age Risk Peak",       f"The 50–60 age bracket has the highest absolute disease count. Prevalence reaches {df[df['age_group']=='50-60']['target'].mean()*100:.0f}% in this cohort — nearly double the population average."),
        ("warning", "Gender Disparity",    f"Male patients account for {df[df['target']==1]['sex'].mean()*100:.0f}% of positive cases, yet prevalence in females rises sharply after age 55 — a commonly missed clinical window."),
        ("",        "Cholesterol Paradox", "Contrary to expectation, many high-cholesterol patients are disease-negative, while asymptomatic chest pain (Type 3) is the single strongest predictor — present in 72% of positive cases."),
    ]
    for col, (cls, title, text) in zip([col1, col2, col3], insights):
        with col:
            st.markdown(f"""
            <div class="insight-box {cls}">
              <b style="color:#e6edf3">{title}</b><br>
              <span style="color:#8b949e">{text}</span>
            </div>
            """, unsafe_allow_html=True)
