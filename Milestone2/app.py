"""
Prediction AI — Milestone 2
Risk Assessment, Risk Scoring, SWOT Analysis & Feasibility Assessment

Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Prediction AI — Milestone 2",
    page_icon="📊",
    layout="wide",
)

# --------------------------------------------------------------------------
# Reference data (drawn from the Milestone 2 course content)
# --------------------------------------------------------------------------
RISK_TYPES = {
    "Market Risk": {
        "meaning": "Uncertainty about customer demand and market acceptance.",
        "example": "Customers may not be interested in the product.",
        "question": "Will customers actually want our product?",
    },
    "Financial Risk": {
        "meaning": "Possibility of money-related problems.",
        "example": "Project requires ₹10 lakhs but only ₹5 lakhs is available.",
        "question": "Do we have enough financial resources?",
    },
    "Competition Risk": {
        "meaning": "Risk created by existing or new competitors.",
        "example": "Several strong companies already offer similar products.",
        "question": "Can our project compete successfully?",
    },
    "Technical Risk": {
        "meaning": "Risk related to technology, development or technical skills.",
        "example": "Project requires advanced AI but the team lacks expertise.",
        "question": "Can we technically build the project?",
    },
    "Operational Risk": {
        "meaning": "Problems that may occur while running the project.",
        "example": "Staff shortage, poor management, resource or maintenance problems.",
        "question": "Can we operate the project successfully?",
    },
}

RISK_SCALE = {
    1: "Very Low Risk",
    2: "Low Risk",
    3: "Medium Risk",
    4: "High Risk",
    5: "Very High Risk",
}

FEASIBILITY_BANDS = [
    (80, 100, "Highly Feasible", "🟢"),
    (60, 79, "Feasible", "🟩"),
    (40, 59, "Moderately Feasible", "🟧"),
    (0, 39, "Not Feasible", "🔴"),
]

EXAMPLE_PROJECT = {
    "name": "AI-Based Online Learning Platform",
    "description": "An AI-personalized platform that adapts lessons to each learner.",
    "risks": {
        "Market Risk": 3,
        "Financial Risk": 4,
        "Competition Risk": 4,
        "Technical Risk": 2,
        "Operational Risk": 3,
    },
    "strengths": "AI personalization\nEasy accessibility",
    "weaknesses": "Limited budget\nSmall team",
    "opportunities": "Growing online education market",
    "threats": "Established competitors\nRapid technology changes",
}

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def risk_level_from_score(avg_score: float) -> str:
    if avg_score <= 1.5:
        return "Very Low Risk"
    elif avg_score <= 2.5:
        return "Low Risk"
    elif avg_score <= 3.5:
        return "Medium Risk"
    elif avg_score <= 4.5:
        return "High Risk"
    return "Very High Risk"


def feasibility_band(score: float):
    for low, high, label, emoji in FEASIBILITY_BANDS:
        if low <= score <= high:
            return label, emoji
    return "Not Feasible", "🔴"


def parse_lines(text: str):
    return [line.strip() for line in text.splitlines() if line.strip()]


def compute_feasibility(avg_risk: float, strengths, weaknesses, opportunities, threats) -> float:
    """
    Illustrative feasibility formula (0-100), for teaching purposes:
      - 60% weight: inverse of average risk (lower risk -> higher feasibility)
      - 40% weight: net SWOT balance (Strengths + Opportunities vs Weaknesses + Threats)
    """
    risk_component = (5 - avg_risk) / 4 * 100  # 0-100

    positives = len(strengths) + len(opportunities)
    negatives = len(weaknesses) + len(threats)
    total = positives + negatives
    if total == 0:
        swot_component = 50.0
    else:
        swot_component = (positives / total) * 100

    score = 0.6 * risk_component + 0.4 * swot_component
    return round(max(0, min(100, score)), 1)


def build_recommendation(project_name, avg_risk, risk_label, feas_score, feas_label,
                          strengths, weaknesses, opportunities, threats) -> str:
    name = project_name if project_name else "This project"
    top_strength = strengths[0] if strengths else "no notable strengths identified"
    top_threat = threats[0] if threats else "no major threats identified"

    lines = [
        f"**{name}** carries an overall risk score of **{avg_risk:.1f}/5** ({risk_label}), "
        f"and scores **{feas_score}/100** on feasibility (**{feas_label}**).",
        f"- Key strength to leverage: *{top_strength}*.",
        f"- Key threat to monitor: *{top_threat}*.",
    ]
    if feas_label in ("Highly Feasible", "Feasible"):
        lines.append(
            "Overall, the project appears **worth pursuing**, provided the identified "
            "risks and threats are actively managed."
        )
    elif feas_label == "Moderately Feasible":
        lines.append(
            "Overall, the project is **feasible with caution** — reducing key risks "
            "(especially the highest-scoring ones) would meaningfully improve its outlook."
        )
    else:
        lines.append(
            "Overall, the project currently looks **difficult to justify** without major "
            "changes — revisit the highest risk areas and weaknesses before proceeding."
        )
    return "\n\n".join(lines)


# --------------------------------------------------------------------------
# Sidebar — project info & example loader
# --------------------------------------------------------------------------
st.sidebar.title("📊 Prediction AI")
st.sidebar.caption("Milestone 2 — Risk Assessment & SWOT Analysis")

if "loaded_example" not in st.session_state:
    st.session_state.loaded_example = False

if st.sidebar.button("Load Example Project (from class)", use_container_width=True):
    st.session_state.loaded_example = True

st.sidebar.markdown("---")
st.sidebar.header("1️⃣ Project Information")

default_name = EXAMPLE_PROJECT["name"] if st.session_state.loaded_example else ""
default_desc = EXAMPLE_PROJECT["description"] if st.session_state.loaded_example else ""

project_name = st.sidebar.text_input("Project / Startup Name", value=default_name)
project_description = st.sidebar.text_area("Short Description", value=default_desc, height=100)

st.sidebar.markdown("---")
st.sidebar.info(
    "Fill in the Risk Assessment and SWOT sections in the main panel, then scroll down "
    "for the automatic Risk Score, SWOT summary, and Feasibility recommendation."
)

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.title("Prediction AI — Milestone 2")
st.subheader("Risk Assessment → Risk Scoring → SWOT Analysis → Feasibility Assessment")
st.markdown(
    "Convert your project information into an evaluation and a decision. "
    "Fill out the sections below to generate an automatic risk score, SWOT summary, "
    "and final feasibility recommendation."
)
st.markdown("---")

# --------------------------------------------------------------------------
# Section: Risk Assessment
# --------------------------------------------------------------------------
st.header("2️⃣ Risk Assessment")
st.caption("Risk is the possibility that something may negatively affect a project. "
           "Rate each risk type on a scale of 1 (Very Low) to 5 (Very High).")

risk_scores = {}
cols = st.columns(len(RISK_TYPES))

for i, (risk_name, info) in enumerate(RISK_TYPES.items()):
    with cols[i]:
        st.markdown(f"**{risk_name}**")
        with st.expander("What is this?"):
            st.write(f"**Meaning:** {info['meaning']}")
            st.write(f"**Example:** {info['example']}")
            st.write(f"**Key question:** {info['question']}")
        default_val = EXAMPLE_PROJECT["risks"][risk_name] if st.session_state.loaded_example else 3
        risk_scores[risk_name] = st.slider(
            risk_name, 1, 5, default_val, key=f"risk_{risk_name}", label_visibility="collapsed"
        )
        st.caption(RISK_SCALE[risk_scores[risk_name]])

st.markdown("---")

# --------------------------------------------------------------------------
# Section: Risk Scoring Engine
# --------------------------------------------------------------------------
st.header("3️⃣ Risk Scoring Engine")

avg_risk = sum(risk_scores.values()) / len(risk_scores)
risk_label = risk_level_from_score(avg_risk)

score_col, chart_col = st.columns([1, 2])

with score_col:
    st.metric("Overall Risk Score", f"{avg_risk:.1f} / 5", risk_label)
    formula_terms = " + ".join(str(v) for v in risk_scores.values())
    st.caption(f"Average = ({formula_terms}) / {len(risk_scores)} = {avg_risk:.1f}")

with chart_col:
    df_risk = pd.DataFrame({
        "Risk Type": list(risk_scores.keys()),
        "Score": list(risk_scores.values()),
    }).set_index("Risk Type")
    st.bar_chart(df_risk, height=250)

st.markdown("---")

# --------------------------------------------------------------------------
# Section: SWOT Analysis
# --------------------------------------------------------------------------
st.header("4️⃣ SWOT Analysis")
st.caption("SWOT = Strengths, Weaknesses, Opportunities, Threats. "
           "Strengths & Weaknesses are internal; Opportunities & Threats are external. "
           "Enter one item per line.")

swot_cols = st.columns(2)

with swot_cols[0]:
    st.markdown("#### 💪 Strengths *(internal, positive)*")
    strengths_text = st.text_area(
        "Strengths", value=EXAMPLE_PROJECT["strengths"] if st.session_state.loaded_example else "",
        placeholder="e.g. Unique technology\nSkilled team", height=120, label_visibility="collapsed"
    )
    st.markdown("#### ⚠️ Weaknesses *(internal, negative)*")
    weaknesses_text = st.text_area(
        "Weaknesses", value=EXAMPLE_PROJECT["weaknesses"] if st.session_state.loaded_example else "",
        placeholder="e.g. Limited budget\nSmall team", height=120, label_visibility="collapsed"
    )

with swot_cols[1]:
    st.markdown("#### 🚀 Opportunities *(external, positive)*")
    opportunities_text = st.text_area(
        "Opportunities", value=EXAMPLE_PROJECT["opportunities"] if st.session_state.loaded_example else "",
        placeholder="e.g. Growing market\nNew customer segments", height=120, label_visibility="collapsed"
    )
    st.markdown("#### 🛑 Threats *(external, negative)*")
    threats_text = st.text_area(
        "Threats", value=EXAMPLE_PROJECT["threats"] if st.session_state.loaded_example else "",
        placeholder="e.g. Strong competitors\nMarket changes", height=120, label_visibility="collapsed"
    )

strengths = parse_lines(strengths_text)
weaknesses = parse_lines(weaknesses_text)
opportunities = parse_lines(opportunities_text)
threats = parse_lines(threats_text)

st.markdown("##### SWOT Quick View")
swot_grid = pd.DataFrame(
    {
        "Positive": [
            "\n".join(f"• {s}" for s in strengths) or "—",
            "\n".join(f"• {o}" for o in opportunities) or "—",
        ],
        "Negative": [
            "\n".join(f"• {w}" for w in weaknesses) or "—",
            "\n".join(f"• {t}" for t in threats) or "—",
        ],
    },
    index=["Internal", "External"],
)
st.table(swot_grid)

st.markdown("---")

# --------------------------------------------------------------------------
# Section: Feasibility Assessment
# --------------------------------------------------------------------------
st.header("5️⃣ Feasibility Assessment")
st.caption("Feasibility means determining whether a project is practical, achievable and "
           "worth implementing — combining risk score and SWOT balance.")

feas_score = compute_feasibility(avg_risk, strengths, weaknesses, opportunities, threats)
feas_label, feas_emoji = feasibility_band(feas_score)

feas_col1, feas_col2 = st.columns([1, 2])
with feas_col1:
    st.metric("Feasibility Score", f"{feas_score} / 100", f"{feas_emoji} {feas_label}")
with feas_col2:
    st.progress(min(int(feas_score), 100) / 100)
    st.caption(
        "80–100 Highly Feasible · 60–79 Feasible · 40–59 Moderately Feasible · 0–39 Not Feasible"
    )

st.markdown("---")

# --------------------------------------------------------------------------
# Section: Final Recommendation
# --------------------------------------------------------------------------
st.header("6️⃣ Final Recommendation")

recommendation = build_recommendation(
    project_name, avg_risk, risk_label, feas_score, feas_label,
    strengths, weaknesses, opportunities, threats
)
st.success(recommendation)

with st.expander("📋 Complete Milestone 2 Flow"):
    st.markdown(
        "**Project Data → Risk Assessment → Risk Score → SWOT Analysis → "
        "Feasibility Assessment → Final Recommendation**\n\n"
        "- **Risk:** What can go wrong?\n"
        "- **SWOT:** What is good, weak, possible and dangerous?\n"
        "- **Feasibility:** Can we realistically implement it?"
    )
