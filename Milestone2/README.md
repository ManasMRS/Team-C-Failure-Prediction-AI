# Prediction AI — Milestone 2 (Streamlit App)

An interactive tool covering the full Milestone 2 flow:
**Risk Assessment → Risk Scoring → SWOT Analysis → Feasibility Assessment → Final Recommendation.**

## What it does

1. **Project Information** — name and short description (sidebar).
2. **Risk Assessment** — sliders (1–5) for the five risk types: Market, Financial,
   Competition, Technical, Operational. Each has an expandable "What is this?" note
   with the meaning, an example, and the key question, straight from the course content.
3. **Risk Scoring Engine** — automatically averages the five scores into an overall
   Risk Score (1–5) and label (Very Low → Very High Risk), plus a bar chart.
4. **SWOT Analysis** — free-text entry (one item per line) for Strengths, Weaknesses,
   Opportunities, and Threats, summarized in a quick-view grid.
5. **Feasibility Assessment** — combines the risk score and SWOT balance into a
   0–100 Feasibility Score, banded into Highly Feasible / Feasible / Moderately
   Feasible / Not Feasible.
6. **Final Recommendation** — a plain-language summary pulling together the risk
   level, feasibility band, and top strength/threat.

A **"Load Example Project"** button in the sidebar fills everything in with the
AI-Based Online Learning Platform example from the class slides, so students can
see the tool work end-to-end before entering their own project.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Notes for instructors

- The feasibility formula (in `compute_feasibility()` in `app.py`) is intentionally
  simple and documented in the code — 60% weight on inverse average risk, 40% weight
  on the SWOT positive/negative balance. Feel free to tune the weights as a class
  exercise, or ask students to propose their own formula.
- All five risk definitions, the 1–5 risk scale, and the feasibility bands are
  pulled directly from the Milestone 2 slide deck so the app stays consistent with
  the lesson.
