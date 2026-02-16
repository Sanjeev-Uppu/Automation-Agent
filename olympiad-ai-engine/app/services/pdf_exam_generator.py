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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch


def generate_exam_pdf(mock_data, file_path="exam_paper.pdf"):

    # ----------------------------
    # SAFETY CHECKS
    # ----------------------------
    if "questions" not in mock_data or not mock_data["questions"]:
        raise ValueError("Invalid mock data: Questions missing")

    chapter = mock_data.get("chapter", "Unknown Chapter")
    duration = mock_data.get("duration_minutes", 60)
    questions = mock_data["questions"]

    total_marks = len(questions) * 2

    # ----------------------------
    # DOCUMENT SETUP
    # ----------------------------
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
        ["Chapter:", chapter, "Duration:", f"{duration} Minutes"],
        ["Total Questions:", str(len(questions)), "Total Marks:", str(total_marks)]
    ]

    table = Table(header_data, colWidths=[110, 160, 110, 110])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke)
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

    # ----------------------------
    # QUESTIONS
    # ----------------------------
    for q in questions:

        q_id = q.get("id", "")
        q_text = q.get("question", "")
        options = q.get("options", [])

        elements.append(
            Paragraph(f"<b>Q{q_id}.</b> {q_text} (2 Marks)", normal_style)
        )
        elements.append(Spacer(1, 0.1 * inch))

        for option in options:
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

    for q in questions:
        q_id = q.get("id", "")
        answer = q.get("correct_answer", "")
        elements.append(
            Paragraph(f"Q{q_id}: {answer}", normal_style)
        )
        elements.append(Spacer(1, 0.2 * inch))

    # ----------------------------
    # BUILD PDF
    # ----------------------------
    doc.build(elements)

    return file_path
