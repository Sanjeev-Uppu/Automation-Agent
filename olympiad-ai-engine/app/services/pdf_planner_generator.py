from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_planner_pdf(plan_data, file_path):

    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    elements.append(Paragraph("<b>Study Planner</b>", styles["Heading1"]))
    elements.append(Spacer(1, 0.5 * inch))

    for day in plan_data.get("plan", []):
        elements.append(Paragraph(f"<b>Day {day['day']}</b>", normal_style))
        elements.append(Paragraph(f"Topics: {day['topics']}", normal_style))
        elements.append(Paragraph(f"Tasks: {day['tasks']}", normal_style))
        elements.append(Spacer(1, 0.3 * inch))

    doc.build(elements)

    return file_path
