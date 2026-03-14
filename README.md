# 🫀 CardioInsight AI — Heart Disease Analytics Platform

> **Streamlit + Google Gemini AI** · Built on the UCI Heart Disease Dataset (303 patients)

## Screenshots Preview

The app features 6 pages:
- 🏠 **Overview** — KPI dashboard with 5 key charts
- 🩺 **Clinical Analysis** — For clinicians (Dr. Sharma scenario)
- 🏛️ **Policy Dashboard** — Population health & policy (Ramesh scenario)
- 👤 **Personal Monitor** — Individual risk gauges + radar chart (Anita scenario)
- 📖 **Data Story** — 7-scene narrative journey through the data
- 🤖 **Gemini AI Assistant** — Chat with Gemini about anything in the dataset

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate the dataset (one-time)
```bash
python data/generate_data.py
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 🔑 Gemini API Key Setup

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Create a free API key
3. Paste it in the **Gemini AI Assistant** page sidebar

> **No key needed** to explore the dashboards, visualisations, or personal monitor.
> The key is only required to activate the AI chat assistant.

---

## 📁 Project Structure

```
heart_disease_app/
├── app.py                    # Main Streamlit entry point + global CSS
├── requirements.txt
├── data/
│   ├── generate_data.py      # Generates heart_disease.csv
│   └── heart_disease.csv     # UCI dataset (303 records, 14 features)
├── pages/
│   ├── overview.py           # Home dashboard
│   ├── clinical.py           # Clinical risk analysis
│   ├── policy.py             # Population health & policy
│   ├── personal.py           # Personal health monitor
│   ├── story.py              # 7-scene data story
│   └── gemini_chat.py        # Gemini AI assistant
└── utils/
    ├── data_utils.py         # Data loading, feature engineering, filtering
    └── charts.py             # Reusable Plotly chart builders (10 chart types)
```

---

## 🧠 Dataset Features

| Feature     | Description                        |
|-------------|-----------------------------------|
| age         | Patient age in years               |
| sex         | 1 = Male, 0 = Female               |
| cp          | Chest pain type (0-3)              |
| trestbps    | Resting blood pressure (mmHg)      |
| chol        | Serum cholesterol (mg/dL)          |
| fbs         | Fasting blood sugar > 120          |
| restecg     | Resting ECG results (0-2)          |
| thalach     | Max heart rate achieved            |
| exang       | Exercise-induced angina            |
| oldpeak     | ST depression                      |
| slope       | Slope of peak ST segment           |
| ca          | Number of major vessels (0-3)      |
| thal        | Thalassemia type                   |
| target      | Heart disease present (1=yes)      |

---

## 📊 Visualisations Included

1. Bar Chart — Cases by Age Group
2. Donut Chart — Gender Distribution  
3. Scatter Plot — Cholesterol vs Max Heart Rate
4. Heat Map — Chest Pain Type vs Disease Status
5. Line Chart — Age vs Resting Blood Pressure
6. Box Plot — Cholesterol by Age Group
7. Treemap — Thalassemia Type Prevalence
8. Histogram — Max Heart Rate Distribution
9. Dual-Axis Chart — BP vs ST Depression Over Age
10. Bubble Chart — Risk Score vs Age (bubble = cholesterol)
11. Correlation Heatmap — Feature correlation matrix
12. Radar Chart — Personal risk profile vs population
13. Gauge Charts — Individual health metrics vs benchmarks

---

## 🤖 Gemini AI Features

- **Data-aware system prompt** — Gemini is pre-loaded with all dataset statistics
- **8 Quick Prompts** — Pre-built questions covering clinical, policy, and personal angles
- **Multi-turn conversation** — Full chat history maintained per session
- **Personalised risk assessment** — Input your metrics and ask for analysis
- **Graceful fallback** — App works fully without API key (dashboards remain functional)

---

## 🛠 Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Frontend     | Streamlit 1.35+                     |
| Charts       | Plotly Express + Graph Objects      |
| AI           | Google Gemini 1.5 Flash             |
| Data         | Pandas, NumPy                       |
| Styling      | Custom CSS (DM Serif Display font)  |
| Dataset      | UCI Heart Disease (303 records)     |
