"""
Recommendation Module

Generates recommendations based on risk scores
from the Risk Assessment module.
"""


def generate_recommendations(
    market_risk,
    technical_risk,
    financial_risk,
    competition_risk
):

    recommendations = []

    # Market recommendation
    if market_risk >= 60:

        recommendations.append(
            "Conduct additional market research and "
            "validate customer demand before scaling."
        )

    elif market_risk >= 30:

        recommendations.append(
            "Continue monitoring market demand and "
            "validate the product with target users."
        )

    else:

        recommendations.append(
            "Maintain market research and monitor "
            "changes in customer demand."
        )


    # Technical recommendation
    if technical_risk >= 60:

        recommendations.append(
            "Create a stronger technical roadmap and "
            "address major implementation risks."
        )

    elif technical_risk >= 30:

        recommendations.append(
            "Strengthen the development roadmap and "
            "perform regular technical testing."
        )

    else:

        recommendations.append(
            "Continue regular testing and maintain "
            "the existing technical architecture."
        )


    # Financial recommendation
    if financial_risk >= 60:

        recommendations.append(
            "Review the project budget carefully and "
            "establish stronger financial controls."
        )

    elif financial_risk >= 30:

        recommendations.append(
            "Monitor development costs and maintain "
            "a controlled project budget."
        )

    else:

        recommendations.append(
            "Continue monitoring operational and "
            "development expenses."
        )


    # Competition recommendation
    if competition_risk >= 60:

        recommendations.append(
            "Develop stronger product differentiation "
            "and continuously monitor competitors."
        )

    elif competition_risk >= 30:

        recommendations.append(
            "Monitor competitor products, pricing and "
            "features to maintain differentiation."
        )

    else:

        recommendations.append(
            "Continue monitoring the competitive landscape."
        )


    return recommendations


def generate_key_findings(
    market_risk,
    technical_risk,
    financial_risk,
    competition_risk
):

    findings = []

    # Market
    if market_risk >= 60:

        findings.append(
            "The project has significant market-related "
            "uncertainty that requires additional validation."
        )

    elif market_risk >= 30:

        findings.append(
            "The project shows potential market opportunity "
            "with some demand-related uncertainty."
        )

    else:

        findings.append(
            "Market-related risk is relatively controlled."
        )


    # Technical
    if technical_risk >= 60:

        findings.append(
            "Technical implementation represents a "
            "significant area of project risk."
        )

    elif technical_risk >= 30:

        findings.append(
            "Technical implementation is feasible but "
            "requires continuous monitoring."
        )

    else:

        findings.append(
            "Technical implementation risk is relatively low."
        )


    # Financial
    if financial_risk >= 60:

        findings.append(
            "Financial sustainability requires careful "
            "budget planning and monitoring."
        )

    elif financial_risk >= 30:

        findings.append(
            "Financial planning should be monitored "
            "throughout development."
        )

    else:

        findings.append(
            "Financial risk is currently relatively controlled."
        )


    # Competition
    if competition_risk >= 60:

        findings.append(
            "Strong competitive pressure may affect "
            "project adoption."
        )

    elif competition_risk >= 30:

        findings.append(
            "Competition requires continuous product "
            "differentiation."
        )

    else:

        findings.append(
            "Competition-related risk is currently manageable."
        )


    return findings