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


def generate_question_paper_pdf(
    question_data,
    file_path="question_paper.pdf"
):

    if "questions" not in question_data or not question_data["questions"]:
        raise ValueError("Invalid question paper data")

    school_name = question_data["school_name"]
    grade = question_data["grade"]
    subject = question_data["subject"]
    chapter = question_data["chapter"]
    difficulty = question_data.get("difficulty_level", "Not Specified")
    duration = question_data["duration_minutes"]
    marks_per_question = question_data["marks_per_question"]
    questions = question_data["questions"]

    total_questions = len(questions)
    total_marks = total_questions * marks_per_question

    # ---------------- DOCUMENT SETUP ----------------
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

    # ---------------- HEADER ----------------
    elements.append(Paragraph(f"<b>{school_name}</b>", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    header_table_data = [
        ["Grade:", str(grade), "Subject:", subject],
        ["Chapter:", chapter, "Difficulty:", difficulty],
        ["Duration:", f"{duration} Minutes", "Total Marks:", str(total_marks)],
        ["Total Questions:", str(total_questions), "Marks per Question:", str(marks_per_question)]
    ]

    table = Table(header_table_data, colWidths=[120, 140, 120, 120])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))

    # ---------------- INSTRUCTIONS ----------------
    elements.append(Paragraph("<b>Instructions:</b>", styles["Heading3"]))
    elements.append(Paragraph("1. All questions are compulsory.", normal_style))
    elements.append(Paragraph(f"2. Each question carries {marks_per_question} marks.", normal_style))
    elements.append(Paragraph("3. Choose the correct option.", normal_style))
    elements.append(Paragraph(f"4. Total Duration: {duration} Minutes.", normal_style))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("<b>Section A - Multiple Choice Questions</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------------- QUESTIONS ----------------
    for index, q in enumerate(questions, start=1):

        q_text = q["question"]
        options = q["options"]

        elements.append(
            Paragraph(f"<b>Q{index}.</b> {q_text} ({marks_per_question} Marks)", normal_style)
        )
        elements.append(Spacer(1, 0.15 * inch))

        for option in options:
            elements.append(Paragraph(f"• {option}", normal_style))

        elements.append(Spacer(1, 0.35 * inch))

    # ---------------- ANSWER KEY PAGE ----------------
    elements.append(PageBreak())
    elements.append(Paragraph("<b>Answer Key</b>", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    for index, q in enumerate(questions, start=1):
        elements.append(
            Paragraph(f"Q{index}: {q['correct_answer']}", normal_style)
        )
        elements.append(Spacer(1, 0.2 * inch))

    # ---------------- BUILD ----------------
    doc.build(elements)

    return file_path