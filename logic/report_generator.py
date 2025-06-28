from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch


class ReportGenerator:

    def _build_level_1_content(self, data):
        styles = getSampleStyleSheet()
        normal_style = styles["BodyText"]
        story = []

        # Add heading
        story.append(Paragraph("LEVEL-1 ANALYSIS", styles["Heading1"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(data["description"], normal_style))
        story.append(Spacer(1, 12))

        # Column Descriptions Table
        story.append(Paragraph("🧾 Column Descriptions", styles["Heading2"]))
        story.append(Spacer(1, 6))

        col_data = [["Column", "Description"]] + [
            [k, Paragraph(v, normal_style)] for k, v in data["column_descriptions"].items()]
        col_table = Table(col_data, colWidths=[100, 350], hAlign='LEFT')
        col_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ])
        story.append(col_table)
        story.append(Spacer(1, 12))

        # Data Types Table
        story.append(Paragraph("🔎 Column Data Types", styles["Heading2"]))
        story.append(Spacer(1, 6))

        type_data = [["Column", "Data Type"]] + [
            [k, v] for k, v in data["data_types"].items()]
        type_table = Table(type_data, colWidths=[100, 100], hAlign='LEFT')
        type_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ])
        story.append(type_table)
        story.append(Spacer(1, 12))

        # Interesting Facts
        story.append(Paragraph("📊 Interesting Facts", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"• {data['interesting_facts']['interesting_fact1']}", normal_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"• {data['interesting_facts']['interesting_fact2']}", normal_style))
        story.append(Spacer(1, 12))

        return story

    def generate_level_1_report(self, data, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = self._build_level_1_content(data)
        doc.build(story)

    def generate_level_2_report(self, data_level1, data_level2, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = self._build_level_1_content(data_level1)

        styles = getSampleStyleSheet()
        story.append(Spacer(1, 12))
        story.append(PageBreak())  # page break
        story.append(Paragraph("📈 LEVEL-2 ANALYSIS", styles["Heading1"]))
        story.append(Spacer(1, 12))

        # Add plots from data_level2 (paths stored in data_level2 dict)
        plot_titles = {
            "country_revenue_plot": "Top 10 Countries by Revenue",
            "monthly_revenue_plot": "Monthly Revenue Trend",
            "product_quantity_plot": "Top 10 Products by Quantity Sold"
        }

        for key, title in plot_titles.items():
            if key in data_level2:
                story.append(Paragraph(f"🖼️ {title}", styles["Heading2"]))
                story.append(Spacer(1, 6))
                img = Image(data_level2[key], width=6.0*inch, height=4.0*inch)
                story.append(img)
                story.append(Spacer(1, 12))

        doc.build(story)

    def generate_level_3_report(self, data_level1, data_level2, data_level3, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = self._build_level_1_content(data_level1)

        styles = getSampleStyleSheet()
        story.append(PageBreak())
        story.append(Paragraph("📈 LEVEL-2 ANALYSIS", styles["Heading1"]))
        story.append(Spacer(1, 12))

        plot_titles_level2 = {
            "country_revenue_plot": "Top 10 Countries by Revenue",
            "monthly_revenue_plot": "Monthly Revenue Trend",
            "product_quantity_plot": "Top 10 Products by Quantity Sold"
        }

        for key, title in plot_titles_level2.items():
            if key in data_level2:
                story.append(Paragraph(f"🖼️ {title}", styles["Heading2"]))
                story.append(Spacer(1, 6))
                img = Image(data_level2[key], width=6.0*inch, height=4.0*inch)
                story.append(img)
                story.append(Spacer(1, 12))

        story.append(PageBreak())
        story.append(Paragraph("📊 LEVEL-3 ANALYSIS", styles["Heading1"]))
        story.append(Spacer(1, 12))

        plot_titles_level3 = {
            "correlation_matrix_plot": "Correlation Heatmap of Numeric Features",
            "revenue_kde_plot": "Revenue Distribution (KDE Plot)",
            "scatter_quantity_revenue_plot": "Quantity vs Revenue by Country",
            "price_boxplot_plot": "Unit Price Distribution by Top 5 Countries"
        }

        for key, title in plot_titles_level3.items():
            if key in data_level3:
                story.append(Paragraph(f"🖼️ {title}", styles["Heading2"]))
                story.append(Spacer(1, 6))
                img = Image(data_level3[key], width=6.0*inch, height=4.0*inch)
                story.append(img)
                story.append(Spacer(1, 12))

        doc.build(story)
