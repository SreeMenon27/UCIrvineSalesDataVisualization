from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors


class ReportGenerator:

    def generate_level_1_report(self, data, output_file):
        self.output_file = output_file

        #Create pdf document
        doc = SimpleDocTemplate(output_file, pagesize = A4)
        styles = getSampleStyleSheet()
        story = []

        # Add heading
        story.append(Paragraph("LEVEL-1 ANALYSIS", styles["Heading1"]))
        story.append(Spacer(1,6))
        story.append(Paragraph(data["description"], styles["BodyText"]))
        story.append(Spacer(1,12))

        # Add column descriptions table
        story.append(Paragraph("🧾 Column Descriptions", styles["Heading2"]))
        story.append(Spacer(1, 6))

        col_data = [["Column", "Description"]] + [[k, v] for k, v in data["column_descriptions"].items()]
        col_table = Table(col_data, hAlign='LEFT')
        col_table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')])
        story.append(col_table)
        story.append(Spacer(1, 12))

        # Add Data Types Table
        story.append(Paragraph("🔎 Column Data Types", styles["Heading2"]))
        story.append(Spacer(1, 6))

        type_data = [["Column", "Data Type"]] + [[k, v] for k, v in data["data_types"].items()]
        type_table = Table(type_data, hAlign='LEFT')
        type_table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')])
        story.append(type_table)
        story.append(Spacer(1, 12))

        # Add Interesting Facts
        story.append(Paragraph("📊 Interesting Facts", styles["Heading2"]))
        story.append(Spacer(1, 6))

        facts = data["interesting_facts"]
        story.append(Paragraph(f"• {facts['interesting_fact1']}", styles["BodyText"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"• {facts['interesting_fact2']}", styles["BodyText"]))
        story.append(Spacer(1, 12))

        doc.build(story)






