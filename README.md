# Data Visualization Assignment

This project analyzes an online retail dataset to generate multi-level reports with insightful visualizations.

## Features

- **Level 1:** Basic dataset overview including column descriptions and data types.
- **Level 2:** Visual analysis with bar plots and line charts showing revenue trends.
- **Level 3:** Advanced analysis with correlation heatmaps, KDE plots, scatter plots, and boxplots.

## Installation

Make sure you have Python 3.x installed along with required packages:

```bash
pip install -r requirements.txt

Folder Structure
/assets          # Contains generated plot images and PDF reports
/logic           # Core processing and report generation modules
main.py          # Entry point of the application
requirements.txt # Python dependencies
README.md        # Project overview

Dependencies
pandas

matplotlib

seaborn

reportlab

Notes
The reports are saved as PDF files in the assets directory.

Level 3 analysis uses enhanced visualizations for deeper insights.

Ensure assets/ folder exists or the program will create it automatically.
