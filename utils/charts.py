"""utils/charts.py — reusable Plotly chart builders"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

BG      = "#0d1117"
SURFACE = "#161b22"
BORDER  = "#30363d"
TEXT    = "#e6edf3"
MUTED   = "#8b949e"
RED     = "#e05252"
BLUE    = "#4c9be8"
GREEN   = "#3fb950"
AMBER   = "#d29922"
PURPLE  = "#a371f7"
TEAL    = "#39d0d8"

PALETTE_DISEASE = {"Heart Disease": RED, "Healthy": BLUE}
PALETTE_GENDER  = {"Male": BLUE, "Female": "#c788e5"}
SEQ_RED  = ["#3a1a1a", "#7a2e2e", "#b24040", RED, "#f08080", "#fcc"]
SEQ_BLUE = ["#0d2038", "#1a4a7a", "#2a7abf", BLUE, "#80b8f0", "#cce0ff"]


def _base_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=TEXT, family="DM Sans"), x=0.01, xanchor="left"),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(color=MUTED, size=11, family="DM Sans"),
        margin=dict(l=20, r=20, t=44 if title else 20, b=20),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, borderwidth=1,
                    font=dict(color=TEXT, size=11)),
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, color=MUTED),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, color=MUTED),
    )
    return fig


def bar_age_group(df) -> go.Figure:
    g = df.groupby(["age_group", "disease_label"]).size().reset_index(name="count")
    fig = px.bar(g, x="age_group", y="count", color="disease_label",
                 barmode="group", color_discrete_map=PALETTE_DISEASE,
                 labels={"age_group": "Age Group", "count": "Patients", "disease_label": ""})
    _base_layout(fig, "Heart Disease Cases by Age Group")
    fig.update_traces(marker_line_width=0)
    return fig


def donut_gender(df) -> go.Figure:
    pos = df[df["target"] == 1]
    g = pos["gender"].value_counts().reset_index()
    g.columns = ["gender", "count"]
    fig = px.pie(g, values="count", names="gender", hole=0.62,
                 color="gender", color_discrete_map=PALETTE_GENDER)
    _base_layout(fig, "Gender Split — Heart Disease Cases", height=340)
    fig.update_traces(textposition="outside", textinfo="percent+label",
                      marker=dict(line=dict(color=SURFACE, width=2)))
    return fig


def scatter_chol_hr(df) -> go.Figure:
    fig = px.scatter(df, x="chol", y="thalach", color="disease_label",
                     color_discrete_map=PALETTE_DISEASE,
                     opacity=0.7,
                     labels={"chol": "Cholesterol (mg/dL)", "thalach": "Max Heart Rate", "disease_label": ""},
                     hover_data=["age", "gender"])
    fig.add_vline(x=240, line_dash="dash", line_color=AMBER,
                  annotation_text="High Chol Threshold", annotation_font_color=AMBER)
    _base_layout(fig, "Cholesterol vs Max Heart Rate")
    return fig


def heatmap_cp_disease(df) -> go.Figure:
    pivot = df.groupby(["cp_label", "disease_label"]).size().unstack(fill_value=0)
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0, SURFACE], [0.5, "#4c2a2a"], [1, RED]],
        showscale=True, text=pivot.values, texttemplate="%{text}",
        textfont=dict(color=TEXT, size=13),
    ))
    _base_layout(fig, "Chest Pain Type vs Disease Status", height=320)
    return fig


def line_age_bp(df) -> go.Figure:
    g = df.groupby(["age", "disease_label"])["trestbps"].mean().reset_index()
    fig = px.line(g, x="age", y="trestbps", color="disease_label",
                  color_discrete_map=PALETTE_DISEASE,
                  labels={"age": "Age", "trestbps": "Avg Resting BP (mmHg)", "disease_label": ""})
    fig.add_hline(y=140, line_dash="dot", line_color=RED,
                  annotation_text="Hypertension Threshold", annotation_font_color=RED)
    _base_layout(fig, "Age vs Average Resting Blood Pressure")
    fig.update_traces(line=dict(width=2))
    return fig


def boxplot_chol_age(df) -> go.Figure:
    fig = px.box(df, x="age_group", y="chol", color="disease_label",
                 color_discrete_map=PALETTE_DISEASE,
                 labels={"age_group": "Age Group", "chol": "Cholesterol (mg/dL)", "disease_label": ""})
    _base_layout(fig, "Cholesterol Distribution by Age Group")
    return fig


def treemap_thal(df) -> go.Figure:
    g = df.groupby(["thal_label", "disease_label"]).size().reset_index(name="count")
    g["parent"] = g["thal_label"] + " — " + g["disease_label"]
    fig = px.treemap(g, path=["thal_label", "disease_label"], values="count",
                     color="disease_label", color_discrete_map=PALETTE_DISEASE)
    _base_layout(fig, "Disease Prevalence by Thalassemia Type", height=360)
    fig.update_traces(marker=dict(line=dict(width=2, color=SURFACE)))
    return fig


def histogram_hr(df) -> go.Figure:
    fig = px.histogram(df, x="thalach", color="disease_label", nbins=25,
                       barmode="overlay", opacity=0.75,
                       color_discrete_map=PALETTE_DISEASE,
                       labels={"thalach": "Max Heart Rate Achieved", "count": "Patients", "disease_label": ""})
    _base_layout(fig, "Distribution of Maximum Heart Rate")
    fig.update_traces(marker_line_width=0)
    return fig


def dual_axis_bp_oldpeak(df) -> go.Figure:
    g = df[df["target"] == 1].groupby("age").agg(
        avg_bp=("trestbps", "mean"), avg_op=("oldpeak", "mean")
    ).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=g["age"], y=g["avg_bp"], name="Resting BP",
                             line=dict(color=RED, width=2)), secondary_y=False)
    fig.add_trace(go.Scatter(x=g["age"], y=g["avg_op"], name="ST Depression",
                             line=dict(color=AMBER, width=2, dash="dash")), secondary_y=True)
    _base_layout(fig, "BP vs ST Depression Over Age (Disease Patients)")
    fig.update_yaxes(title_text="Resting BP (mmHg)", secondary_y=False,
                     gridcolor=BORDER, color=MUTED)
    fig.update_yaxes(title_text="ST Depression (oldpeak)", secondary_y=True,
                     gridcolor=BORDER, color=MUTED)
    fig.update_xaxes(title_text="Age")
    return fig


def bubble_risk(df) -> go.Figure:
    sample = df.sample(min(150, len(df)), random_state=1)
    fig = px.scatter(sample, x="age", y="risk_score", size="chol",
                     color="disease_label", color_discrete_map=PALETTE_DISEASE,
                     size_max=25, opacity=0.75,
                     labels={"age": "Age", "risk_score": "Composite Risk Score",
                             "chol": "Cholesterol", "disease_label": ""},
                     hover_data=["gender", "chol", "trestbps"])
    _base_layout(fig, "Risk Score vs Age  (bubble = cholesterol)")
    return fig


def prevalence_bar(df) -> go.Figure:
    g = (df.groupby("age_group")["target"].agg(["sum", "count"])
           .reset_index()
           .rename(columns={"sum": "cases", "count": "total"}))
    g["prevalence"] = (g["cases"] / g["total"] * 100).round(1)
    fig = px.bar(g, x="age_group", y="prevalence",
                 color="prevalence", color_continuous_scale=[[0, BLUE], [0.5, AMBER], [1, RED]],
                 labels={"age_group": "Age Group", "prevalence": "Prevalence (%)"},
                 text="prevalence")
    fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
    _base_layout(fig, "Disease Prevalence by Age Group (%)")
    fig.update_coloraxes(showscale=False)
    return fig


def correlation_heatmap(df) -> go.Figure:
    cols = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca", "target"]
    corr = df[cols].corr().round(2)
    labels = ["Age", "Rest BP", "Cholesterol", "Max HR", "ST Depr.", "Vessels", "Target"]
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=labels, y=labels,
        colorscale=[[0, "#1a3a6e"], [0.5, SURFACE], [1, "#6e1a1a"]],
        zmid=0, text=corr.values, texttemplate="%{text}",
        textfont=dict(size=10, color=TEXT), showscale=True,
    ))
    _base_layout(fig, "Feature Correlation Matrix", height=400)
    return fig
