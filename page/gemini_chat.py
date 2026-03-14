"""pages/gemini_chat.py — Gemini AI Assistant with data-aware context"""
import streamlit as st
import pandas as pd
import os, sys, json, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_utils import load_data, get_summary_stats

SURFACE = "#161b22"; SURFACE2 = "#1c2333"; BORDER = "#30363d"
TEXT = "#e6edf3"; MUTED = "#8b949e"
RED = "#e05252"; BLUE = "#4c9be8"; GREEN = "#3fb950"; AMBER = "#d29922"

# ── Gemini call (graceful fallback if API key missing) ────────────────────────
def call_gemini(messages: list[dict], api_key: str) -> str:
    """Call Gemini via google-generativeai SDK."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.7, max_output_tokens=1200,
            ),
            system_instruction=messages[0]["content"] if messages[0]["role"] == "system" else ""
        )
        history = [
            {"role": "user" if m["role"] == "user" else "model",
             "parts": [m["content"]]}
            for m in messages
            if m["role"] != "system"
        ]
        chat   = model.start_chat(history=history[:-1])
        result = chat.send_message(history[-1]["parts"][0])
        return result.text
    except ImportError:
        return "_google-generativeai not installed. Run: `pip install google-generativeai`_"
    except Exception as e:
        return f"_Gemini error: {e}_\n\nInstall the SDK and add your API key in the sidebar."


def build_system_prompt(df: pd.DataFrame) -> str:
    stats = get_summary_stats(df)
    age_prev = (df.groupby("age_group")["target"].mean() * 100).round(1).to_dict()

    return textwrap.dedent(f"""
    You are CardioInsight AI, an expert medical data analyst and healthcare AI assistant
    specialising in cardiovascular disease risk analysis.

    You have full access to the Heart Disease UCI Dataset loaded in memory:

    DATASET SUMMARY:
    - Total patients: {stats['total']}
    - Heart disease positive: {stats['positive']} ({stats['prevalence']}% prevalence)
    - Average age: {stats['avg_age']} years
    - Average cholesterol: {stats['avg_chol']} mg/dL
    - Average resting BP: {stats['avg_bp']} mmHg
    - Male patients: {stats['male_pct']}%

    PREVALENCE BY AGE GROUP: {json.dumps(age_prev)}

    KEY DATASET FACTS:
    - 14 features: age, sex, cp (chest pain type 0-3), trestbps, chol, fbs, restecg,
      thalach (max HR), exang, oldpeak (ST depression), slope, ca, thal, target
    - Asymptomatic chest pain (cp=3) has the HIGHEST disease association (~72% prevalence)
    - Exercise-induced angina (exang=1) patients: {round(df[df['exang']==1]['target'].mean()*100,1)}% disease rate
    - High cholesterol (>240) patients: {round(df[df['chol']>240]['target'].mean()*100,1)}% disease rate
    - Hypertension (BP>140) patients: {round(df[df['trestbps']>140]['target'].mean()*100,1)}% disease rate
    - Thal type 2 (Reversible Defect): {round(df[df['thal']==2]['target'].mean()*100,1)}% disease rate
    - Males: {round(df[df['sex']==1]['target'].mean()*100,1)}% prevalence | Females: {round(df[df['sex']==0]['target'].mean()*100,1)}% prevalence

    CLINICAL THRESHOLDS:
    - Total cholesterol: <200 normal, 200-240 borderline, >240 high
    - Resting BP: <120 normal, 120-139 elevated, 140-159 Stage 1 HTN, ≥160 Stage 2
    - Max HR target: ~(220 - age) × 0.85 for stress testing

    YOUR ROLE:
    - Answer questions about the dataset, cardiovascular health, and risk factors
    - Provide personalised risk explanations when given patient metrics
    - Explain visualisations and patterns found in the dashboards
    - Suggest evidence-based lifestyle and policy interventions
    - Be warm, clear, and appropriately cautious — always recommend professional medical advice
    - Use data references where possible (cite the statistics above)
    - Format responses with clear structure using markdown

    IMPORTANT: You are an AI assistant. Always recommend consulting a qualified healthcare
    professional for medical decisions. Do not diagnose conditions.
    """).strip()


# ── Quick prompts ──────────────────────────────────────────────────────────────
QUICK_PROMPTS = [
    ("🔍 Key Risk Factors",         "What are the top 3 risk factors for heart disease in this dataset? Explain each with supporting statistics."),
    ("👨‍⚕️ Clinical Recommendations", "What clinical interventions would you recommend for a 55-year-old male patient with cholesterol of 260 and BP of 145?"),
    ("🏛️ Policy Insights",           "Based on this dataset, what are the most impactful public health policies to reduce heart disease prevalence?"),
    ("🧬 Gender Differences",        "How do risk patterns differ between male and female patients in this dataset? Are there any surprising findings?"),
    ("📊 Explain the Dashboard",     "Can you walk me through the most important visualisations in the Clinical Analysis dashboard and what they reveal?"),
    ("🥗 Lifestyle Changes",         "What lifestyle modifications would have the greatest impact on reducing heart disease risk based on the data?"),
    ("⚠️ Silent Warning Signs",      "Why is asymptomatic chest pain so dangerous and how is it reflected in this dataset?"),
    ("🎯 Personal Risk Check",       "I'm a 48-year-old woman with cholesterol of 230, BP of 135, and no exercise angina. What does this dataset say about my risk profile?"),
]


def render():
    df = load_data()

    st.markdown("""
    <div style="padding:20px 0 8px;">
      <h1 style="font-family:'DM Serif Display',serif; font-size:2.2rem; margin:0;">
        🤖 Gemini AI Assistant
      </h1>
      <p style="color:#8b949e; margin-top:6px;">
        Ask anything about heart disease, the dataset, your risk profile, or clinical insights.
        Powered by <b style="color:#4c9be8;">Google Gemini 1.5 Flash</b>.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── API Key input ─────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔑 Gemini API Key")
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            placeholder="AIza...",
            help="Get your free API key at https://aistudio.google.com",
        )
        if api_key:
            st.success("API key set ✓")
        else:
            st.markdown(f"""
            <div style="background:{SURFACE2}; border:1px solid {BORDER}; border-radius:8px;
                        padding:12px; font-size:0.8rem; color:{MUTED}; line-height:1.6;">
              Get a free key at<br>
              <a href="https://aistudio.google.com" style="color:{BLUE};">
                aistudio.google.com
              </a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        show_context = st.checkbox("Show system context", value=False)
        clear_chat   = st.button("🗑️ Clear Chat History")

    # ── State init ────────────────────────────────────────────────────────────
    if "messages" not in st.session_state or clear_chat:
        st.session_state.messages = []
        st.session_state.turn_count = 0

    system_prompt = build_system_prompt(df)

    if show_context:
        with st.expander("🧠 System Context (sent to Gemini)", expanded=False):
            st.code(system_prompt, language="markdown")

    # ── Quick prompt buttons ───────────────────────────────────────────────────
    st.markdown("#### ⚡ Quick Questions")
    cols = st.columns(4)
    for i, (label, prompt) in enumerate(QUICK_PROMPTS):
        with cols[i % 4]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state._trigger_response = True

    st.markdown("---")

    # ── Chat history ──────────────────────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])

    # ── Auto-respond to quick prompt ──────────────────────────────────────────
    if st.session_state.get("_trigger_response"):
        del st.session_state["_trigger_response"]
        _send_and_respond(df, system_prompt, api_key)
        st.rerun()

    # ── Chat input ────────────────────────────────────────────────────────────
    if prompt_input := st.chat_input("Ask about heart disease, your risk profile, or the data..."):
        st.session_state.messages.append({"role": "user", "content": prompt_input})
        _send_and_respond(df, system_prompt, api_key)
        st.rerun()

    # ── Empty state ───────────────────────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown(f"""
        <div style="text-align:center; padding:48px 24px; color:{MUTED};">
          <div style="font-size:3rem; margin-bottom:16px;">🫀 🤖</div>
          <div style="font-size:1.1rem; color:{TEXT}; margin-bottom:8px; font-family:'DM Serif Display',serif;">
            Ask me anything about heart disease
          </div>
          <div style="max-width:500px; margin:0 auto; line-height:1.7;">
            I have full context of the UCI Heart Disease dataset — {len(df)} patients,
            {len(df.columns)} features, and the clinical benchmarks from the analysis.
            Try one of the quick questions above, or type your own below.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Disclaimer ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:24px; padding:10px 16px; background:{SURFACE2};
                border-radius:8px; font-size:0.78rem; color:{MUTED}; text-align:center;">
      ⚕️ CardioInsight AI is for educational purposes only. Always consult a qualified
      healthcare professional for medical advice, diagnosis, or treatment.
    </div>
    """, unsafe_allow_html=True)


def _send_and_respond(df, system_prompt, api_key):
    """Compose messages and call Gemini."""
    full_messages = [{"role": "system", "content": system_prompt}] + \
                    st.session_state.messages

    if not api_key:
        response = (
            "⚠️ **API Key Required**\n\n"
            "Please enter your Google Gemini API key in the sidebar to enable AI responses.\n\n"
            "You can get a **free** API key at [aistudio.google.com](https://aistudio.google.com).\n\n"
            "Once you've added the key, ask me anything about the heart disease dataset, "
            "clinical patterns, or your personal risk profile!"
        )
    else:
        with st.spinner("Gemini is thinking..."):
            response = call_gemini(full_messages, api_key)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.turn_count = st.session_state.get("turn_count", 0) + 1
