import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generate_exam_pdf(mock_data, file_path="exam_paper.pdf"):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=pagesizes.A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # ----------------------------
    # PAGE 1 - QUESTION PAPER
    # ----------------------------

    elements.append(Paragraph("<b>Olympiad Mastery AI</b>", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    header_data = [
        ["Class:", "5", "Subject:", "Science"],
        ["Chapter:", mock_data["chapter"], "Time:", "1 Hour"],
        ["Total Marks:", str(len(mock_data["questions"]) * 2)]
    ]

    table = Table(header_data, colWidths=[80, 150, 80, 150])
    table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # Instructions
    elements.append(Paragraph("<b>Instructions:</b>", styles["Heading3"]))
    elements.append(Paragraph("1. All questions are compulsory.", normal_style))
    elements.append(Paragraph("2. Each question carries 2 marks.", normal_style))
    elements.append(Paragraph("3. Choose the correct answer.", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Section A - Multiple Choice Questions</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Questions
    for q in mock_data["questions"]:
        elements.append(Paragraph(f"<b>Q{q['id']}.</b> {q['question']} (2 Marks)", normal_style))
        elements.append(Spacer(1, 0.1 * inch))

        for option in q["options"]:
            elements.append(Paragraph(f"• {option}", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

    # ----------------------------
    # PAGE BREAK
    # ----------------------------
    elements.append(PageBreak())

    # ----------------------------
    # PAGE 2 - ANSWER KEY
    # ----------------------------
    elements.append(Paragraph("<b>Answer Key</b>", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    for q in mock_data["questions"]:
        elements.append(Paragraph(f"Q{q['id']}: {q['correct_answer']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return file_path
