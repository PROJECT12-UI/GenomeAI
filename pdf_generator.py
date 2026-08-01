from reportlab.lib import colors

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    TableStyle,

    PageBreak

)

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

import os



# =====================================================
# REGISTER FONT
# =====================================================

try:

    pdfmetrics.registerFont(

        TTFont(

            "Poppins",

            "Poppins-Regular.ttf"

        )

    )

    FONT_NAME = "Poppins"

except:

    FONT_NAME = "Helvetica"



# =====================================================
# PDF GENERATOR
# =====================================================

class GenomePDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.title_style = self.styles["Heading1"]

        self.title_style.alignment = TA_CENTER

        self.title_style.fontName = FONT_NAME

        self.title_style.textColor = colors.HexColor("#0F4C81")

        self.title_style.spaceAfter = 25

        self.heading_style = self.styles["Heading2"]

        self.heading_style.fontName = FONT_NAME

        self.heading_style.textColor = colors.HexColor("#0F4C81")

        self.normal_style = self.styles["BodyText"]

        self.normal_style.fontName = FONT_NAME

        self.normal_style.leading = 20



# =====================================================
# CREATE PDF
# =====================================================

    def create_pdf(

        self,

        filename,

        report

    ):

        doc = SimpleDocTemplate(

            filename,

            rightMargin=40,

            leftMargin=40,

            topMargin=40,

            bottomMargin=40

        )

        story = []



# =====================================================
# TITLE
# =====================================================

        story.append(

            Paragraph(

                "GenomeAI Clinical Report",

                self.title_style

            )

        )

        story.append(

            Paragraph(

                "Artificial Intelligence Based Future Baby Genome Analysis",

                self.normal_style

            )

        )

        story.append(

            Spacer(

                1,

                0.35 * inch

            )

        )
        # =====================================================
# REPORT INFORMATION
# =====================================================

        story.append(

            Paragraph(

                "Report Information",

                self.heading_style

            )

        )

        report_info = [

            ["Report Date", report.get("report_date", "N/A")],

            ["Health Score", f'{report.get("health_score", 0)}%'],

            ["High Risk", str(report.get("high_risk", 0))],

            ["Medium Risk", str(report.get("medium_risk", 0))],

            ["Low Risk", str(report.get("low_risk", 0))],

            ["AI Simulations", str(report.get("total_samples", 0))]

        ]

        table = Table(

            report_info,

            colWidths=[180, 280]

        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#0F4C81")),

                ("TEXTCOLOR", (0,0), (0,-1), colors.white),

                ("BACKGROUND", (1,0), (1,-1), colors.whitesmoke),

                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

                ("FONTNAME", (0,0), (-1,-1), FONT_NAME),

                ("BOTTOMPADDING", (0,0), (-1,-1), 10),

                ("TOPPADDING", (0,0), (-1,-1), 10),

                ("VALIGN", (0,0), (-1,-1), "MIDDLE")

            ])

        )

        story.append(table)

        story.append(Spacer(1, 0.30 * inch))


# =====================================================
# DISEASE ANALYSIS
# =====================================================

        story.append(

            Paragraph(

                "Disease Analysis",

                self.heading_style

            )

        )

        diseases = report.get("diseases", [])

        if diseases:

            disease_data = [

                [

                    "Disease",

                    "Gene",

                    "Inheritance",

                    "Risk"

                ]

            ]

            for disease in diseases:

                disease_data.append(

                    [

                        disease.get("name", "-"),

                        disease.get("gene", "-"),

                        disease.get("inheritance", "-"),

                        disease.get("risk_level", "-")

                    ]

                )

            disease_table = Table(

                disease_data,

                colWidths=[150, 90, 120, 80]

            )

            disease_table.setStyle(

                TableStyle([

                    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F4C81")),

                    ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

                    ("FONTNAME", (0,0), (-1,-1), FONT_NAME),

                    ("BACKGROUND", (0,1), (-1,-1), colors.beige),

                    ("BOTTOMPADDING", (0,0), (-1,-1), 8),

                    ("TOPPADDING", (0,0), (-1,-1), 8)

                ])

            )

            story.append(disease_table)

        else:

            story.append(

                Paragraph(

                    "No disease information available.",

                    self.normal_style

                )

            )

        story.append(

            Spacer(

                1,

                0.30 * inch

            )

        )
        # =====================================================
# AI SUMMARY
# =====================================================

        story.append(

            Paragraph(

                "Artificial Intelligence Summary",

                self.heading_style

            )

        )

        ai_summary = f"""

        GenomeAI analyzed the uploaded maternal and paternal
        genome sequences using Artificial Intelligence and
        statistical inheritance prediction.

        The overall predicted health score is
        <b>{report.get("health_score",0)}%</b>.

        Predicted Disease:
        <b>{report.get("predicted_disease","Not Available")}</b>

        Risk Level:
        <b>{report.get("risk_level","Unknown")}</b>.

        """

        story.append(

            Paragraph(

                ai_summary,

                self.normal_style

            )

        )

        story.append(

            Spacer(

                1,

                0.30 * inch

            )

        )


# =====================================================
# MEDICAL RECOMMENDATION
# =====================================================

        story.append(

            Paragraph(

                "Medical Recommendation",

                self.heading_style

            )

        )

        recommendation = report.get(

            "recommendation",

            "No recommendation available."

        )

        story.append(

            Paragraph(

                recommendation,

                self.normal_style

            )

        )

        story.append(

            Spacer(

                1,

                0.30 * inch

            )

        )


# =====================================================
# DISCLAIMER
# =====================================================

        story.append(

            Paragraph(

                "Disclaimer",

                self.heading_style

            )

        )

        disclaimer = """

        This report was generated automatically by
        GenomeAI using Artificial Intelligence.

        The report is intended only for educational,
        research and decision-support purposes.

        Clinical diagnosis should always be confirmed
        by qualified healthcare professionals and
        laboratory testing.

        """

        story.append(

            Paragraph(

                disclaimer,

                self.normal_style

            )

        )

        story.append(

            Spacer(

                1,

                0.40 * inch

            )

        )


# =====================================================
# FOOTER
# =====================================================

        story.append(

            Paragraph(

                "<b>GenomeAI Clinical Decision Support System</b>",

                self.title_style

            )

        )


# =====================================================
# BUILD PDF
# =====================================================

        doc.build(

            story

        )

        return filename