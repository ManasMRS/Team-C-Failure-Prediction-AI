import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from modules.risk_assessment import (
    generate_risk_assessment,
)

from modules.recommendation import (
    generate_key_findings,
    generate_recommendations,
)

from modules.report_generator import (
    generate_text_report,
    generate_pdf_report,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Startup Risk Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL APP
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 0% 0%,
                rgba(124, 58, 237, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 100% 0%,
                rgba(219, 39, 119, 0.10),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #faf8ff 0%,
                #ffffff 50%,
                #fff7fc 100%
            );
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {
        max-width: 1500px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #32106b 0%,
                #5b21b6 45%,
                #86198f 72%,
                #9d174d 100%
            );

        border-right: 1px solid
        rgba(255,255,255,0.08);
    }


    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }


    section[data-testid="stSidebar"] hr {
        border-color:
        rgba(255,255,255,0.20) !important;
    }


    /* =====================================================
       SIDEBAR BRAND
       ===================================================== */

    .sidebar-brand {
        padding: 8px 0 18px 0;
    }

    .sidebar-logo {
        font-size: 25px;
        font-weight: 850;
        color: #ffffff;
    }

    .sidebar-subtitle {
        font-size: 12px;
        color: rgba(255,255,255,0.72);
        margin-top: 5px;
    }

    .sidebar-section-title {
        font-size: 13px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.20);
        margin: 12px 0 18px 0;
    }


    /* =====================================================
       SIDEBAR STATUS
       ===================================================== */

    .prediction-status {
        display: flex;
        gap: 10px;
        align-items: center;

        background:
            rgba(34,197,94,0.16);

        border:
            1px solid rgba(134,239,172,0.25);

        border-radius:
            12px;

        padding:
            12px 14px;

        margin-bottom:
            12px;
    }

    .status-icon {
        width: 28px;
        height: 28px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background: rgba(34,197,94,0.25);

        font-weight: 800;
    }

    .status-title {
        font-size: 13px;
        font-weight: 750;
    }

    .status-subtitle {
        font-size: 11px;
        opacity: 0.75;
        margin-top: 2px;
    }


    .no-prediction-card {
        background:
            rgba(255,255,255,0.10);

        border:
            1px solid rgba(255,255,255,0.15);

        border-radius:
            12px;

        padding:
            14px;

        color:
            white;

        font-size:
            13px;
    }

    .no-prediction-title {
        font-weight: 750;
        margin-bottom: 8px;
    }

    .no-prediction-text {
        opacity: 0.85;
        line-height: 1.5;
    }


    /* =====================================================
       SIDEBAR STAT CARDS
       ===================================================== */

    .sidebar-stat-card {
        background:
            rgba(255,255,255,0.12);

        border:
            1px solid rgba(255,255,255,0.18);

        border-radius:
            15px;

        padding:
            15px;

        margin-top:
            10px;

        box-shadow:
            0 8px 25px
            rgba(0,0,0,0.15);
    }

    .sidebar-stat-label {
        font-size: 12px;
        color: rgba(255,255,255,0.82);
        font-weight: 650;
    }

    .sidebar-stat-value {
        font-size: 25px;
        font-weight: 850;
        color: #ffffff;
        margin-top: 5px;
    }

    .sidebar-stat-description {
        font-size: 11px;
        color: rgba(255,255,255,0.65);
        margin-top: 3px;
    }


    /* =====================================================
       MAIN HEADINGS
       ===================================================== */

    h1 {
        background:
            linear-gradient(
                90deg,
                #5b21b6,
                #7c3aed,
                #db2777
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        font-weight: 850 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #312e81 !important;
        font-weight: 800 !important;
    }

    h3 {
        color: #4c1d95 !important;
        font-weight: 750 !important;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    .stTextInput input,
    .stTextArea textarea {
        background:
            rgba(255,255,255,0.95) !important;

        color:
            #1f2937 !important;

        border:
            1px solid #ddd6fe !important;

        border-radius:
            12px !important;

        padding:
            12px 14px !important;
    }

    .stTextInput input:hover,
    .stTextArea textarea:hover {
        border-color:
            #a78bfa !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color:
            #7c3aed !important;

        box-shadow:
            0 0 0 2px
            rgba(124,58,237,0.12) !important;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #ffffff,
                #faf5ff
            );

        border:
            1px solid #ede9fe;

        border-radius:
            18px;

        padding:
            20px;

        min-height:
            125px;

        box-shadow:
            0 8px 25px
            rgba(76,29,149,0.08);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform:
            translateY(-3px);

        box-shadow:
            0 14px 35px
            rgba(76,29,149,0.14);
    }

    div[data-testid="stMetricLabel"] {
        color:
            #6b7280 !important;

        font-weight:
            650 !important;
    }

    div[data-testid="stMetricValue"] {
        color:
            #4c1d95 !important;

        font-weight:
            850 !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius:
            12px !important;

        font-weight:
            700 !important;
    }

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(
                90deg,
                #6d28d9,
                #9333ea,
                #db2777
            ) !important;

        color:
            white !important;

        border:
            none !important;

        border-radius:
            14px !important;

        min-height:
            50px !important;

        font-weight:
            800 !important;

        box-shadow:
            0 8px 22px
            rgba(124,58,237,0.25);

        transition:
            all 0.2s ease;
    }

    .stButton > button[kind="primary"]:hover {
        transform:
            translateY(-2px);

        box-shadow:
            0 12px 30px
            rgba(124,58,237,0.35);
    }


    /* =====================================================
       DOWNLOAD BUTTON
       ===================================================== */

    .stDownloadButton > button {
        min-height:
            46px !important;

        border-radius:
            12px !important;

        border:
            1px solid #ddd6fe !important;

        font-weight:
            700 !important;

        background:
            #ffffff !important;
    }

    .stDownloadButton > button:hover {
        border-color:
            #7c3aed !important;

        color:
            #7c3aed !important;
    }


    /* =====================================================
       CONTAINERS
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius:
            20px !important;

        border:
            1px solid #e9d5ff !important;

        background:
            rgba(255,255,255,0.88) !important;

        box-shadow:
            0 8px 30px
            rgba(76,29,149,0.06);
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius:
            12px !important;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer-line {
        height:
            1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #c4b5fd,
                #f9a8d4,
                transparent
            );

        margin-top:
            45px;

        margin-bottom:
            18px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def risk_icon(level):
    """Return an icon based on risk level."""

    level = str(level).lower()

    if "low" in level:
        return "🟢"

    if "moderate" in level or "medium" in level:
        return "🟡"

    return "🔴"


def risk_color(level):
    """Return chart color based on risk level."""

    level = str(level).lower()

    if "low" in level:
        return "#16a34a"

    if "moderate" in level or "medium" in level:
        return "#f59e0b"

    return "#dc2626"


def save_prediction_history(assessment):
    """
    Save the latest prediction for the real trend chart.
    """

    if "risk_history" not in st.session_state:
        st.session_state["risk_history"] = []

    history = st.session_state["risk_history"]

    history.append(
        {
            "date": datetime.now().strftime(
                "%d %b %Y %H:%M"
            ),

            "overall_risk":
                float(
                    assessment["overall_risk"]
                ),

            "market_risk":
                float(
                    assessment["market_risk"]
                ),

            "technical_risk":
                float(
                    assessment["technical_risk"]
                ),

            "financial_risk":
                float(
                    assessment["financial_risk"]
                ),

            "competition_risk":
                float(
                    assessment["competition_risk"]
                ),
        }
    )

    # Keep latest 10 predictions
    st.session_state["risk_history"] = history[-10:]


def render_prediction_result(prediction):
    """
    Display prediction KPI cards and quick assessment.
    """

    st.markdown(
        "## 🎯 Prediction Result"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "⚠️ Overall Risk",
            f'{prediction["overall_risk"]:.1f}%',
            prediction["overall_level"],
        )

    with c2:
        st.metric(
            "🌎 Market Risk",
            f'{prediction["market_risk"]:.1f}%',
            prediction["market_level"],
        )

    with c3:
        st.metric(
            "⚙️ Technical Risk",
            f'{prediction["technical_risk"]:.1f}%',
            prediction["technical_level"],
        )

    with c4:
        st.metric(
            "🎯 Success Probability",
            f'{prediction["success_probability"]:.1f}%',
        )

    st.write("")

    with st.container(border=True):

        st.markdown(
            "### 🔎 Quick Assessment"
        )

        overall_level = prediction["overall_level"]

        st.write(
            f"{risk_icon(overall_level)} "
            f"The project currently has "
            f"**{overall_level.lower()}** with an "
            f"overall risk score of "
            f"**{prediction['overall_risk']:.1f}%**."
        )

        st.write(
            f"The calculated success probability is "
            f"**{prediction['success_probability']:.1f}%**."
        )

        st.info(
            "Go to **📊 Dashboard** to view interactive "
            "risk analytics."
        )


# ============================================================
# HERO
# ============================================================

def render_hero():

    st.markdown(
        "# 🚀 AI Startup Risk Analyzer"
    )

    st.caption(
        "AI-powered project risk prediction • "
        "Risk analytics • Success probability • "
        "Assessment reports"
    )

    st.write("")

    with st.container(border=True):

        col1, col2 = st.columns(
            [2.2, 1],
            vertical_alignment="center",
        )

        with col1:

            st.markdown(
                "## 🧠 Intelligent Project Risk Analysis"
            )

            st.write(
                "Transform your project information into "
                "actionable risk insights. Enter your project "
                "details and assessment factors to calculate "
                "overall risk, success probability, key findings, "
                "and recommendations."
            )

        with col2:

            st.markdown(
                "### 📊 Milestone 4"
            )

            st.caption(
                "Risk Analytics & Assessment"
            )

            if st.session_state.get("prediction"):
                st.success("Prediction Ready")
            else:
                st.info("Awaiting Prediction")

    st.write("")


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.sidebar.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                🚀 Risk AI
            </div>

            <div class="sidebar-subtitle">
                Startup & Project Risk Analyzer
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.sidebar.markdown(
        """
        <div class="sidebar-section-title">
            🧭 Navigation
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        label="Navigation",
        options=[
            "🧠 New Prediction",
            "📊 Dashboard",
            "🔍 Risk Analytics",
            "📋 Assessment Report",
            "📁 Project Information",
        ],
        label_visibility="collapsed",
        key="navigation_page",
    )

    st.sidebar.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # PREDICTION STATUS
    # --------------------------------------------------------

    prediction = st.session_state.get(
        "prediction"
    )

    if prediction:

        st.sidebar.markdown(
            """
            <div class="prediction-status">

                <div class="status-icon">
                    ✓
                </div>

                <div>

                    <div class="status-title">
                        Prediction Available
                    </div>

                    <div class="status-subtitle">
                        Latest assessment is ready
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        overall_risk = float(
            prediction.get(
                "overall_risk",
                0,
            )
        )

        success_probability = float(
            prediction.get(
                "success_probability",
                0,
            )
        )

        st.sidebar.markdown(
            f"""
            <div class="sidebar-stat-card">

                <div class="sidebar-stat-label">
                    ⚠️ Overall Risk
                </div>

                <div class="sidebar-stat-value">
                    {overall_risk:.1f}%
                </div>

                <div class="sidebar-stat-description">
                    Project risk score
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            f"""
            <div class="sidebar-stat-card">

                <div class="sidebar-stat-label">
                    🎯 Success Probability
                </div>

                <div class="sidebar-stat-value">
                    {success_probability:.1f}%
                </div>

                <div class="sidebar-stat-description">
                    Estimated success probability
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.sidebar.markdown(
            """
            <div class="no-prediction-card">

                <div class="no-prediction-title">
                    ⏳ No prediction generated yet
                </div>

                <div class="no-prediction-text">
                    Enter your project information and
                    assessment factors, then click
                    <b>Predict Project Risk</b>.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    return page


# ============================================================
# NEW PREDICTION PAGE
# ============================================================

def render_prediction_page():

    st.markdown(
        "## 🧠 Project Risk Prediction"
    )

    st.caption(
        "Enter your project details and assessment factors "
        "to generate a new risk prediction."
    )

    # ========================================================
    # PROJECT INFORMATION
    # ========================================================

    with st.container(border=True):

        st.markdown(
            "### 📋 Project Information"
        )

        st.caption(
            "Basic information for the project risk assessment."
        )

        project_name = st.text_input(
            "Project Name",
            value=st.session_state.get(
                "project_name",
                "",
            ),
            placeholder=(
                "Example: AI Healthcare Assistant"
            ),
            key="input_project_name",
        )

        project_description = st.text_area(
            "Project Description",
            value=st.session_state.get(
                "project_description",
                "",
            ),
            placeholder=(
                "Describe your startup, product, "
                "or project..."
            ),
            height=100,
            key="input_project_description",
        )

        col1, col2 = st.columns(2)

        with col1:

            target_market = st.text_input(
                "🌎 Target Market",
                value=st.session_state.get(
                    "target_market",
                    "",
                ),
                placeholder=(
                    "Example: Healthcare sector"
                ),
                key="input_target_market",
            )

            budget = st.text_input(
                "💰 Available Budget",
                value=st.session_state.get(
                    "budget",
                    "",
                ),
                placeholder=(
                    "Example: ₹10,00,000"
                ),
                key="input_budget",
            )

        with col2:

            resources = st.text_input(
                "👥 Available Resources",
                value=st.session_state.get(
                    "resources",
                    "",
                ),
                placeholder=(
                    "Example: 4 developers + AI resources"
                ),
                key="input_resources",
            )

            objectives = st.text_area(
                "🎯 Project Objectives",
                value=st.session_state.get(
                    "objectives",
                    "",
                ),
                placeholder=(
                    "What do you want to achieve?"
                ),
                height=100,
                key="input_objectives",
            )

    st.write("")

    # ========================================================
    # ASSESSMENT FACTORS
    # ========================================================

    st.markdown(
        "## 📊 Project Assessment Factors"
    )

    st.caption(
        "Use values from 0–100. Higher Market Demand, "
        "Technical Readiness and Financial Strength indicate "
        "better conditions. Higher Competition Intensity "
        "means greater competition."
    )

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### 🌎 Market"
            )

            market_demand = st.slider(
                "Market Demand",
                min_value=0,
                max_value=100,
                value=st.session_state.get(
                    "market_demand",
                    70,
                ),
                help=(
                    "Expected demand for your product "
                    "or service."
                ),
                key="market_demand_slider",
            )

            st.markdown(
                "### ⚙️ Technology"
            )

            technical_readiness = st.slider(
                "Technical Readiness",
                min_value=0,
                max_value=100,
                value=st.session_state.get(
                    "technical_readiness",
                    65,
                ),
                help=(
                    "Readiness of the technology, "
                    "team and product."
                ),
                key="technical_readiness_slider",
            )

        with col2:

            st.markdown(
                "### 💰 Finance"
            )

            financial_strength = st.slider(
                "Financial Strength",
                min_value=0,
                max_value=100,
                value=st.session_state.get(
                    "financial_strength",
                    60,
                ),
                help=(
                    "Strength of the available "
                    "financial resources."
                ),
                key="financial_strength_slider",
            )

            st.markdown(
                "### 🏆 Competition"
            )

            competition_intensity = st.slider(
                "Competition Intensity",
                min_value=0,
                max_value=100,
                value=st.session_state.get(
                    "competition_intensity",
                    50,
                ),
                help=(
                    "Intensity of competition "
                    "in the target market."
                ),
                key="competition_intensity_slider",
            )

    st.write("")

    # ========================================================
    # INPUT PREVIEW
    # ========================================================

    with st.expander(
        "👁️ Preview Assessment Inputs",
        expanded=False,
    ):

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Market Demand",
                f"{market_demand}%",
            )

        with c2:
            st.metric(
                "Technical Readiness",
                f"{technical_readiness}%",
            )

        with c3:
            st.metric(
                "Financial Strength",
                f"{financial_strength}%",
            )

        with c4:
            st.metric(
                "Competition",
                f"{competition_intensity}%",
            )

    st.write("")

    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    predict = st.button(
        "🚀 Predict Project Risk",
        type="primary",
        use_container_width=True,
    )

    # ========================================================
    # GENERATE PREDICTION
    # ========================================================

    if predict:

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not project_name.strip():

            st.error(
                "❌ Please enter the Project Name."
            )

            return

        if not target_market.strip():

            st.error(
                "❌ Please enter the Target Market."
            )

            return

        if not project_description.strip():

            st.warning(
                "⚠️ Project description is empty. "
                "You can continue, but a description is recommended."
            )

        # ----------------------------------------------------
        # CONVERT CONDITIONS TO RISK
        # ----------------------------------------------------

        # Higher demand = lower market risk
        market_risk = 100 - market_demand

        # Higher readiness = lower technical risk
        technical_risk = 100 - technical_readiness

        # Higher financial strength = lower financial risk
        financial_risk = 100 - financial_strength

        # Higher competition = higher competition risk
        competition_risk = competition_intensity

        # ----------------------------------------------------
        # GENERATE ASSESSMENT
        # ----------------------------------------------------

        assessment = generate_risk_assessment(
            market_score=market_risk,
            technical_score=technical_risk,
            financial_score=financial_risk,
            competition_score=competition_risk,
        )

        # ----------------------------------------------------
        # KEY FINDINGS
        # ----------------------------------------------------

        findings = generate_key_findings(
            market_risk=market_risk,
            technical_risk=technical_risk,
            financial_risk=financial_risk,
            competition_risk=competition_risk,
        )

        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        recommendations = generate_recommendations(
            market_risk=market_risk,
            technical_risk=technical_risk,
            financial_risk=financial_risk,
            competition_risk=competition_risk,
        )

        # ----------------------------------------------------
        # SAVE PROJECT INFORMATION
        # ----------------------------------------------------

        st.session_state["project_name"] = (
            project_name.strip()
        )

        st.session_state["project_description"] = (
            project_description.strip()
        )

        st.session_state["target_market"] = (
            target_market.strip()
        )

        st.session_state["budget"] = (
            budget.strip()
        )

        st.session_state["resources"] = (
            resources.strip()
        )

        st.session_state["objectives"] = (
            objectives.strip()
        )

        st.session_state["competition"] = (
            f"{competition_intensity}% intensity"
        )

        # Save original input values too
        st.session_state["market_demand"] = (
            market_demand
        )

        st.session_state["technical_readiness"] = (
            technical_readiness
        )

        st.session_state["financial_strength"] = (
            financial_strength
        )

        st.session_state["competition_intensity"] = (
            competition_intensity
        )

        # ----------------------------------------------------
        # SAVE PREDICTION
        # ----------------------------------------------------

        st.session_state["prediction"] = assessment

        st.session_state["key_findings"] = findings

        st.session_state["recommendations"] = recommendations

        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        save_prediction_history(
            assessment
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            "✅ Prediction generated successfully!"
        )

    # ========================================================
    # ALWAYS SHOW LATEST PREDICTION
    # ========================================================

    prediction = st.session_state.get(
        "prediction"
    )

    if prediction:

        st.write("")

        render_prediction_result(
            prediction
        )


# ============================================================
# DASHBOARD
# ============================================================

def render_dashboard():

    prediction = st.session_state.get(
        "prediction"
    )

    if prediction is None:

        st.info(
            "📌 No prediction available. "
            "Go to **🧠 New Prediction** and generate "
            "a project risk prediction first."
        )

        return

    st.markdown(
        "## 📊 Risk Analytics Dashboard"
    )

    st.caption(
        "Interactive analytics generated from "
        "your latest project assessment."
    )

    # ========================================================
    # KPI CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "⚠️ Overall Risk",
            f'{prediction["overall_risk"]:.1f}%',
            prediction["overall_level"],
        )

    with c2:

        st.metric(
            "🌎 Market Risk",
            f'{prediction["market_risk"]:.1f}%',
            prediction["market_level"],
        )

    with c3:

        st.metric(
            "⚙️ Technical Risk",
            f'{prediction["technical_risk"]:.1f}%',
            prediction["technical_level"],
        )

    with c4:

        st.metric(
            "🎯 Success Probability",
            f'{prediction["success_probability"]:.1f}%',
        )

    st.write("")

    # ========================================================
    # CHARTS
    # ========================================================

    chart_col1, chart_col2 = st.columns(
        [1.5, 1]
    )

    # ========================================================
    # RISK CATEGORY CHART
    # ========================================================

    with chart_col1:

        with st.container(border=True):

            st.markdown(
                "### 📊 Risk Category Analysis"
            )

            categories = [
                "Market",
                "Technical",
                "Financial",
                "Competition",
            ]

            values = [
                prediction["market_risk"],
                prediction["technical_risk"],
                prediction["financial_risk"],
                prediction["competition_risk"],
            ]

            levels = [
                prediction["market_level"],
                prediction["technical_level"],
                prediction["financial_level"],
                prediction["competition_level"],
            ]

            colors = [
                risk_color(level)
                for level in levels
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=categories,
                    y=values,
                    text=[
                        f"{value:.1f}%"
                        for value in values
                    ],
                    textposition="outside",
                    marker_color=colors,
                    marker_line_width=0,
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Risk Score: %{y:.1f}%"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                height=420,

                yaxis={
                    "title": "Risk Score (%)",
                    "range": [0, 110],
                    "gridcolor": "#eee7ff",
                },

                xaxis={
                    "title": "",
                },

                plot_bgcolor="rgba(0,0,0,0)",

                paper_bgcolor="rgba(0,0,0,0)",

                margin={
                    "l": 20,
                    "r": 20,
                    "t": 30,
                    "b": 40,
                },

                font={
                    "family": "Arial",
                    "color": "#374151",
                },

                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    # ========================================================
    # SUCCESS GAUGE
    # ========================================================

    with chart_col2:

        with st.container(border=True):

            st.markdown(
                "### 🎯 Success Probability"
            )

            success = float(
                prediction["success_probability"]
            )

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",

                    value=success,

                    number={
                        "suffix": "%",
                        "font": {
                            "size": 42,
                            "color": "#4c1d95",
                        },
                    },

                    gauge={
                        "axis": {
                            "range": [0, 100],
                            "tickcolor": "#6b7280",
                        },

                        "bar": {
                            "color": "#7c3aed",
                            "thickness": 0.25,
                        },

                        "bgcolor": "#f5f3ff",

                        "borderwidth": 0,

                        "steps": [
                            {
                                "range": [0, 30],
                                "color": "#fee2e2",
                            },
                            {
                                "range": [30, 60],
                                "color": "#fef3c7",
                            },
                            {
                                "range": [60, 100],
                                "color": "#dcfce7",
                            },
                        ],
                    },
                )
            )

            gauge.update_layout(
                height=420,

                paper_bgcolor="rgba(0,0,0,0)",

                margin={
                    "l": 20,
                    "r": 20,
                    "t": 30,
                    "b": 20,
                },
            )

            st.plotly_chart(
                gauge,
                use_container_width=True,
            )

    # ========================================================
    # REAL TREND CHART
    # ========================================================

    st.markdown(
        "### 📈 Risk Assessment Trend"
    )

    history = st.session_state.get(
        "risk_history",
        [],
    )

    if len(history) >= 2:

        df = pd.DataFrame(history)

        with st.container(border=True):

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["overall_risk"],
                    mode="lines+markers",
                    name="Overall Risk",
                    line={
                        "color": "#7c3aed",
                        "width": 4,
                    },
                    marker={
                        "size": 9,
                    },
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["market_risk"],
                    mode="lines+markers",
                    name="Market Risk",
                    line={
                        "color": "#db2777",
                        "width": 3,
                    },
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["technical_risk"],
                    mode="lines+markers",
                    name="Technical Risk",
                    line={
                        "color": "#9333ea",
                        "width": 3,
                    },
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["financial_risk"],
                    mode="lines+markers",
                    name="Financial Risk",
                    line={
                        "color": "#f59e0b",
                        "width": 3,
                    },
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["competition_risk"],
                    mode="lines+markers",
                    name="Competition Risk",
                    line={
                        "color": "#dc2626",
                        "width": 3,
                    },
                )
            )

            fig.update_layout(
                height=450,

                yaxis={
                    "title": "Risk Score (%)",
                    "range": [0, 100],
                    "gridcolor": "#eee7ff",
                },

                xaxis={
                    "title": "Assessment",
                },

                hovermode="x unified",

                plot_bgcolor="rgba(0,0,0,0)",

                paper_bgcolor="rgba(0,0,0,0)",

                margin={
                    "l": 20,
                    "r": 20,
                    "t": 30,
                    "b": 40,
                },

                legend={
                    "orientation": "h",
                    "y": 1.12,
                },
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    else:

        with st.container(border=True):

            st.info(
                "📈 Generate at least two predictions "
                "with different assessment values to "
                "display the real risk trend."
            )

    # ========================================================
    # PROJECT SUMMARY
    # ========================================================

    st.write("")

    with st.container(border=True):

        st.markdown(
            "### 📝 Project Risk Summary"
        )

        project_name = st.session_state.get(
            "project_name",
            "Unnamed Project",
        )

        st.write(
            f"**Project:** {project_name}"
        )

        st.write(
            f"**Overall Risk:** "
            f"{prediction['overall_risk']:.1f}% "
            f"({prediction['overall_level']})"
        )

        st.write(
            f"**Success Probability:** "
            f"{prediction['success_probability']:.1f}%"
        )


# ============================================================
# RISK ANALYTICS
# ============================================================

def render_risk_analytics():

    prediction = st.session_state.get(
        "prediction"
    )

    if prediction is None:

        st.warning(
            "⚠️ Please generate a prediction first."
        )

        return

    st.markdown(
        "## 🔍 Detailed Risk Analytics"
    )

    st.caption(
        "Detailed breakdown of the project's "
        "major risk categories."
    )

    # ========================================================
    # RISK TABLE
    # ========================================================

    data = pd.DataFrame(
        {
            "Risk Category": [
                "Market Risk",
                "Technical Risk",
                "Financial Risk",
                "Competition Risk",
            ],

            "Risk Score": [
                prediction["market_risk"],
                prediction["technical_risk"],
                prediction["financial_risk"],
                prediction["competition_risk"],
            ],

            "Risk Level": [
                prediction["market_level"],
                prediction["technical_level"],
                prediction["financial_level"],
                prediction["competition_level"],
            ],
        }
    )

    data["Risk Score"] = (
        data["Risk Score"]
        .round(2)
    )

    with st.container(border=True):

        st.markdown(
            "### 📋 Risk Summary"
        )

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
        )

    st.write("")

    # ========================================================
    # RISK BREAKDOWN
    # ========================================================

    st.markdown(
        "### ⚡ Risk Breakdown"
    )

    risks = [
        (
            "🌎",
            "Market Risk",
            prediction["market_risk"],
            prediction["market_level"],
        ),

        (
            "⚙️",
            "Technical Risk",
            prediction["technical_risk"],
            prediction["technical_level"],
        ),

        (
            "💰",
            "Financial Risk",
            prediction["financial_risk"],
            prediction["financial_level"],
        ),

        (
            "🏆",
            "Competition Risk",
            prediction["competition_risk"],
            prediction["competition_level"],
        ),
    ]

    col1, col2 = st.columns(2)

    for index, (
        icon,
        name,
        score,
        level,
    ) in enumerate(risks):

        target = (
            col1
            if index % 2 == 0
            else col2
        )

        with target:

            with st.container(border=True):

                st.markdown(
                    f"### {icon} {name}"
                )

                st.metric(
                    "Risk Score",
                    f"{score:.1f}%",
                )

                st.write(
                    f"{risk_icon(level)} "
                    f"**{level}**"
                )

                st.progress(
                    min(
                        max(
                            score / 100,
                            0
                        ),
                        1,
                    )
                )


# ============================================================
# ASSESSMENT REPORT
# ============================================================

def render_report():

    prediction = st.session_state.get(
        "prediction"
    )

    if prediction is None:

        st.warning(
            "⚠️ Please generate a prediction first."
        )

        return

    findings = st.session_state.get(
        "key_findings",
        [],
    )

    recommendations = st.session_state.get(
        "recommendations",
        [],
    )

    project_name = st.session_state.get(
        "project_name",
        "AI Startup Risk Analyzer",
    )

    st.markdown(
        "## 📋 Assessment Report"
    )

    st.caption(
        "Key findings, risk assessment, "
        "recommendations and export options."
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    with st.container(border=True):

        st.markdown(
            f"### 🚀 {project_name}"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Overall Risk",
                f'{prediction["overall_risk"]:.1f}%',
            )

        with c2:

            st.metric(
                "Risk Level",
                prediction["overall_level"],
            )

        with c3:

            st.metric(
                "Success Probability",
                f'{prediction["success_probability"]:.1f}%',
            )

    st.write("")

    # ========================================================
    # KEY FINDINGS
    # ========================================================

    st.markdown(
        "### 🔎 1. Key Findings"
    )

    if isinstance(
        findings,
        (list, tuple),
    ):

        for index, finding in enumerate(
            findings,
            start=1,
        ):

            with st.container(border=True):

                st.markdown(
                    f"**Finding {index}**"
                )

                st.write(
                    finding
                )

    else:

        with st.container(border=True):

            st.write(
                findings
            )

    # ========================================================
    # RISK ASSESSMENT
    # ========================================================

    st.markdown(
        "### ⚠️ 2. Risk Assessment"
    )

    risk_items = [
        (
            "Overall Risk",
            prediction["overall_risk"],
            prediction["overall_level"],
        ),

        (
            "Market Risk",
            prediction["market_risk"],
            prediction["market_level"],
        ),

        (
            "Technical Risk",
            prediction["technical_risk"],
            prediction["technical_level"],
        ),

        (
            "Financial Risk",
            prediction["financial_risk"],
            prediction["financial_level"],
        ),

        (
            "Competition Risk",
            prediction["competition_risk"],
            prediction["competition_level"],
        ),
    ]

    for name, score, level in risk_items:

        with st.container(border=True):

            c1, c2, c3 = st.columns(
                [2, 1, 2]
            )

            with c1:

                st.write(
                    f"{risk_icon(level)} "
                    f"**{name}**"
                )

            with c2:

                st.write(
                    f"**{score:.1f}%**"
                )

            with c3:

                st.write(
                    level
                )

                st.progress(
                    min(
                        max(
                            score / 100,
                            0
                        ),
                        1,
                    )
                )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown(
        "### 💡 3. Recommendations"
    )

    if isinstance(
        recommendations,
        (list, tuple),
    ):

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            with st.container(border=True):

                st.markdown(
                    f"**Recommendation {index}**"
                )

                st.write(
                    recommendation
                )

    else:

        with st.container(border=True):

            st.write(
                recommendations
            )

    # ========================================================
    # EXPORT
    # ========================================================

    st.markdown(
        "### 📤 Export Assessment"
    )

    report_data = {
        "project_name":
            project_name,

        "project_description":
            st.session_state.get(
                "project_description",
                "",
            ),

        "target_market":
            st.session_state.get(
                "target_market",
                "",
            ),

        "budget":
            st.session_state.get(
                "budget",
                "",
            ),

        "competition":
            st.session_state.get(
                "competition",
                "",
            ),

        "resources":
            st.session_state.get(
                "resources",
                "",
            ),

        "objectives":
            st.session_state.get(
                "objectives",
                "",
            ),

        "overall_risk":
            prediction["overall_risk"],

        "market_risk":
            prediction["market_risk"],

        "technical_risk":
            prediction["technical_risk"],

        "financial_risk":
            prediction["financial_risk"],

        "competition_risk":
            prediction["competition_risk"],

        "success_probability":
            prediction["success_probability"],

        "overall_level":
            prediction["overall_level"],

        "market_level":
            prediction["market_level"],

        "technical_level":
            prediction["technical_level"],

        "financial_level":
            prediction["financial_level"],

        "competition_level":
            prediction["competition_level"],

        "key_findings":
            findings,

        "recommendations":
            recommendations,

        "generated_at":
            datetime.now().strftime(
                "%d %B %Y, %I:%M %p"
            ),
    }

    try:

        pdf_file = generate_pdf_report(
            report_data
        )

        text_file = generate_text_report(
            report_data
        )

        # ----------------------------------------------------
        # Make sure text is downloadable
        # ----------------------------------------------------

        if isinstance(
            text_file,
            str,
        ):
            text_data = text_file.encode(
                "utf-8"
            )
        else:
            text_data = text_file

        # ----------------------------------------------------
        # Download buttons
        # ----------------------------------------------------

        c1, c2 = st.columns(2)

        with c1:

            st.download_button(
                "📄 Download PDF Report",

                data=pdf_file.getvalue(),

                file_name=(
                    "startup_risk_assessment.pdf"
                ),

                mime="application/pdf",

                use_container_width=True,
            )

        with c2:

            st.download_button(
                "📝 Download Text Report",

                data=text_data,

                file_name=(
                    "startup_risk_assessment.txt"
                ),

                mime="text/plain",

                use_container_width=True,
            )

    except Exception as error:

        st.error(
            f"❌ Report generation failed: {error}"
        )


# ============================================================
# PROJECT INFORMATION
# ============================================================

def render_project_information():

    project_name = st.session_state.get(
        "project_name",
        "",
    )

    if not project_name:

        st.info(
            "📌 Generate a prediction first "
            "to view project information."
        )

        return

    st.markdown(
        "## 📁 Project Information"
    )

    fields = [
        (
            "Project Name",
            project_name,
        ),

        (
            "Project Description",
            st.session_state.get(
                "project_description",
                "",
            ),
        ),

        (
            "Target Market",
            st.session_state.get(
                "target_market",
                "",
            ),
        ),

        (
            "Available Budget",
            st.session_state.get(
                "budget",
                "",
            ),
        ),

        (
            "Competition",
            st.session_state.get(
                "competition",
                "",
            ),
        ),

        (
            "Available Resources",
            st.session_state.get(
                "resources",
                "",
            ),
        ),

        (
            "Project Objectives",
            st.session_state.get(
                "objectives",
                "",
            ),
        ),
    ]

    for title, value in fields:

        with st.container(border=True):

            st.markdown(
                f"### {title}"
            )

            st.write(
                value
                if value
                else "Not provided"
            )


# ============================================================
# FOOTER
# ============================================================

def render_footer():

    st.markdown(
        '<div class="footer-line"></div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "AI Startup Risk Analyzer • "
        "Milestone 4 • "
        "Python • Streamlit • Plotly • Pandas • ReportLab"
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    selected_page = render_sidebar()

    render_hero()

    # --------------------------------------------------------
    # PAGE ROUTING
    # --------------------------------------------------------

    if selected_page == "🧠 New Prediction":

        render_prediction_page()

    elif selected_page == "📊 Dashboard":

        render_dashboard()

    elif selected_page == "🔍 Risk Analytics":

        render_risk_analytics()

    elif selected_page == "📋 Assessment Report":

        render_report()

    elif selected_page == "📁 Project Information":

        render_project_information()

    render_footer()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    main()