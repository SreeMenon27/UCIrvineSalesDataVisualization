from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
from datetime import datetime
from reportlab.lib.enums import TA_CENTER

class ReportGenerator:
    def __init__(self):
        styles = getSampleStyleSheet()
        self.centered_heading1 = ParagraphStyle(
            name='CenteredHeading1',
            parent=styles['Heading1'],
            alignment=TA_CENTER
        )
        self.centered_heading2 = ParagraphStyle(
            name='CenteredHeading2',
            parent=styles['Heading2'],
            alignment=TA_CENTER
        )

    def _build_title_page(self):
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name='TitleStyle', parent=styles['Title'], alignment=1)
        info_style = ParagraphStyle(name='InfoStyle', parent=styles['Normal'], alignment=1)

        story = []
        story.append(Spacer(1, 100))
        story.append(Paragraph("Sales Data Analysis Report – Online Retail", title_style))
        story.append(Spacer(1, 40))
        story.append(Paragraph(f"Author: Sreekala Menon", info_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Date Generated: {datetime.today().strftime('%B %d, %Y')}", info_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Data Source: UCI Machine Learning Repository", info_style))
        story.append(PageBreak())
        return story

    def _build_level_1_content(self, data):
        styles = getSampleStyleSheet()
        normal_style = styles["BodyText"]
        heading_style = ParagraphStyle(name='CenteredHeading1', parent=styles['Heading1'], alignment=1)
        story = []

        # Add heading
        story.append(Paragraph("LEVEL-1 ANALYSIS", self.centered_heading1))
        story.append(Spacer(1, 6))
        story.append(Paragraph(data["description"], normal_style))
        story.append(Spacer(1, 12))

        # Column Descriptions Table
        story.append(Paragraph("Column Descriptions", styles["Heading2"]))
        story.append(Spacer(1, 6))

        col_data = [["Column", "Description"]] + [
            [k, Paragraph(v, normal_style)] for k, v in data["column_descriptions"].items()]
        col_table = Table(col_data, colWidths=[100, 380], hAlign='LEFT')
        col_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ])
        story.append(col_table)
        story.append(Spacer(1, 12))

        # Data Types Table
        story.append(Paragraph("Column Data Types", styles["Heading2"]))
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

        # KPI Table
        story.append(Paragraph("Key Performance Indicators", styles["Heading2"]))
        story.append(Spacer(1, 6))
        kpi_data = [
            ["Metric", "Value"],
            ["Total Transactions", data.get("kpis", {}).get("total_transactions", "-")],
            ["Total Revenue", data.get("kpis", {}).get("total_revenue", "-")],
            ["Avg Revenue per Invoice", data.get("kpis", {}).get("avg_revenue", "-")],
            ["Unique Customers", data.get("kpis", {}).get("unique_customers", "-")],
        ]
        kpi_table = Table(kpi_data, colWidths=[200, 150], hAlign='LEFT')
        kpi_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ])
        story.append(kpi_table)
        story.append(Spacer(1, 12))

        # Interesting Facts
        story.append(Paragraph("Interesting Facts", styles["Heading2"]))
        story.append(Spacer(1, 6))
        for key in sorted(data["interesting_facts"].keys()):
            story.append(Paragraph(f"• {data['interesting_facts'][key]}", normal_style))
            story.append(Spacer(1, 6))

        return story

    def generate_level_1_report(self, data, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = self._build_title_page() + self._build_level_1_content(data)
        doc.build(story)

    def generate_level_2_report(self, data_level1, data_level2, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = self._build_title_page() + self._build_level_1_content(data_level1)

        #styles = getSampleStyleSheet()
        story.append(Spacer(1, 12))
        story.append(PageBreak())
        story.append(Spacer(1, 24))
        story.append(Paragraph("LEVEL-2 ANALYSIS", self.centered_heading1))
        story.append(Spacer(1, 12))

        plot_titles = {
            "country_revenue_plot": "Top 10 Countries by Revenue",
            "monthly_revenue_plot": "Monthly Revenue Trend",
            "product_quantity_plot": "Top 10 Products by Quantity Sold",
            "top_customers_plot": "Top 10 Customers by Revenue"
        }

        for key, title in plot_titles.items():
            if key in data_level2:
                block = KeepTogether([
                    Paragraph(f"{title}", self.centered_heading2),
                    Spacer(1, 6),
                    Image(data_level2[key], width=6.0*inch, height=3.5*inch),
                    Spacer(1, 12)
                ])
                story.append(block)

        doc.build(story)

    def generate_level_3_report(self, data_level1, data_level2, data_level3, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = self._build_title_page() + self._build_level_1_content(data_level1)
        styles = getSampleStyleSheet()

        # LEVEL 2 SECTION
        story.append(PageBreak())
        story.append(Spacer(1, 24))
        story.append(Paragraph("LEVEL-2 ANALYSIS", styles["Heading1"]))
        story.append(Spacer(1, 12))

        plot_titles_level2 = {
            "country_revenue_plot": "Top 10 Countries by Revenue",
            "monthly_revenue_plot": "Monthly Revenue Trend",
            "product_quantity_plot": "Top 10 Products by Quantity Sold",
            "top_customers_plot": "Top 10 Customers by Revenue"
        }

        for key, title in plot_titles_level2.items():
            if key in data_level2:
                block = KeepTogether([
                    Paragraph(f"{title}", self.centered_heading2),
                    Spacer(1, 6),
                    Image(data_level2[key], width=6.0*inch, height=3.5*inch),
                    Spacer(1, 12)
                ])
                story.append(block)

        # LEVEL 3 SECTION
        story.append(PageBreak())
        story.append(Spacer(1, 24))
        story.append(Paragraph("LEVEL-3 ANALYSIS", self.centered_heading1))
        story.append(Spacer(1, 12))

        plot_titles_level3 = {
            "correlation_matrix_plot": "Correlation Heatmap of Numeric Features",
            "revenue_kde_plot": "Revenue Distribution (KDE Plot)",
            "scatter_quantity_revenue_plot": "Quantity vs Revenue by Country"
        }

        for key, title in plot_titles_level3.items():
            if key in data_level3:
                block = KeepTogether([
                    Paragraph(f"{title}", self.centered_heading2),
                    Spacer(1, 6),
                    Image(data_level3[key], width=6.0*inch, height=3.5*inch),
                    Spacer(1, 12)
                ])
                story.append(block)

        # KPI Trend Table
        if "monthly_kpi_csv" in data_level3:
            story.append(PageBreak())
            story.append(Paragraph("Monthly KPI Trends", styles["Heading1"]))
            story.append(Spacer(1, 6))

            df_kpi = pd.read_csv(data_level3["monthly_kpi_csv"])
            kpi_table_data = [df_kpi.columns.tolist()] + df_kpi.values.tolist()
            table_data = [
                [Paragraph(str(cell), styles["BodyText"]) for cell in row]
                for row in kpi_table_data
            ]

            kpi_table = Table(table_data, hAlign='LEFT', colWidths=[80, 100, 120, 120])
            kpi_table.setStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
            ])
            story.append(kpi_table)

        # Revenue Outlier Table
        if "revenue_outliers_csv" in data_level3:
            story.append(PageBreak())
            story.append(Paragraph("High Revenue Outliers", styles["Heading1"]))
            story.append(Spacer(1, 6))

            df_outliers = pd.read_csv(data_level3["revenue_outliers_csv"]).head(10)
            outlier_data = [df_outliers.columns.tolist()] + df_outliers.values.tolist()
            table_data = [
                [Paragraph(str(cell), styles["BodyText"]) for cell in row]
                for row in outlier_data
            ]

            outlier_table = Table(table_data, hAlign='LEFT', colWidths=[80, 100, 100, 100])
            outlier_table.setStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
            ])
            story.append(outlier_table)

        doc.build(story)
