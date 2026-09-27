"""
Report Generator Module

Generates:
1. TXT reports
2. PDF reports
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_text_report(data):
    """
    Generate a downloadable TXT report.
    """

    project_name = data.get(
        "project_name",
        "AI Startup Risk Analyzer"
    )

    report = f"""
============================================================
              PROJECT RISK ASSESSMENT REPORT
============================================================

Project Name:
{project_name}

Generated:
{datetime.now().strftime("%d %B %Y, %I:%M %p")}


============================================================
1. KEY FINDINGS
============================================================

"""

    for index, finding in enumerate(
        data.get("key_findings", []),
        start=1
    ):

        report += f"{index}. {finding}\n"


    report += f"""

============================================================
2. RISK ASSESSMENT
============================================================

Overall Risk:
{data.get("overall_risk", 0):.0f}%

Market Risk:
{data.get("market_risk", 0):.0f}%

Technical Risk:
{data.get("technical_risk", 0):.0f}%

Financial Risk:
{data.get("financial_risk", 0):.0f}%

Competition Risk:
{data.get("competition_risk", 0):.0f}%

Success Probability:
{data.get("success_probability", 0):.0f}%


============================================================
3. RECOMMENDATIONS
============================================================

"""

    for index, recommendation in enumerate(
        data.get("recommendations", []),
        start=1
    ):

        report += (
            f"{index}. {recommendation}\n"
        )


    report += """

============================================================
                  END OF REPORT
============================================================
"""

    return report


def generate_pdf_report(data):
    """
    Generate a PDF report and return it as BytesIO.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#6D28D9"),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#7E22CE"),
        spaceBefore=18,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#374151")
    )

    story = []

    project_name = data.get(
        "project_name",
        "AI Startup Risk Analyzer"
    )

    # Title
    story.append(
        Paragraph(
            "PROJECT RISK ASSESSMENT REPORT",
            title_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Project:</b> {project_name}",
            body_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            body_style
        )
    )

    story.append(
        Spacer(1, 20)
    )


    # --------------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "1. Key Findings",
            heading_style
        )
    )

    for finding in data.get(
        "key_findings",
        []
    ):

        story.append(
            Paragraph(
                f"• {finding}",
                body_style
            )
        )

        story.append(
            Spacer(1, 5)
        )


    # --------------------------------------------------------
    # RISK ASSESSMENT
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "2. Risk Assessment",
            heading_style
        )
    )

    table_data = [
        ["Metric", "Score", "Level"],

        [
            "Overall Risk",
            f"{data.get('overall_risk', 0):.0f}%",
            data.get("overall_level", "")
        ],

        [
            "Market Risk",
            f"{data.get('market_risk', 0):.0f}%",
            data.get("market_level", "")
        ],

        [
            "Technical Risk",
            f"{data.get('technical_risk', 0):.0f}%",
            data.get("technical_level", "")
        ],

        [
            "Financial Risk",
            f"{data.get('financial_risk', 0):.0f}%",
            data.get("financial_level", "")
        ],

        [
            "Competition Risk",
            f"{data.get('competition_risk', 0):.0f}%",
            data.get("competition_level", "")
        ],

        [
            "Success Probability",
            f"{data.get('success_probability', 0):.0f}%",
            "Estimated"
        ]
    ]

    table = Table(
        table_data,
        colWidths=[
            2.7 * inch,
            1.2 * inch,
            1.5 * inch
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#7E22CE")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#E9D5FF")
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#FAF5FF")
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    story.append(table)


    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "3. Recommendations",
            heading_style
        )
    )

    for recommendation in data.get(
        "recommendations",
        []
    ):

        story.append(
            Paragraph(
                f"• {recommendation}",
                body_style
            )
        )

        story.append(
            Spacer(1, 5)
        )


    story.append(
        Spacer(1, 25)
    )

    story.append(
        Paragraph(
            "Generated by AI Risk Analytics Dashboard",
            body_style
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer