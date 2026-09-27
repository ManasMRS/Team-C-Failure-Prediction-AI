"""
Risk Assessment Module

This module calculates the major project risk metrics
used by the Milestone 4 Risk Analytics Dashboard.
"""


def calculate_risk_score(
    market_score,
    technical_score,
    financial_score,
    competition_score
):
    """
    Calculate the overall project risk.

    Each input should be between 0 and 100.
    Higher score = higher risk.
    """

    scores = [
        market_score,
        technical_score,
        financial_score,
        competition_score
    ]

    # Keep values within 0-100
    scores = [
        max(0, min(100, float(score)))
        for score in scores
    ]

    overall_risk = sum(scores) / len(scores)

    return round(overall_risk, 2)


def calculate_success_probability(overall_risk):
    """
    Convert overall risk into estimated success probability.

    Higher risk results in lower estimated probability.
    """

    overall_risk = max(0, min(100, float(overall_risk)))

    success_probability = 100 - overall_risk

    return round(success_probability, 2)


def get_risk_level(score):
    """
    Convert a numerical risk score into a risk level.
    """

    score = float(score)

    if score < 30:
        return "Low Risk"

    elif score < 60:
        return "Moderate Risk"

    else:
        return "High Risk"


def generate_risk_assessment(
    market_score,
    technical_score,
    financial_score,
    competition_score
):
    """
    Generate complete risk assessment data.
    """

    overall_risk = calculate_risk_score(
        market_score,
        technical_score,
        financial_score,
        competition_score
    )

    success_probability = calculate_success_probability(
        overall_risk
    )

    return {
        "overall_risk": overall_risk,

        "market_risk": round(float(market_score), 2),

        "technical_risk": round(
            float(technical_score),
            2
        ),

        "financial_risk": round(
            float(financial_score),
            2
        ),

        "competition_risk": round(
            float(competition_score),
            2
        ),

        "success_probability": success_probability,

        "overall_level": get_risk_level(
            overall_risk
        ),

        "market_level": get_risk_level(
            market_score
        ),

        "technical_level": get_risk_level(
            technical_score
        ),

        "financial_level": get_risk_level(
            financial_score
        ),

        "competition_level": get_risk_level(
            competition_score
        )
    }