"""utils/data_utils.py — shared data loading and feature engineering"""
import os
import pandas as pd
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "heart_disease.csv")

CP_MAP    = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}
RESTECG_MAP = {0: "Normal", 1: "ST-T Abnormality", 2: "LV Hypertrophy"}
SLOPE_MAP = {0: "Upsloping", 1: "Flat", 2: "Downsloping"}
THAL_MAP  = {0: "Normal", 1: "Fixed Defect", 2: "Reversible Defect", 3: "Unknown"}

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["gender"]        = df["sex"].map({1: "Male", 0: "Female"})
    df["disease_label"] = df["target"].map({1: "Heart Disease", 0: "Healthy"})
    df["cp_label"]      = df["cp"].map(CP_MAP)
    df["restecg_label"] = df["restecg"].map(RESTECG_MAP)
    df["slope_label"]   = df["slope"].map(SLOPE_MAP)
    df["thal_label"]    = df["thal"].map(THAL_MAP)
    df["age_group"]     = pd.cut(df["age"], bins=[0,40,50,60,70,100],
                                  labels=["<40","40-50","50-60","60-70","70+"])
    df["chol_category"] = pd.cut(df["chol"], bins=[0,200,240,999],
                                  labels=["Normal","Borderline","High"])
    df["risk_score"]    = (
        (df["chol"] / 240).clip(0, 2) +
        (df["trestbps"] / 140).clip(0, 2) +
        df["exang"] * 0.8 +
        (df["ca"] * 0.3) +
        ((220 - df["age"] - df["thalach"]) / 50).clip(0, 2)
    ).round(2)
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    total      = len(df)
    positive   = int(df["target"].sum())
    negative   = total - positive
    avg_age    = round(df["age"].mean(), 1)
    avg_chol   = round(df["chol"].mean(), 1)
    avg_bp     = round(df["trestbps"].mean(), 1)
    male_pct   = round(df["sex"].mean() * 100, 1)
    return dict(total=total, positive=positive, negative=negative,
                prevalence=round(positive/total*100, 1),
                avg_age=avg_age, avg_chol=avg_chol, avg_bp=avg_bp,
                male_pct=male_pct)


def filter_df(df, age_range, gender, disease_status, chol_cat):
    d = df.copy()
    d = d[d["age"].between(*age_range)]
    if gender != "All":
        d = d[d["gender"] == gender]
    if disease_status != "All":
        d = d[d["disease_label"] == disease_status]
    if chol_cat != "All":
        d = d[d["chol_category"] == chol_cat]
    return d
